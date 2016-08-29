lua.root = ./lua/install
exe = luaserver
Cflags = -g
Iflags = -I$(lua.root)/include
Lflags = -L$(lua.root)/lib -llua

CC = cc

.PHONY: clean 

source = $(shell $(find . -depth 1 -name "*.c"))

objects = lup.o luaserver.o

%.o: %.c; $(CC) $(Cflags) $(Iflags) -c $< -o $@

$(exe): $(objects); $(CC) $(Cflags) $(Lflags) $^ -o $@

clean: ;rm -rf $(exe) $(exe).dSYM *.o
