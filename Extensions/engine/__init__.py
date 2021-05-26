from os.path import abspath
import numpy as np
import pyrr

from OpenGL.GL import *
from pyrr import vector

from Extensions import loaders
from math import sin, cos, radians, floor



# objects = []
TEXTURE_ATLAS = loaders.TextureAtlas(abspath('Assets/Textures/minecraft_texture_sheet.png'), 48)

# Vector3 
class Vector3:
    zero = pyrr.Vector3([0, 0, 0], dtype=float)
    up = pyrr.Vector3([0, 1, 0], dtype=float)
    forward = pyrr.Vector3([0, 0, 1], dtype=float)
    right = pyrr.Vector3([1, 0, 0], dtype=float)

    @staticmethod
    def isZero(vector3):
        """
        Check if array / vector is all zeros
        returns:
            True if is all zeros
        """
        condition = True

        for x in vector3:
            condition &= not x
        
        return condition

    @staticmethod
    def isZero(vector3, callback):
        condition = True
        for x in vector3:
            condition &= not x
        
        if not condition:
            return callback()
        
        return vector3



class Transform:
    """
    COMPONENT,
    keeps track of object position and rotation
    """
    def __init__(self, position:tuple or list=(0, 2, 0), rotation: tuple or list=(0, 0, 0)):
        self._position = pyrr.Vector3(position, dtype=float)
        self._rotation = pyrr.Vector3(rotation, dtype=float)
        self._parent = None

    #region Properties
    @property
    def position(self):
        return self._position

    @property
    def rotation(self):
        return pyrr.Quaternion.from_eulers(self._rotation)

    @property
    def eulers(self):
        return self._rotation

    @property
    def parent(self):
        return self._parent
    #endregion

    #region Setters
    @position.setter
    def position(self, new_postion):
        self.move_to_position(new_postion)

    @rotation.setter
    def rotation(self, new_eulers):
        self.rotate_to(new_eulers)
    #endregion

    #region Functions
    #region Movement
    def move(self, direction: tuple or list):
        direction = pyrr.Vector3(direction, dtype=float)
        self._position += direction

    def move_to(self, new_position: tuple or list):
        new_position = pyrr.Vector3(new_position, dtype=float)
        self._position = new_position

    # def move_look_at(self, direction: tuple or list, target: tuple or list=(0, 0, 0)):
    #     direction = pyrr.Vector3(direction)
    #     target = pyrr.Vector3(target)
    #     self.view = pyrr.matrix44.create_look_at(self.position + direction, target, self.up)
    #endregion

    #region Rotation
    def rotate(self, rotation: tuple or list):
        rotation = pyrr.Vector3(rotation, dtype=float)
        self._rotation += rotation

    def rotate_to(self, new_rotation: tuple or list):
        new_rotation = pyrr.Vector3(new_rotation, dtype=float)
        self._rotation = new_rotation
    #endregion
    #endregion



