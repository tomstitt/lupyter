# A Lua Kernel for Jupyter

Lupyter is a Lua kernel built on [ipykernel](https://github.com/ipython/ipykernel).
Tab-completion is available but documentation lookup is still a work in progress.

## Installing

In most cases it's enough to `pip install` with `LUA_DIR` pointing
to your Lua installation but if Lua is installed
in your `PATH` you may not need `LUA_DIR`. You can always add
`-v` after `pip install` if your Lua install isn't found and you
want to see a list of the directories searched.

```
[LUA_DIR=/path/to/your/lua_root] pip install .
```

If your Python is in a weird place the kernelspec might not be
visible to Jupyter.

You can confirm that the kernelspec was install correctly with:

```
jupyter kernelspec list
```

If the kernelspec isn't in the list check which paths Jupyter can see
and make sure your kernelspec was installed to one of them:

```
jupyter --paths
```

You can manually install to one of those paths with:

```
jupyter kernelspec install data_kernelspec --name lupyter --prefix ...
```
