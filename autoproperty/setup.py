from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        "light_autoproperty",
        ["autoproperty/light_autoproperty.pyx"],
        language="c++",
    )
]

setup(
    name="light_autoproperty",
    ext_modules=cythonize(extensions, compiler_directives={
        'language_level': 3,
        'boundscheck': False,
        'wraparound': False,
        'initializedcheck': False,
        'nonecheck': False,
    }),
    zip_safe=False,
)