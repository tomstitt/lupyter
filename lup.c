#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

const char *stringify = "stringify_args";


int stringify_args(lua_State *L) {
   luaL_Buffer B;
   luaL_buffinit(L, &B);

   int top = lua_gettop(L);
   for (int i = 1; i <= top; i++) {
      if (lua_isnil(L, i)) {
         luaL_addstring(&B, "nil");
      }
      else {
         // gross
         // because lua_tostring blows
         lua_getglobal(L, "tostring");
         lua_pushvalue(L, i);
         if (lua_pcall(L, 1, 1, 0) != 0) {
            printf("fail\n");
            exit(1);
         }
         const char *str = lua_tostring(L, -1);
         size_t str_len = strlen(str);
         char t[str_len + 1];
         memcpy(t, str, str_len + 1);
         lua_pop(L, 1);
         luaL_addstring(&B, t);
      }
      if (i < top) {
         luaL_addchar(&B, '\t');
      }
   }
   luaL_pushresult(&B);
   printf("tostring is: '%s'\n", lua_tostring(L, -1));
   return 1;
}


char *process_chunk(lua_State *L, const char *chunk) {
   char *c = NULL;
   lua_pushfstring(L, "%s(%s)", stringify, chunk);
   luaL_loadstring(L, lua_tostring(L, -1));
   if (lua_pcall(L, 0, 1, 0) != 0) {
      lua_settop(L, 0);
      if (luaL_dostring(L, chunk) != 0) {
         const char *error = lua_tostring(L, -1);
         size_t error_len = strlen(error);
         c = (char*)malloc(error_len * sizeof(char));
         memcpy(c, error, error_len);
      }
      else {
          // pass
          // is there anyway this could be a string
          // to return?
      }
   }
   else {
      const char *res = lua_tostring(L, -1);
      if (res != NULL) {
         size_t res_len = strlen(res);
         c = (char*)malloc(res_len + 1);
         memcpy(c, res, res_len + 1);
      }
   }
   lua_settop(L, 0);

   return c;
}


int main(void) {
   lua_State *L = luaL_newstate();
   luaL_openlibs(L);
   size_t buf_size;
   char buf[1024];

   lua_register(L, stringify, stringify_args);
   while (1) {
      printf("lua> ");
      gets(buf);
      char *r = process_chunk(L, buf);
      printf("%s\n", r);
      free(r);
   }

   lua_close(L);
   return 0;
}