class Chunk_Renderer:
    """
    Static game object \n
    functions:
        __init__: intialization
        create_buffers: this is called in __init__, if it isn't specified otherwise
        render: renders object
    """
    def __init__(self, vertices: np.array, position:tuple[3] or list[3], atlas=TEXTURE_ATLAS):
        """
        Creates object that contains data obout game object \n
        parameters:
            vertices of cube: vertices of every face
            indices of cube: indicies of triangles
            texture_atlas: texture atlas object  
            \n

        returns:
            nothing, use object functions for manipulation
        """
        self.VAO = None
        self.vertices = vertices.flatten().astype(dtype=np.float32)
        self.position = position

        # Atlas
        self.texture_atlas = atlas

        # creating Cube buffers
        self.create_buffers()


    def create_buffers(self):
        """
        Creates buffers for object
        """

        VBO = glGenBuffers(1)

        # Points Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # VBO attribs
        # Poisiton
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 6, ctypes.c_void_p(0))

        # Normal - face index
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 6, ctypes.c_void_p(12))

        # Texture offset
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 6, ctypes.c_void_p(16))

        # Atlas texture binding
        atlas_texture = glGenTextures(1)
        self.texture_buff = loaders.TextureLoader.load(self.texture_atlas.atlas, atlas_texture)


    def render_all(self, loc_chunk_pos):
        """
        Render object \n
            model_loc: pointer to shader variable
        """
        glUniform3f(loc_chunk_pos, *self.position)
        glDrawArrays(GL_POINTS, 0, self.vertices.nbytes // (4 * 6))
        # glDrawElementsInstanced(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None, self.instance_data_len)



class Object:
    def __init__(self, position: tuple[3] or list[3]=(0, 0, 0), rotation:tuple[3] or list[3]=(0, 0, 0), *args):
        self.transform = Transform(position, rotation)

        for x in args:
            self.add_component(x)

    def add_component(self, component: object):
        name = component.__class__.__name__.lower()
        setattr(self, name, component)

    def remove_component(self, name: str):
        delattr(self, name)



class Camera(Object):
    def __init__(self, fov:int=45, asp_ratio:float=16/9, near_plane: float=0.1, far_plane:int or float=100, position:tuple or list=(0, 2, 3), clamp:tuple or list=(-90, 90)):
        """"""
        super().__init__(position, rotation=(-90, 0, 0))
        # yaw = y, pitch = x, roll = z
        self.yaw = -90
        self.pitch = 0

        self.clamp = clamp

        self.up = Vector3.up
        self.front = -Vector3.forward
        self.right = Vector3.right

        # projection matrix
        self.projection = pyrr.matrix44.create_perspective_projection_matrix(fov, asp_ratio, near_plane, far_plane)
        # view matrix
        self.view = pyrr.matrix44.create_look_at(self.transform.position.astype(dtype=np.int32), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))


    def rotate(self, mouse_input: tuple[2] or list[2]):
        yaw = self.yaw
        pitch = self.pitch
        clamp_min, clamp_max = self.clamp
        mouse_x, mouse_y = mouse_input

        # clamp y input between min, max
        pitch = max(clamp_min, min(clamp_max, pitch + mouse_y))
        yaw += mouse_x

        front = pyrr.Vector3([0, 0, 0], dtype=float)
        front.x = cos(radians(yaw)) * cos(radians(pitch))
        front.y = sin(radians(pitch))
        front.z = sin(radians(yaw)) * cos(radians(pitch))

        self.front = vector.normalize(front)
        self.right = vector.normalize(pyrr.vector3.cross(self.front, Vector3.up))
        self.up = vector.normalize(pyrr.vector3.cross(self.right, self.front))

        self.yaw = yaw
        self.pitch = pitch
        
        x = self.transform.position + pyrr.Vector3(self.front)
        self.view = pyrr.matrix44.create_look_at(self.transform.position, x, self.up)

    def raycast_chunk(self, ray_length=1):
        pass




class Player(Object):
    def __init__(self, camera: Camera, sensitivity=0.25, speed=0.15, position:tuple or list=(0, 0, 3), rotation:tuple or list=(0, 0, 0)):
        super().__init__(position, rotation)
        self.sensitivity = sensitivity
        self.speed = speed

        self.camera = camera


    def process_input(self, mouse_input, player_input):
        player_input, self.camera.front, self.speed
        player_input = pyrr.Vector3(player_input)
        player_movement = np.array([0, 0, 0], dtype=float)

        if not player_input.x == 0:
            player_movement += self.camera.right * self.speed * player_input.x
        if not player_input.z == 0:
            player_movement += self.camera.front * self.speed * player_input.z
        if not player_input.y == 0:
            player_movement += Vector3.up * self.speed * player_input.y
            
        mouse_x, mouse_y = mouse_input
        mouse_x *= self.sensitivity
        mouse_y *= -self.sensitivity

        self.camera.transform.move(player_movement)
        self.camera.rotate((mouse_x, mouse_y))
