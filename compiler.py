
import sys
from os import listdir, remove
from os.path import join, isfile, sep, isdir, lexists, splitext

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


BASE_PATH = 'gclient'
sys.argv = [__file__, 'build_ext', '--inplace']

PY_FILE = '.py'
EXCLUDE_PY = '__init__.py'
EXT_FILES = ('.py', '.c', '.pyc')


def scanner(directory, _files=[]):
    for ent in listdir(directory):
        elm = join(directory, ent)
        path, ext = splitext(elm)
        if isfile(elm) and ext == PY_FILE and ent != EXCLUDE_PY:
            _files.append(path)
        elif isdir(elm):
            scanner(elm, _files)
    return _files


def make_extension(path):
    name = path.replace(sep, '.')
    path += PY_FILE
    return Extension(
        name,
        sources=[path],
        language="c",
        )

files = scanner(BASE_PATH)
extensions = [make_extension(entry) for entry in files]

setup(ext_modules=cythonize(extensions))

for entry in files:
    for ext in EXT_FILES:
        path = entry + ext
        if lexists(path):
            remove(path)
            print 'File deleted :: ' + path
