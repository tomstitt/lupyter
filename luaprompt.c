#include "lup.h"

int main(void) {
   lua_State *L = luaL_newstate();
   luaL_openlibs(L);
   init(L);

   size_t buf_size = 1024;
   char buf[buf_size];

   while (1) {
      printf("lua> ");
      fgets(buf, buf_size, stdin);
      char *r = process_chunk(L, buf);
      if (r) printf("%s\n", r);
      free(r);
   }

   lua_close(L);
   return 0;
}
