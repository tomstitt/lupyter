from distutils.core import setup, Extension

# this stuff could be system dependent
lup_ext_mod = Extension("lup",
                          sources=["src/lup.c", "src/_lup.c"],
#                          include_dirs=['/usr/local/include'],
                          libraries=['lua'],
                          #library_dirs=['/usr/local/lib']
                          )

setup(name="luypter", packages=['lupyter'], ext_modules=[lup_ext_mod])
