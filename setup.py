from distutils.core import setup, Extension

# this stuff could be system dependent
extension_mod = Extension("lup",
                          sources=["lup.c", "_lup.c"],
                          include_dirs=['/usr/local/include'],
                          libraries=['lua'],
                          library_dirs=['/usr/local/lib'])

setup(name="lup", ext_modules=[extension_mod])
