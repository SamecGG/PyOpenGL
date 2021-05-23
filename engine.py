from os.path import abspath
import numpy as np
from numpy.lib.utils import deprecate
import pyrr

from OpenGL.GL import *
from pyrr import vector

from Extensions import loaders
from pygame import image, Surface, mouse, transform
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



<<<<<<< HEAD
class Cube_Renderer:
    """
    Static game object \n
    functions:
        __init__: intialization
        create_buffers: this is called in __init__, if it isn't specified otherwise
        render: renders object
    """
    def __init__(self, vertices: np.array, indices: np.array, atlas=TEXTURE_ATLAS):
        """
        Creates object that contains data obout game object \n
        parameters:
            vertices of cube: vertices of every face
            indices of cube: indicies of triangles
            texture_atlas: texture atlas object  
            \n
=======
# class Mesh_Instancer:
>>>>>>> master



class Cube_Instancer:
    def __init__(self, cube_vertices, cube_indices, texture_sheet):
        # Type Data Arrays
        self.object_types = []
        # Set instacing arrays to textures length
        self.instance_array = np.zeros((0, 3))
        self.instance_textures = np.zeros((0), dtype=np.int32)
        self.instance_array_len = 0

        # Cube data
        self.cube_vertices = cube_vertices
        self.cube_indices = cube_indices
        self.texture_sheet = texture_sheet

        # Objects
        self.IVBO = None
        self.VAO = None
<<<<<<< HEAD
        # Cube data
        self.vertices = vertices.flatten().astype(dtype=np.float32)
        self.indices = indices.flatten().astype(dtype=np.uint32)

        # Atlas
        self.texture_atlas = atlas

        # Instance data
        self.instance_data = np.zeros((0, 5), np.float32)
        # self.instance_positions = np.zeros((0, 3))
        # self.instance_textures = np.zeros((0))

        # creating Cube buffers
        self.create_buffers()
=======
        self.textures = None


    def add_object_type(self, texture_index):
        """
        texture: pygame Surface
        """
        self.object_types.append(texture_index)
>>>>>>> master


    def create_buffers(self):
        """
        Create buffers for all objects
        """

        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)
        texture = glGenTextures(1)

        #region Texture settings
        glBindTexture(GL_TEXTURE_2D, texture)

        # Set texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # Set texture filtering parameters, bylo tu GL_LINEAR 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #endregion

        # Cube VAO
        glBindVertexArray(VAO)

        # Cube Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.cube_vertices.nbytes, self.cube_vertices, GL_STATIC_DRAW)

        # Cube Element Buffer Object
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.cube_indices.nbytes, self.cube_indices, GL_STATIC_DRAW)
        
        # Shader attribs
        # cube vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.cube_vertices.itemsize * 5, ctypes.c_void_p(0))
        # cube textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.cube_vertices.itemsize * 5, ctypes.c_void_p(12))

<<<<<<< HEAD
        # Atlas texture binding
        atlas_texture = glGenTextures(1)
        self.texture_buff = loaders.TextureLoader.load(self.texture_atlas.atlas, atlas_texture)

        # glBindTexture(GL_TEXTURE_2D, self.texture_buff)
=======
        # Texure loading
        loaders.TextureAtlasLoader.load(self.texture_sheet.images, self.texture_sheet.img_size, 16, 16)

        self.textures = texture
        self.VAO = VAO

>>>>>>> master

    def instantiate(self, position: tuple[3] or list[3]=(0, 0, 0), texture: int=0):
        position = pyrr.Vector3(position)

        self.instance_textures = np.append(self.instance_textures, texture)
        self.instance_array = np.append(self.instance_array, position.reshape(1, 3), axis=0)

<<<<<<< HEAD
    
    def instantiate(self, position:tuple or list=(0, 0, 0), texture_index:int=0):
        """
        # Instantiate object into world at position, with texture_index
        this function just appends instance data to instance data array
        """
        # position.x, position.y, position.z texture index
        # to np array conversion
        position = np.array(position).reshape((3))
        texture_offset = np.array(self.texture_atlas.get_position(texture_index)).reshape((2))

        # append data to instance data arr
        data = np.append(position, texture_offset).reshape(1, 5)
        self.instance_data = np.append(self.instance_data, data, axis=0)


    def bake_instances(self):
        self.instance_data_len = len(self.instance_data)
        self.instance_data = self.instance_data.astype(np.float32).flatten()

        instanceVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, instanceVBO)
        glBufferData(GL_ARRAY_BUFFER, self.instance_data.nbytes, self.instance_data, GL_STATIC_DRAW)

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.instance_data.itemsize * 5, ctypes.c_void_p(0))
        glVertexAttribDivisor(2, 1) # 1 means, every instance will have it's own translate

        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 2, GL_FLOAT, GL_FALSE, self.instance_data.itemsize * 5, ctypes.c_void_p(12))
        glVertexAttribDivisor(3, 1) # 1 means, every instance will have it's own uv offset


    def render_all(self, model_loc):
        """
        Render object \n
            model_loc: pointer to shader variable
        """

        glDrawElementsInstanced(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None, self.instance_data_len)
=======

    def bake_arrays(self):
        IVBO = glGenBuffers(1)

        self.instance_array_len = len(self.instance_array)
        self.instance_array = self.instance_array.astype(np.float32).flatten()

        # Instance Veretex Buffer Object
        
        glBindBuffer(GL_ARRAY_BUFFER, IVBO)
        glBufferData(GL_ARRAY_BUFFER, self.instance_array.nbytes, self.instance_array, GL_STATIC_DRAW)

        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribDivisor(2, 1) # 1: every instance will have it's own position

        self.IVBO = IVBO

    def render_objects(self):
        glDrawElementsInstanced(GL_TRIANGLES, len(self.cube_indices), GL_UNSIGNED_INT, None, self.instance_array_len)
>>>>>>> master



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
    def __init__(self, fov:int=60, asp_ratio:float=16/9, near_plane: float=0.1, far_plane:int or float=100, position:tuple or list=(0, 2, 3), clamp:tuple or list=(-90, 90)):
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
        self.view = pyrr.matrix44.create_look_at(self.transform.position.astype(dtype=np.int32), self.transform.position.astype(dtype=np.int32) + self.front, self.up)


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
            
            
        #TODO: implement jumping
        mouse_x, mouse_y = mouse_input
        mouse_x *= self.sensitivity
        mouse_y *= -self.sensitivity

        self.camera.transform.move(player_movement)
        self.camera.rotate((mouse_x, mouse_y))
<<<<<<< HEAD
=======



# Texture Sheet
class TextureSheet:
    """
    Sheet is used for extracting each texture from Texture sheet
    Access images in this.images - list of individual textures

    functions:
        __init__
        load_area_at
    """
    def __init__(self, path, img_size):
        """
        parameters:
            path: path of texture sheet
            img_size: size of individual image (px)
        """
        sheet = image.load(path)

        if sheet:
            self.path = path
            self.sheet = sheet
            self.images = []
            self.img_size = img_size

            sheet_size = tuple(floor(x / img_size) for x in sheet.get_size())
            for y in range(sheet_size[1]):
                y *= img_size

                for x in range(sheet_size[0]):
                    i = x + floor(y/img_size) * sheet_size[1]
                    x *= img_size

                    self.load_area_at((x, y), img_size, i)            

    def load_area_at(self, position: tuple, img_size: int, index: int=0):
        """
        Loads picture from sheet \n
        parameters: 
            position: starting position of area that will be loaded
            img_size: size of image
            index: index, where will be this image inserted into this.images
        \n
        returns:
            pygame.Surface of loaded image
        """
        sheet = self.sheet
        img = Surface((img_size, img_size))

        for x in range(position[0], position[0] + img_size):
            for y in range(position[1], position[1] + img_size):
                pos = (x, y)
                pixel_pos = (x - position[0], y - position[1])
                color = sheet.get_at(pos)
                img.set_at(pixel_pos, color)

        self.images.insert(index, img)
        return img



def render_objects(model_loc):
    """Render all objects"""
    for obj in objects:
        obj.render(model_loc)
>>>>>>> master
