import pygame
import numpy as np
import pyrr
import os, math
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from Extensions import loaders

# TODO: shader from file to str loader
# pygame init
# TODO: Cube creator -
# TODO: Quad creator
# TODO: VAO, VBO, EBO handling functions
# TODO: Texture bind
# OpenGL settings
# calculating render (projection, pos)
# view
# pointers setting (model, proj, view)
# main loop:
#   TODO: rendering

shader = loaders.ShaderLoader.load(os.path.abspath("Assets/Shaders/Basic.shader"))
# projection matrix
projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
# camera; eye, target, up
view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 3]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))

class Object:
    def __init__(self, vertices, indices, texture_path=None, rotation=(0, 0, 0), position=(0, 0, 0)):
        self.vertices = vertices
        self.indices = indices
        self.rotation = rotation
        self.position = pyrr.Vector3(position)

        if texture_path:
            texture_buff = glGenTextures(1)

            loaders.TextureLoader.load(texture_path, texture_buff)

            self.texture_buff = texture_buff


    def create_buffers(self):
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

        self.VAO = VAO

    
    def render(self, model_loc):
        position = pyrr.matrix44.create_from_translation(self.position)
        rotation_x = pyrr.Matrix44.from_x_rotation(self.rotation[0])
        rotation_y = pyrr.Matrix44.from_x_rotation(self.rotation[1])
        rotation_z = pyrr.Matrix44.from_x_rotation(self.rotation[2])

        rotation = pyrr.matrix44.multiply(rotation_x, rotation_y, rotation_z)
        model = pyrr.matrix44.multiply(rotation, position)

        glBindVertexArray(self.VAO)
        glBindTexture(GL_TEXTURE_2D, self.texture_buff)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
