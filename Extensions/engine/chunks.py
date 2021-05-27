from posixpath import abspath
import sys

sys.path.append("..\Extensions")
from geometry import Cube

from os import makedirs
from os.path import abspath, exists, join, isfile
from pyrr import Vector3
from numpy import float16, uint8
from numpy import zeros, array, append, save, load



BlockTypes = {
    0: [],
    1: [3, 3, 3, 3, 2, 0],
}

WORLD_PATH = abspath('Worlds/1st_world/')
if not exists(WORLD_PATH):
    makedirs(WORLD_PATH)



class Chunk:
    CHUNK_SIZE = Vector3([16, 128, 16], dtype=uint8)
    CHUNK_SIZE_yz = CHUNK_SIZE.y * CHUNK_SIZE.z
    CUBE = Cube()

    def __init__(self, atlas, chunk_position: tuple[3] or list[3] = (0, 0, 0)):
        self.position = array(chunk_position)

        self.atlas = atlas
        self.vertices = zeros(0, float16)
        self.chunk_data = zeros(0)


    def generate_chunk(self, height: int or float):
        height = min(height, Chunk.CHUNK_SIZE.y)
        chunk_data = zeros(0)

        for x in range(Chunk.CHUNK_SIZE.x):
            for y in range(Chunk.CHUNK_SIZE.y):
                for z in range(Chunk.CHUNK_SIZE.z):
                    if y < height:
                        # append block - block type (default: 1)
                        data = 1
                    else:
                        # append air - 0
                        data = 0

                    chunk_data = append(chunk_data, data)

        self.chunk_data = chunk_data

    @property
    def grid_position(self):
        return self.position // Chunk.CHUNK_SIZE

    @staticmethod
    def data_index_to_position(index):
        x = index // Chunk.CHUNK_SIZE_yz
        y = index // Chunk.CHUNK_SIZE.z
        z = index % Chunk.CHUNK_SIZE_yz

        return x, y, z


    def generate_mesh(self):
        # 4 vertices per each face
        # 3 * 2 triangle indices per each face

        for x in range(Chunk.CHUNK_SIZE.x):
            for y in range(Chunk.CHUNK_SIZE.y):
                for z in range(Chunk.CHUNK_SIZE.z):
                    # block variables
                    block_position = Vector3([x, y, z])
                    block_type = self.chunk_data[block_position.x * Chunk.CHUNK_SIZE_yz + block_position.y * Chunk.CHUNK_SIZE.z + block_position.z]
                    if block_type:
                        block_type_array = BlockTypes[block_type]

                    if block_type == 0:
                        continue

                    # check for each face if is exposed (next to 0 or out of limit)
                    for face_index in range(0, 6):
                        face_normal = Cube.normals[face_index]
                        check_position = block_position + face_normal

                        if 0 <= check_position.x < Chunk.CHUNK_SIZE.x and 0 <= check_position.y < Chunk.CHUNK_SIZE.y and 0 <= check_position.z < Chunk.CHUNK_SIZE.z:
                            block_data = self.chunk_data[check_position.x * Chunk.CHUNK_SIZE_yz + check_position.y * Chunk.CHUNK_SIZE.z + check_position.z]

                            if block_data == 0:
                                self.generate_face(block_position, face_index, block_type_array[face_index])
                        else:
                            self.generate_face(block_position, face_index,block_type_array[face_index])


    def generate_face(self, block_position, face_index, texture:int):
        # block_pos-3 places(can be converted to 1 number), face_index-1place, atlas_offset-2 places
        data = [*(block_position), face_index, *self.atlas.get_position(texture)]
        data = array(data, dtype=float16)

        self.vertices = append(self.vertices, data)



class ChunkManager:
    FAILED = -1
    SUCCESS = 0

    @staticmethod
    def save(position: tuple[3] or list[3], data):
        with open(join(WORLD_PATH, f'{position[0]}_{position[2]}.npy'), 'w') as f:
            save(f, data)
            return ChunkManager.SUCCESS


    @staticmethod
    def load(position: tuple[3] or list[3], atlas):
        file_path = join(WORLD_PATH, f'{position[0]}_{position[2]}.npy')
        chunk = Chunk(atlas, position * Chunk.CHUNK_SIZE)

        if not exists(file_path):
            # create chunk
            chunk.generate_chunk(10)
        else:
            with open(file_path, 'r') as f:
                data = load(f)
                chunk.chunk_data = data
        
        chunk.generate_mesh()
        return chunk
