import numpy as np
from numpy.core.numeric import indices



class Cube:
    #region Maps
    vertex_face_map = np.array([
        0, 1, 2, 3,
        4, 5, 6, 7,

        5, 6, 2, 1,
        7, 4, 0, 3, 

        4, 5, 1, 0,
        6, 7, 3, 2
    ], dtype=np.uint16)

    uv_map = np.array([
        [0.0, 0.0,],
        [1.0, 0.0,],
        [1.0, 1.0,], 
        [0.0, 1.0]
    ], dtype=np.float16)
    #endregion

    def __init__(self, length=1):
        self.vertices = np.zeros((8, 3))
        self.cube_map = np.zeros((6, 4, 5))
        self.indices = np.zeros((6, 6))
        # self.normals = np.array([
        #     [0, 0, 1], [0, 0, -1],
        #     [1, 0, 0], [-1, 0, 0],
        #     [-1, 0, 0], [1, 0, 0]
        #     ])

        self.create_indices()
        self.create_verticies()
        self.create_faces()

    
    def create_verticies(self):
        """Creates individual verticies of cube"""
        vertices = np.zeros(shape=(8, 3))

        for z in range(1, 3):
            for y in range(2):
                for x in range(2):
                # vertex creation
                    vertices[(z - 1) * 4 + y * 2 + x] = [(x + y) % 2 - 0.5, y % 2 - 0.5, z % 2 - 0.5]

        self.vertices = vertices
        return vertices

    def create_faces(self):
        """Creates verticies for each face"""
        vertices = self.vertices.reshape(8, 3)

        if not np.all(vertices):
            print(f"WARNING: {self} doesn't have any vertices")

        cube_map = np.zeros(shape=(0, 5))
        for i in range(6):
            for j in range(4):
                index = i * 4 + j
                vertex_index = Cube.vertex_face_map[index]
                
                vertex_position = vertices[vertex_index]
                uv_position = Cube.uv_map[j]

                face_data = np.append(vertex_position, uv_position)
                cube_map = np.append(cube_map, face_data)
        
        self.cube_map = cube_map.reshape(6, 4, 5)
        return cube_map


    def create_indices(self):
        """Creates indicies of vertices that make up individual triagnle of faces"""
        indices = np.zeros(shape=(6, 0))

        for i in range(6):
            n = i * 4
            face = np.empty(0)

            for j in range(3):
                face = np.append(face, n + j)

            for j in range(2, 4):
                face = np.append(face, n + j)

            face = np.append(face, n)
            indices = np.append(indices, face)  
        
        self.indices = indices
        return indices 