#region TextureLoader
from OpenGL.GL import *
from PIL import Image
#endregion

class ShaderLoader:
    @staticmethod
    def load(path):
        result = ""
        with open(path, 'r') as f:
            line = f.readline()
            while line:
                result+=str(line)
                line = f.readline()
        return result

class TextureLoader:
    @staticmethod
    def load(path, texture):
        glBindTexture(GL_TEXTURE_2D, texture)
        
        # Set texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        # load image
        image = Image.open(path)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = image.convert("RGBA").tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        return texture
