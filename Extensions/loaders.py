#region TextureLoader
from OpenGL.GL import *
from pygame import image, transform
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
    def load(img, texture):
        glBindTexture(GL_TEXTURE_2D, texture)

        # Set texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # Set texture filtering parameters, bylo tu GL_LINEAR 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        # load image
        img = transform.flip(img, False, True)
        img_width, img_height = img.get_rect().size
        img_data = image.tostring(img, "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_width, img_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
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