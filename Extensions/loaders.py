#region TextureLoader
from OpenGL.GL import *
from pygame import image, transform
#endregion

#region TextureAtlasLoader 
import numpy as np
#endregion

class ShaderLoader:
    @staticmethod
    def load(path, shaders=2):
        result = [""]
        with open(path, 'r') as f:
            line = f.readline()
            index = 0

            while line:
                if line.find('//shader') >= 0 and result[index]:
                    result.append("")
                    index += 1  

                result[index] += str(line)
                line = f.readline()

        return result

class TextureLoader:
    @staticmethod
    def load(img):
        # load image
        img = transform.flip(img, False, True)
        img_width, img_height = img.get_rect().size
        img_data = image.tostring(img, "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
<<<<<<< HEAD
        return texture



class TextureAtlas:
    def __init__(self, path, img_size):
        # load image
        img = image.load(path)
        img = transform.flip(img, False, True)
        img_width, img_height = img.get_rect().size
        # img_data = image.tostring(img, "RGBA")
        rows = img_height // img_size
        columns = img_width // img_size
        
        self.atlas = img
        self.rows, self.columns = rows, columns

    def get_position(self, index):
        column = index % self.rows
        row = index//self.rows

        return float(column/self.rows), float(row/self.rows) 
=======

class TextureAtlasLoader:
    @staticmethod
    def load(texture_sheet, img_size, img_count_x, img_count_y):
        img_count = img_count_x * img_count_y

        glTexImage3D(GL_TEXTURE_2D_ARRAY, 0, GL_RGBA, 
             img_size, img_size, img_count, 0,
             GL_RGBA, GL_UNSIGNED_BYTE, None)

        for iy in range(img_count_y):
            for ix in range(img_count_x):
                i = iy * img_count_x + ix
                img = transform.flip(texture_sheet[i], False, True)
                img_data = image.tostring(img, "RGBA")

                glTexSubImage3D(GL_TEXTURE_2D_ARRAY, 0,
                    0, 0, i,
                    img_size, img_size, 1,
                    GL_RGBA, GL_UNSIGNED_BYTE, img_data)
>>>>>>> master
