import setuptools
import os
import sys
import fnmatch
import re

distname = "lupyter"
description = "A Lua Jupyter Kernel using ipykernel"

here = os.path.abspath(os.path.dirname(__file__))
interface_name = "clua"
lua_dir = "/usr/local"
prefer = "lua"

if "LUA_DIR" in os.environ:
    lua_dir = os.environ["LUA_DIR"]
if not os.path.exists(lua_dir):
    sys.exit(f"fatal: {lua_dir} doesn't exist, please set LUA_DIR to a Lua install root")


def get_lua_release(path):
    with open(path) as f:
        version = re.findall(r"#define LUA_RELEASE.*\"Lua ([0-9\. ]+)", f.read())[0]
    return version


def get_kernel_name(name):
    return name.lower().replace(" ", "_").replace(".", "_")


def find_lua(root):
    include = os.path.join(root, "include")
    libdir = os.path.join(root, "lib")
    if not os.path.exists(os.path.join(include, "lua.h")):
        return None
    if not os.path.exists(os.path.join(libdir, "liblua.a")):
        return None
    version = get_lua_release(os.path.join(include, "lua.h"))
    name = "Lua " + version

    return {"display_name": name,
            "kernel_name": get_kernel_name(name),
            "version": version,
            "include": include,
            "libdir": libdir,
            "static_lib_path": os.path.join(libdir, "liblua.a"),
            "lib": "lua"}


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
            static_lib_path = os.path.join(libdir, f)
            break
    else:
        return None

    lua_version = get_lua_release(os.path.join(include, "lua.h"))
    name = "LuaJIT"
    with open(os.path.join(include, "luajit.h")) as f:
        luajit_version = re.findall(r"#define LUAJIT_VERSION.*\"LuaJIT ([0-9\. ]+)", f.read())[0]
        name = "LuaJIT " + luajit_version

    return {"display_name": name,
            "kernel_name": get_kernel_name(name),
            "version": lua_version,
            "luajit_version": luajit_version,
            "include": include,
            "libdir": libdir,
            "static_lib_path": static_lib_path,
            "lib": lib}


info = find_lua(lua_dir) or find_luajit(lua_dir)

if info is None:
    sys.exit(f"fatal: unable to find Lua in {lua_dir}, please set LUA_DIR to a valid install root")
else:
    print("found lua:")
    for k,v in info.items():
        print(f"  {k}: {v}")

with open(os.path.join(distname, "versions.py"), "w") as f:
    fstr = f'lua_version = "{info["version"]}"'
    if "luajit_version" in info:
        fstr += f'\nluajit_version = "{info["luajit_version"]}"'
    f.write(fstr)

lup_ext_mod = setuptools.Extension(f"{distname}.{interface_name}",
    sources=[f"{distname}/{interface_name}/lup.c"],
    include_dirs=[info["include"]],
    extra_objects=[info["static_lib_path"]])
    #libraries=[info["lib"]],
    #library_dirs=[info["libdir"]])

setup_args = dict(name=distname,
    description=description,
    url="https://github.com/tomstitt/lupyter",
    license="MIT",
    version="1.0.0",
    packages=setuptools.find_packages(),
    ext_modules=[lup_ext_mod],
    install_requires=["ipykernel", "jupyter_core"])


# Inspired by https://github.com/ipython/ipykernel/blob/master/setup.py
if any(arg.startswith(("bdist", "install")) for arg in sys.argv):
    from ipykernel.kernelspec import write_kernel_spec
    from jupyter_core.paths import jupyter_path
    from glob import glob
    import shutil

    kernelspec_dir = "data_kernelspec"
    dest = os.path.join(here, kernelspec_dir)
    if os.path.exists(dest):
        shutil.rmtree(dest)

    argv = [sys.executable, "-m", f"{distname}.luakernel", "-f", "{connection_file}"]
    write_kernel_spec(dest, overrides={
        "argv": argv,
        "display_name": info["display_name"],
        "language": "lua"
    })

    possible_kernel_dirs = jupyter_path()
    search_dir = os.path.join(sys.prefix, "share", "jupyter")
    if search_dir not in possible_kernel_dirs:
        print(f"The target kernel directory ({search_dir}) will not be picked up by Jupyter, "
              f"please manually install {kernelspec_dir} with: ")
        print(f"jupyter-kernelspec install {kernelspec_dir} --sys-prefix --name {info['kernel_name']}")
    else:
        setup_args["data_files"] = [
            (
                os.path.join("share", "jupyter", "kernels", info["kernel_name"]),
                glob(os.path.join(kernelspec_dir, "*"))
            )
        ]
        print(setup_args["data_files"])

setuptools.setup(**setup_args)
