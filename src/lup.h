#ifndef LUP
#define LUP

#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *process_chunk(lua_State *L, const char *chunk);
void init(lua_State *L);

#endif
