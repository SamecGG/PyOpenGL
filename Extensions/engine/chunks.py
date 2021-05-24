import sys

sys.path.append("..\Extensions")
from geometry import Cube

from pyrr import Vector3
from numpy import uint8
from numpy import zeros, array, append

class Chunk:
    CHUNK_SIZE = Vector3([12, 3, 12], dtype=uint8)
    CUBE = Cube()
    CUBE_FACE_VERTICES = CUBE.cube_map
    CUBE_FACE_INDICES = CUBE.create_indices()

    def __init__(self, chunk_position: tuple[2] or list[2] = (0, 0)):
        self.chunk_position = array(chunk_position)

        self.mesh_vertices = zeros(0)
        self.mesh_indices = zeros(0)


    def generate_chunk(self, height):
        height = min(height, Chunk.CHUNK_SIZE.y)
        chunk_data = zeros(0)
        # chunk_data_textures = zeros(0)

        for x in range(Chunk.CHUNK_SIZE.x):
            for y in range(Chunk.CHUNK_SIZE.y):
                for z in range(Chunk.CHUNK_SIZE.z):
                    if y < height:
                        # append block - 1
                        data = (1, 0)
                        # cube_instancer.instantiate((x, y, z), 0)
                    else:
                        # append air - 0
                        data = (0, 0)

                    chunk_data = append(chunk_data, data[0])
                    # chunk_data_textures = append(chunk_data_textures, data[1])

        # print(chunk_data)
        self.chunk_data = chunk_data
        #self.chunk_data_textures = chunk_data_textures


    @staticmethod
    def data_index_to_position(index):
        yz_size = Chunk.CHUNK_SIZE.y * Chunk.CHUNK_SIZE.z

        x = index // yz_size
        y = index // Chunk.CHUNK_SIZE.z
        z = index % yz_size

        return x, y, z


    def generate_mesh(self):
        # if self.chunk_data.any():
        #     self.generate_chunk(10)

        # 4 vertices per each face
        # 3 * 2 triangle indices per each face

        for x in range(Chunk.CHUNK_SIZE.x):
            for y in range(Chunk.CHUNK_SIZE.y):
                for z in range(Chunk.CHUNK_SIZE.z):
                    # check for each face if is exposed (next to 0 or out of limit)
                    cube_position = Vector3([x, y, z])

                    for face_index in range(0, 6):
                    # if
                        face_normal = Cube.faces_normals[face_index]

                        check_position = cube_position + face_normal
                        print(cube_position, check_position)

                        if 0 <= check_position.x < Chunk.CHUNK_SIZE.x and 0 <= check_position.y < Chunk.CHUNK_SIZE.y and 0 <= check_position.z < Chunk.CHUNK_SIZE.z:
                            block_data = self.chunk_data[check_position.x * Chunk.CHUNK_SIZE.y * Chunk.CHUNK_SIZE.z + check_position.y * Chunk.CHUNK_SIZE.z + check_position.z]
                            if block_data == 0:
                                self.generate_face(cube_position, face_index)
                        else:
                            self.generate_face(cube_position, face_index)

                        # check if check_position is out of bounds
                        # if 0 <= check_position.x * Chunk.CHUNK_SIZE.y * Chunk.CHUNK_SIZE.z + check_position.y * Chunk.CHUNK_SIZE.z + check_position.z < len(self.chunk_data):
                        #     block_data = self.chunk_data[check_position.x * Chunk.CHUNK_SIZE.y * Chunk.CHUNK_SIZE.z + check_position.y * Chunk.CHUNK_SIZE.z + check_position.z]

                        #     if block_data == 0:
                        #         self.generate_face(cube_position, face_index)
                        # else:
                        #     self.generate_face(cube_position, face_index)
                            # print('krajni: ', check_position, cube_position)
        print(self.mesh_indices)


    def generate_face(self, cube_position, face_index):
        vertices = [[vertex + cube_position[index] for index, vertex in enumerate(x[:3])] for x in Chunk.CUBE_FACE_VERTICES[face_index]]
        # print(vertices)
        print(len(self.mesh_indices) // 6)
        indices = [len(self.mesh_indices) // 6 * 4 + index for index in Chunk.CUBE_FACE_INDICES[:6]]
        print(cube_position.x, indices)
        # print(vertices, indices)
        # texture_index = self.chunk_data_textures[cube_position.x, cube_position.y, cube_position.z]

        self.mesh_vertices = append(self.mesh_vertices, vertices)
        self.mesh_indices = append(self.mesh_indices, indices)
        # self.texture_indices = append(self.texture_indices, texture_index)
