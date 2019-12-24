#include "client.h"


int main()
{
    int stop = 0;
    grid_t morpion;

    init_grid(&morpion);

    morpion.val[1][0] = P1_TOKEN;

    initscr();
    while (!stop)
    {
        draw(&morpion);
        if (getch() == 'q')
            stop = 1;
    }
    endwin();
    return 0;
}

void draw(grid_t * grid)
{
    int y_pos[3] = {COLS / 2 - 2, COLS / 2, COLS / 2+ 2};
    int x_pos[3] = {LINES / 2 - 2, LINES / 2, LINES / 2 + 2};
    int i, j;
    
    clear();
    for (i = 0; i < 3; ++i)
    {
        for (j = 0; j < 3; ++j)
        {
            mvaddch(x_pos[i], y_pos[j], grid->val[i][j]);
        }
    }

    refresh();
}

void init_grid(grid_t * grid)
{
    unsigned int i;
    for (i = 0; i < 3; ++i)
    {
        memset(grid->val[i], P2_TOKEN, 3 * sizeof(char));
    }
}