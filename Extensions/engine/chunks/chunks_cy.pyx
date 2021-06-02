from os import makedirs
from os.path import abspath, exists, join, isfile

from pyrr import Vector3

import numpy as np
cimport numpy as np

import time



cdef dict BlockTypes = {
    0: [],
    1: [3, 3, 3, 3, 2, 0],
}

cdef str WORLD_PATH = abspath('Worlds/1st_world/')
if not exists(WORLD_PATH):
    makedirs(WORLD_PATH)

# cube face normals
north = np.array([0, 0, -1], dtype=np.int8)
south = np.array([0, 0, 1], dtype=np.int8)
east = np.array([1, 0, 0], dtype=np.int8)
west = np.array([-1, 0, 0], dtype=np.int8)
up = np.array([0, 1, 0], dtype=np.int8)
down = np.array([0, -1, 0], dtype=np.int8)

# cube face normal list
normals = np.array([south, north, east, west, down, up])


cdef class Chunk:
    cpdef public int position[3]

    # atlas
    cdef unsigned int atlas_rows

    cdef public np.ndarray vertices
    # 16 * 64 * 16
    cdef public int chunk_data[16384]


    def __init__(self, atlas_rows, chunk_position: tuple=(0, 0, 0)):
        self.position = [*chunk_position]

        self.atlas_rows = atlas_rows
        self.vertices = np.zeros(0, np.float32)
        # self.chunk_data = np.zeros(0)


    cpdef generate_chunk(Chunk self):
        cdef:
            int height = 10
            int data = 0
            int chunk_data[16384]

            int x
            int y
            int z

        for x in range(16):
            for y in range(64):
                for z in range(16):
                    if y < height:
                        # append block - block type (default: 1)
                        data = 1
                    else:
                        data = 0

                    chunk_data[x * 1024 + y * 16 + z] = data

        self.chunk_data = chunk_data


    cdef generate_face(Chunk self, int block_position[3], int face_index, int texture):
        cdef int rows = self.atlas_rows
        cdef int column = texture % rows
        cdef int row = texture / rows
        cdef float texture_x = <float>column / rows
        cdef float texture_y = <float>row / rows

        cdef float data[6]
        data[:] = [block_position[0], block_position[1], block_position[2], face_index, texture_x, texture_y] 

        # block_pos-3 places(can be converted to 1 number), face_index-1place, atlas_offset-2 places
        
        self.vertices = np.append(self.vertices, data)


    cpdef generate_mesh(Chunk self, data):
        # 4 vertices per each face
        # 3 * 2 triangle indices per each face
        cdef:
            int x
            int y
            int z

            int block_position[3]
            int block_type
            int block_type_array[6]
            int block_data
            int index
            int face_index

            bint x_bound = False
            bint y_bound = False
            bint z_bound = False

            int check_position_x
            int check_position_y
            int check_position_z

        for x in range(16):
            for y in range(64):
                for z in range(16):
                    # block variables
                    block_position = [x, y, z]
                    block_type = data[block_position[0] * 1024 + block_position[1] * 16 + block_position[2]]
                    block_type_array[:] = [0, 0, 0, 0, 0, 0]

                    if block_type:
                        block_type_array = BlockTypes[block_type]

                    if block_type == 0:
                        continue

                    # check for each face if is exposed (next to 0 or out of limit)
                    face_index = 0 
                    for face_index in range(6):
                        face_normal = normals[face_index]
                        check_position_x, check_position_y, check_position_z = block_position + face_normal

                        x_bound = 0 <= check_position_x < 16
                        y_bound = 0 <= check_position_y < 64
                        z_bound = 0 <= check_position_z < 16

                        if (x_bound and y_bound and z_bound):
                            index = check_position_x * 1024 + check_position_y * 16 + check_position_z
                            block_data = data[index]

                            if block_data == 0:
                                self.generate_face(block_position, face_index, block_type_array[face_index])
                        else:
                            self.generate_face(block_position, face_index, block_type_array[face_index])
        

cdef int FAILED = -1
cdef int SUCCESS = 0

cpdef save(list position, np.ndarray data):
    start_time = time.time()
    print(f"Loading chunk at: {position}")
    with open(join(WORLD_PATH, f'{position[0]}_{position[2]}.npy'), 'wb') as f:
        np.save(f, data)
        return SUCCESS
    print('chunk file save: ', (time.time() - start_time) * 1000)


cpdef load(position: tuple[3] or list[3], atlas):
    file_path = join(WORLD_PATH, f'{position[0]}_{position[2]}.npy')
    print(f"Loading chunk at: {position}")
    cdef tuple chunk_pos = position
    cdef Chunk chunk = Chunk(atlas.rows, chunk_pos)

    cdef np.ndarray data

    if not exists(file_path):
        # create chunk
        chunk.generate_chunk()
    else:
        with open(file_path, 'rb') as f:
            data = np.load(f)
            chunk.chunk_data = data

    chunk.generate_mesh(chunk.chunk_data)
    return chunk

