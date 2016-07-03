lua.root = ../
exe = lup
CFLAGS = -g -I$(lua.root)/src -L$(lua.root)/src -llua
CC = gcc

$(exe): $(exe).c
	$(CC) $(CFLAGS) $< -o $@
