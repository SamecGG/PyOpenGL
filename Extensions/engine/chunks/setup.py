from distutils.core import setup, Extension
from Cython.Build import cythonize
import numpy

module = Extension("chunks", 
sources=['chunks_cy.pyx'],
include_dirs=[numpy.get_include()])

print(numpy.get_include())

setup(name="Chunks",
        version="1.0",
        description="Chunk generation and manipulation",
        ext_modules=cythonize([module]))