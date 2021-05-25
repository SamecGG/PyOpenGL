import sys

sys.path.append("..\Extensions")
from geometry import Cube
from engine import TEXTURE_ATLAS

from pyrr import Vector3
from numpy import uint8
from numpy import zeros, array, append



BlockTypes = {
    0: [1, 1, 1, 1, 1, 1]
}
    



class Chunk:
    CHUNK_SIZE = Vector3([16, 3, 16], dtype=uint8)
    CUBE = Cube()
    CUBE_FACE_VERTICES = CUBE.cube_map
    CUBE_FACE_INDICES = CUBE.create_indices()

    def __init__(self, chunk_position: tuple[2] or list[2] = (0, 0), atlas=TEXTURE_ATLAS):
        self.chunk_position = array(chunk_position)

        self.mesh_vertices = zeros(0)
        self.mesh_indices = zeros(0)
        self.atlas = atlas


    def generate_chunk(self, height):
        height = min(height, Chunk.CHUNK_SIZE.y)
        chunk_data = zeros(0)
        chunk_data_types = zeros(0)
        # chunk_data_textures = zeros(0)

        for x in range(Chunk.CHUNK_SIZE.x):
            for y in range(Chunk.CHUNK_SIZE.y):
                for z in range(Chunk.CHUNK_SIZE.z):
                    if y < height:
                        # append block - 1
                        data = (1, 0)
                    else:
                        # append air - 0
                        data = (0, 0)

                    chunk_data = append(chunk_data, data[0])
                    chunk_data_types = append(chunk_data_types, data[1])

        self.chunk_data = chunk_data
        self.chunk_data_types = chunk_data_types


    @staticmethod
    def data_index_to_position(index):
        yz_size = Chunk.CHUNK_SIZE.y * Chunk.CHUNK_SIZE.z

        x = index // yz_size
        y = index // Chunk.CHUNK_SIZE.z
        z = index % yz_size

        return x, y, z


    def generate_mesh(self):
        # 4 vertices per each face
        # 3 * 2 triangle indices per each face

        for x in range(Chunk.CHUNK_SIZE.x):
            for y in range(Chunk.CHUNK_SIZE.y):
                for z in range(Chunk.CHUNK_SIZE.z):
                    # check for each face if is exposed (next to 0 or out of limit)
                    cube_position = Vector3([x, y, z])
                    block_type = self.chunk_data_types[cube_position.x * Chunk.CHUNK_SIZE.y * Chunk.CHUNK_SIZE.z + cube_position.y * Chunk.CHUNK_SIZE.z + cube_position.z]
                    block_type_array = BlockTypes[block_type]

                    for face_index in range(0, 6):
                    # if
                        face_normal = Cube.faces_normals[face_index]

                        check_position = cube_position + face_normal

                        if 0 <= check_position.x < Chunk.CHUNK_SIZE.x and 0 <= check_position.y < Chunk.CHUNK_SIZE.y and 0 <= check_position.z < Chunk.CHUNK_SIZE.z:
                            block_data = self.chunk_data[check_position.x * Chunk.CHUNK_SIZE.y * Chunk.CHUNK_SIZE.z + check_position.y * Chunk.CHUNK_SIZE.z + check_position.z]
                            if block_data == 0:
                                self.generate_face(cube_position, face_index, block_type_array[face_index])
                        else:
                            self.generate_face(cube_position, face_index,block_type_array[face_index])


    def generate_face(self, cube_position, face_index, texture):
        vertices = [[vertex + cube_position[index] for index, vertex in enumerate(x[:3])] for x in Chunk.CUBE_FACE_VERTICES[face_index]]
        indices = [len(self.mesh_indices) // 6 * 4 + index for index in Chunk.CUBE_FACE_INDICES[:6]]
        uv = self.atlas.get_position(texture)
        uv = [uv_pair / self.atlas.rows + uv for uv_pair in Cube.uv_map]
        print(vertices, uv)
        vertices = append(vertices, uv, axis=1)

        self.mesh_vertices = append(self.mesh_vertices, vertices)
        self.mesh_indices = append(self.mesh_indices, indices)
