from distutils.core import setup, Extension
import os
import sys
import fnmatch

distname = "lupyter"
interface_name = "c_interface"
lua_dir = "/usr/local"
prefer = "lua"

if "LUA_DIR" in os.environ:
    lua_dir = os.environ["LUA_DIR"]

if not os.path.exists(lua_dir):
    sys.exit("fatal: {} doesn't exist, please set LUA_DIR to a Lua install root")


def find_lua(root):
    include = os.path.join(root, "include")
    libdir = os.path.join(root, "lib")
    if not os.path.exists(os.path.join(include, "lua.h")):
        return None
    if not os.path.exists(os.path.join(libdir, "liblua.a")):
        return None

    return {"name": "lua", "include": include, "libdir": libdir, "lib": "lua"}


def find_luajit(root):
    include_root = os.path.join(root, "include")
    if not os.path.exists(include_root):
        return None
    for f in os.listdir(include_root):
        if fnmatch.fnmatch(f, "luajit*"):
            include = os.path.join(include_root, f)
            if os.path.isdir(include):
                if os.path.exists(os.path.join(include, "lua.h")):
                    break
    else:
        return None

    libdir = os.path.join(root, "lib")
    if not os.path.exists(libdir):
        return None
    for f in os.listdir(libdir):
        if fnmatch.fnmatch(f, "libluajit*.a"):
            lib = f[3:-2]
            break
    else:
        return None

    return {"name": "luajit", "include": include, "libdir": libdir, "lib": lib}


info = find_lua(lua_dir)
if info is None:
    info = find_luajit(lua_dir)

if info is None:
    sys.exit("fatal: unable to find Lua in {}, please set LUA_DIR to a valid install root".format(lua_dir))
else:
    print("found {}".format(info["name"]))

lup_ext_mod = Extension("{}.{}".format(distname, interface_name),
    sources=["{}/{}/lup.c".format(distname, interface_name)],
    include_dirs=[info["include"]],
    libraries=[info["lib"]],
    library_dirs=[info["libdir"]])

setup(name=distname,
    version="1.0",
    packages=[distname],
    ext_modules=[lup_ext_mod])
