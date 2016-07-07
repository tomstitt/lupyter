A Lua Kernel for iPython/Jupyter

Simple Lua Kernel + Prompt using python wrapped C.

Build the Python module:

    > python setup.py install

Add the Jupyter Kernel:

    > jupyter kernelspec install ../lupyter

*Unless you have luakernel.py in your python path make sure you run the 
following in the same directory as this file.*

Launch the console:

    > jupyter console --kernel lupyter

Lanuch the browser:

    > jupyter notebook
