// stitt

#define _POSIX_C_SOURCE 200809L
#define _BSD_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <signal.h>

#include "lup.h"

#define PORT 1234
#define BIND_FREQ 2

int blocking_process_chunk(lua_State *L, int sock) {
   size_t buffer_len = 1024;
   char buffer[buffer_len];
   ssize_t message_len;

   // blocking single-socket echo loop
   while ("one") {
      // if the request is empty do nothing
      if ((message_len = read(sock, buffer, buffer_len)) < 1) {
         if (message_len == 0) fprintf(stderr, "client is dead\n");
         else fprintf(stderr, "error on read: %s\n", strerror(errno));
         return 1;
      }
      buffer[message_len] = '\0';
      char *response = process_chunk(L, buffer);
      size_t response_length = 0;
      if (response) {
         response_length = strlen(response);
      }
      else {
         response = malloc(sizeof(char));
         response_length = 1;
         response[0] = '\0';
      }

      // try to write the response
      printf("writing to client, length is %zu\n", response_length);
      if (write(sock, response, response_length) != response_length) {
         free(response);
         fprintf(stderr, "error on write: %s\n", strerror(errno));
         return 2;
      }
      free(response);
   }

   return 0;
}


int luaserver() {
    struct sockaddr_in addr;
    int sock;

    // create listening socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        fprintf(stderr, "problem creating socket: %s", strerror(errno));
        return 1;
    }

    // setup address
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    // bind port
    while (1) {
      if (bind(sock, (const struct sockaddr *)&addr,
               sizeof(struct sockaddr_in)) == -1) {
         fprintf(stderr, "problem binding. trying again in %d seconds\n",
               BIND_FREQ);
         sleep(BIND_FREQ);
         continue;
      }
      printf("bind successful\n");
      break;
    }

    // start listening
    if (listen(sock, 2) == -1) {
        fprintf(stderr, "problem listening\n");
        close(sock);
        return 3;
    }

    // client address info
    int sock_client = -1;
    struct sockaddr_in addr_client;
    socklen_t len = sizeof(struct sockaddr_in);

   // create the Lua State
   lua_State *L = luaL_newstate();
   luaL_openlibs(L);
   init(L);

    // listen indefinitely on port PORT
    while (1) {
        if ((sock_client = accept(sock, (struct sockaddr *)&addr_client,
                    &len)) < 0 ) {
            fprintf(stderr, "bad client socket\n");
            close(sock);
        }
        // print when we get a connection
        fprintf(stderr, "got connection: [%s, %d]\n",
                inet_ntoa(addr_client.sin_addr), ntohs(addr_client.sin_port));

        if (blocking_process_chunk(L, sock_client)) {
           close(sock);
        }
    }

    // exit clean
    close(sock);
    lua_close(L);
    return 0;
}


int main(void) {
   return luaserver();
}
