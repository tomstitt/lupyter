# A Lua Kernel for Jupyter

Lupyter is a Lua kernel based on ipykernel.
Tab-complete is available but documentation lookup is still a work in progress.

## Installing

In most cases it's enough to `pip install` while specifying your
lua root if it isn't in your path.

```
[LUA_DIR=/path/to/your/lua_root] pip install .
```

If your Python is in a weird place the kernelspec might not be
visible to Jupyter.

You can confirm that the kernelspec was install correctly with:

```
jupyter kernelspec list
```

If the kernelspec isn't there check which paths Jupyter can see:

```
jupyter --paths
```

You can install manually to one of those paths with:

```
jupyter kernelspec install data_kernelspec --name lupyter --prefix ...
```
