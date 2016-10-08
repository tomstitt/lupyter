A Lua Kernel for iPython/Jupyter

Simple Lua Kernel + Prompt using python wrapped C.

Build the Python module:

    > python setup.py install

Add the Jupyter Kernel:

    > jupyter kernelspec install ../lupyter

**To use**

Launch the console (quitting is weird use ctrl-z):

    > jupyter console --kernel lupyter

Lanuch the browser:

    > jupyter notebook
