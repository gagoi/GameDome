#include "client.h"
#include "connect.h"


#define MAX 80

void play(char* buff){
    int n;
    bzero(buff, sizeof(buff));
    printf("Where to play: ");
    n = 0;
    while ((buff[n++] = getchar()) != '\n');
    buff[strlen(buff)-1] = 0;
    //return buff;

}
int main(int argc, char * argv[])
{
    int sock;
    sock = initconnect(argc, argv);
    printf("%d\n", sock);
//    char buffer[MAX];
//    bzero(buffer,sizeof(buffer));
//    int b;
//    b = recv(sock,buffer,sizeof(buffer),0);
//    if(b>0){
//        printf("%s, %d, %d\n", buffer, sizeof(buffer),b);
//    }
    int stop = 0;
    grid_t morpion;
    init_grid(&morpion);
    //morpion.val[1][0] = P1_TOKEN;
    initscr();
    char buff[10];
    char test = 'a';

    while (!stop)
    {

        draw(&morpion);
        char c = getch();
        if (c == 'q')
            stop = 1;
        else {
            mvaddch(10, 10, test);
            refresh();
        }
        test ++;

        //play(buff)


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
        memset(grid->val[i], ' ', 3 * sizeof(char));
    }
}