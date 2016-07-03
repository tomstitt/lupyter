lua.root = ..
exe = lup
CFLAGS = -g -I$(lua.root)/src -L$(lua.root)/src -llua
CC = gcc

.PHONY: clean

$(exe): $(exe).c
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -rf $(exe) $(exe).dSYM
