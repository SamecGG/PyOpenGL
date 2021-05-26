import sys

from numpy.core.shape_base import block

sys.path.append("..\Extensions")
from geometry import Cube
from engine import TEXTURE_ATLAS

from pyrr import Vector3, quaternion
from numpy import float16, uint8
from numpy import zeros, array, append



BlockTypes = {
    0: [],
    1: [3, 3, 3, 3, 2, 0],
}
    



class Chunk:
    CHUNK_SIZE = Vector3([16, 30, 16], dtype=uint8)
    CUBE = Cube()
    CUBE_FACE_VERTICES = CUBE.cube_map
    CUBE_FACE_INDICES = CUBE.create_indices()

    def __init__(self, chunk_position: tuple[3] or list[3] = (0, 0, 0), atlas=TEXTURE_ATLAS):
        self.chunk_position = array(chunk_position)

        self.atlas = atlas
        self.vertices = zeros(0, float16)


    def generate_chunk(self, height):
        height = min(height, Chunk.CHUNK_SIZE.y)
        chunk_data = zeros(0)
        # chunk_data_textures = zeros(0)

        for x in range(Chunk.CHUNK_SIZE.x):
            for y in range(Chunk.CHUNK_SIZE.y):
                for z in range(Chunk.CHUNK_SIZE.z):
                    if y < height:
                        # append block - 1
                        data = 1
                    else:
                        # append air - 0
                        data = 0

                    chunk_data = append(chunk_data, data)

        print(chunk_data)
        self.chunk_data = chunk_data


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
                    # block variables
                    block_position = Vector3([x, y, z])
                    block_type = self.chunk_data[block_position.x * Chunk.CHUNK_SIZE.y * Chunk.CHUNK_SIZE.z + block_position.y * Chunk.CHUNK_SIZE.z + block_position.z]
                    if block_type:
                        block_type_array = BlockTypes[block_type]

                    if block_type == 0:
                        continue

                    # check for each face if is exposed (next to 0 or out of limit)
                    for face_index in range(0, 6):
                        face_normal = Cube.normals[face_index]
                        check_position = block_position + face_normal

                        if 0 <= check_position.x < Chunk.CHUNK_SIZE.x and 0 <= check_position.y < Chunk.CHUNK_SIZE.y and 0 <= check_position.z < Chunk.CHUNK_SIZE.z:
                            block_data = self.chunk_data[check_position.x * Chunk.CHUNK_SIZE.y * Chunk.CHUNK_SIZE.z + check_position.y * Chunk.CHUNK_SIZE.z + check_position.z]

                            if block_data == 0:
                                self.generate_face(block_position, face_index, block_type_array[face_index])
                        else:
                            self.generate_face(block_position, face_index,block_type_array[face_index])


    def generate_face(self, block_position, face_index, texture:int):
        # block_pos, normal, texture
        normal = Cube.normals[face_index]

        # block_pos-3 places(can be converted to 1 number), face_index-1place, atlas_offset-2 places
        data = [*(block_position), face_index, *self.atlas.get_position(texture)]
        data = array(data, dtype=float16)

        self.vertices = append(self.vertices, data)