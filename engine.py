from os import stat
import numpy as np
import pyrr

from OpenGL.GL import *
from pyrr import vector

from Extensions import loaders
from pygame import image, Surface, mouse
from math import sin, cos, radians, floor



objects = []

# Vector3 
class Vector3:
    zero = pyrr.Vector3([0, 0, 0], dtype=np.int32)
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



class Mesh_Renderer:
    """
    Static game object \n
    functions:
        __init__: intialization
        create_buffers: this is called in __init__, if it isn't specified otherwise
        render: renders object
    """
    def __init__(self, vertices: np.array, indices: np.array, texture_img: image=None, rotation=(0, 0, 0), position=(0, 0, 0), create_buffers=True):
        """
        Creates object that contains data obout game object \n
        parameters:
            vertices: vertices of every face
            indices: indicies of triangles
            texture_img: texture image  
            rotation: obj rotation         
            position: obj position           
            create_buffers: bool, if the buffers should be created
            \n

        returns:
            nothing, use object functions for manipulation
        """
        self.VAO = None
        self.vertices = vertices.flatten().astype(dtype=np.float32)
        self.indices = indices.flatten().astype(dtype=np.uint32)
        self.rotation = list(rotation)
        self.position = pyrr.Vector3(list(position))
        self.texture_buff = None
        self.texture_path = texture_img

        if create_buffers:
            self.create_buffers()

        objects.append(self)


    def create_buffers(self):
        """
        Creates buffers for object
        """
        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)

        # Cube VAO
        glBindVertexArray(VAO)

        # Cube Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Cube Element Buffer Object
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        # Shader attribs
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 5, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.vertices.itemsize * 5, ctypes.c_void_p(12))

        if self.texture_path:
            texture_buff = glGenTextures(1)

            loaders.TextureLoader.load(self.texture_path, texture_buff)

            self.texture_buff = texture_buff

        self.VAO = VAO

    
    def render(self, model_loc):
        """
        Render object \n
            model_loc: pointer to shader variable
        """
        position = pyrr.matrix44.create_from_translation(self.position)
        rotation_x = pyrr.Matrix44.from_x_rotation(self.rotation[0], dtype=float)
        rotation_y = pyrr.Matrix44.from_y_rotation(self.rotation[1], dtype=float)
        rotation_z = pyrr.Matrix44.from_z_rotation(self.rotation[2], dtype=float)

        rotation = pyrr.matrix44.multiply(rotation_x, rotation_y)
        rotation = pyrr.matrix44.multiply(rotation, rotation_z)
        model = pyrr.matrix44.multiply(rotation, position)

        if not self.VAO:
            raise Error(f"{self} doesn't have buffers")

        glBindVertexArray(self.VAO)
        glBindTexture(GL_TEXTURE_2D, self.texture_buff)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)



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



# class Singleton(object):
#     _instance = None
#     def __new__(class_, *args, **kwargs):
#         if not isinstance(class_._instance, class_):
#             class_._instance = object.__new__(class_, *args, **kwargs)
#         return class_._instance



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

        self.view = pyrr.matrix44.create_look_at(self.transform.position, self.transform.position + self.front, self.up)




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
            
            
        #player_input = np.multiply(player_input + , self.speed)
        #TODO: implement jumping
        #player_input[1] = 0
        mouse_x, mouse_y = mouse_input
        mouse_x *= self.sensitivity
        mouse_y *= -self.sensitivity

        self.camera.transform.move(player_movement)
        self.camera.rotate((mouse_x, mouse_y))



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



def create_buffers():
    """Create buffers for all objects"""
    for obj in objects:
        obj.create_buffers()


def render_objects(model_loc):
    """Render all objects"""
    for obj in objects:
        obj.render(model_loc)
