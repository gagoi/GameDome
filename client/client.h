#ifndef CLIENT_H__
#define CLIENT_H__

#include <ncurses.h>
#include <string.h>

#define P1_TOKEN 'X'
#define P2_TOKEN 'O'

typedef struct {
    char val[3][3];
} grid_t;


void draw(grid_t * grid);
void init_grid(grid_t * grid);

#endif