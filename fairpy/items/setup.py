from setuptools import setup, Extension
import numpy as np

# define the extension module
ext_module = Extension(
    "cy_compensation_procedure", # name of the module
    ["cy_compensation_procedure.pyx"], # list of .pyx files
    include_dirs=[np.get_include()], # include the NumPy header files
    extra_compile_args=["-O3"], # optimize for performance
)

# setup the package
setup(
    name="fairpy", # name of the package
    version="1.0.0", # version of the package
    ext_modules=[ext_module], # list of extension modules to build
)
