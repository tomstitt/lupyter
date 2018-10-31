from distutils.core import setup, Extension
import os

distname = "lupyter"
lua_dir = "/usr/local/include"

if 'LUA_DIR' in os.environ:
    lua_dir = os.environ['LUA_DIR']

# try to build the lua include and lib dir
lua_include_dir = os.path.join(lua_dir, 'include')
lua_lib_dir = os.path.join(lua_dir, 'lib')

if not os.path.exists(lua_include_dir) or not os.path.exists(lua_lib_dir):
    print("fatal: invalid lua path {}".format(lua_dir))

lup_ext_mod = Extension("lup",
    sources=["src/lup.c"],
    include_dirs=[lua_include_dir],
    libraries=['lua'],
    library_dirs=[lua_lib_dir])

setup(name=distname,
    version="1.0",
    packages=[distname],
    ext_modules=[lup_ext_mod])
