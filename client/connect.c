//
// Created by apoupeney on 12/24/19.
//

#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#define MAX 80
#define MAX2 20
#define MAXIP 15



#define SA struct sockaddr

void username(char* buff){
    int n;
    bzero(buff, sizeof(buff));
    printf("Enter your username : ");
    n = 0;
    while ((buff[n++] = getchar()) != '\n');
    buff[strlen(buff)-1] = 0;
    //return buff;

}
void func(int sockfd)
{
    char buff[MAX];
    int n;
    for (;;) {
        bzero(buff, sizeof(buff));
        printf("Enter the string : ");
        n = 0;
        while ((buff[n++] = getchar()) != '\n')
            ;
        write(sockfd, buff, sizeof(buff));
        bzero(buff, sizeof(buff));
        read(sockfd, buff, sizeof(buff));
        printf("From Server : %s", buff);
        if ((strncmp(buff, "exit", 4)) == 0) {
            printf("Client Exit...\n");
            break;
        }
    }
}

void sendmg(int sockfd, const char* buff){
    write(sockfd, buff, sizeof(buff));
}
int main(int argc, char * argv[])
{
    if (argc != 3){
        printf("Usage : ./out [IP ADDRESS] [PORT]");
    }
    int PORT = atoi(argv[2]);
    int sockfd, connfd;
    struct sockaddr_in servaddr, cli;

    // socket create and varification
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        printf("socket creation failed...\n");
        exit(0);
    }
    else
        printf("Socket successfully created..\n");
    bzero(&servaddr, sizeof(servaddr));

    // assign IP, PORT
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = inet_addr(argv[1]);
    servaddr.sin_port = htons(PORT);

    // connect the client socket to server socket
    if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) {
        printf("Unable to connect with the server \n");
        exit(0);
    }
    else
        printf("You're now connected, enjoy ! \n");
        sendmg(sockfd, "NC");
        char pseudo[MAX2];
        username(pseudo);
        sendmg(sockfd, pseudo);
        //printf("Welcome %s ! \n", pseudo);

        char wait[MAX];
        bzero(wait, MAX);
        printf("Waiting for a new player...");
        // read the message from client and copy it in buffer
        read(sockfd, wait, sizeof(wait));
//        printf("From client: %s\t, buff);
    // function for chat
    //func(sockfd);

    // close the socket
    close(sockfd);
}

