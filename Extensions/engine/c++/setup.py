from distutils.core import setup, Extension

module = Extension("myModule", sources=["example.c"])

setup(name="PackageName",
        version="1.0",
        description="Package for myModule",
        ext_modules=[module])