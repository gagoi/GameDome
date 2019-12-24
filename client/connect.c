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

int initconnect(int argc, char * argv[])
{   char buffer[200],texte[200];
    int port, rc, sock,i,c;
    struct sockaddr_in addr;
    struct hostent *entree;
    if (argc !=3)  {
        printf("usage : ./out nom_serveur port\n"); exit(1);
    }
    addr.sin_port=htons(atoi(argv[2]));
    addr.sin_family=AF_INET;
    entree=(struct hostent *)gethostbyname(argv[1]);
    bcopy((char *)entree->h_addr,(char *)&addr.sin_addr,entree->h_length);
    sock= socket(AF_INET,SOCK_STREAM,0);
    if (connect(sock, (struct sockaddr *)&addr,sizeof(struct sockaddr_in)) < 0) {
        printf("probleme connexion\n");
        exit(1); }
    printf("connexion passe\n");
    bzero(texte,sizeof(texte));
    bzero(buffer,sizeof(buffer));
    i = 2;
    texte[0]='N';texte[1]='C';
    printf("You're now connected, enjoy ! \n");

    printf("Enter your username: ");
    while((c=getchar()) != '\n') texte[i++]=c;

    int a;
    a = send(sock,texte,strlen(texte)+1,0);

    if(a>0){
        printf("%s, %d, %d\n", texte, strlen(texte)+1, a);
    }
    printf("%d\n", sock);

    return sock;
//    int b;
//    b = recv(sock,buffer,sizeof(buffer),0);
//    if(a>0){
//        printf("%s, %d, %d\n", buffer, sizeof(buffer),b);
//    }
//    recv(sock,buffer,sizeof(buffer),0);
//    if (strncmp("S",buffer,1) == 0) return sock;

//    close(sock);
}
//int initconnect(int argc, char * argv[])
//{
//    if (argc != 3){
//        printf("Usage : ./out [IP ADDRESS] [PORT]\n");
//        exit(0);
//    }
//    int PORT = atoi(argv[2]);
//    int sockfd, connfd;
//    struct sockaddr_in servaddr, cli;
//
//    // socket create and varification
//    sockfd = socket(AF_INET, SOCK_STREAM, 0);
//    if (sockfd == -1) {
//        printf("socket creation failed...\n");
//        exit(0);
//    }
//    else
//        printf("Socket successfully created..\n");
//    bzero(&servaddr, sizeof(servaddr));
//
//    // assign IP, PORT
//    servaddr.sin_family = AF_INET;
//    servaddr.sin_addr.s_addr = inet_addr(argv[1]);
//    servaddr.sin_port = htons(PORT);
//
//    // connect the client socket to server socket
//    if (connect(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0) {
//        printf("Unable to connect with the server \n");
//        exit(0);
//    }
//    else{
//        printf("You're now connected, enjoy ! \n");
//        char NC[3];
//        NC[0] = 'N';
//        NC[1] = 'C';
//        NC[2] = '\0';
//        send(sockfd, NC, strlen(NC)+1, 0);
//        fsync(sockfd);
//        char pseudo[MAX2];
//        username(pseudo);
//        send(sockfd, pseudo, strlen(pseudo)+1, 0);
//
////        fsync(sockfd);
//        printf("Welcome %s ! \n", pseudo);
//
//
//        printf("Waiting for a new player...\n");}
////        char wait[MAX];
////        bzero(wait, MAX);
////        read(sockfd, wait, sizeof(wait));
////        printf("jai  recu: %s", wait);
//
//
//
//
//
//        // read the message from client and copy it in buffer
////        for(;;){
////            char wait[MAX];
////            bzero(wait, MAX);
////            read(sockfd, wait, sizeof(wait));
////            if (strncmp("S", wait,1)){
////                return sockfd;
////            }
////
////        }
//
////        printf("From client: %s\t, buff);
//    // function for chat
//    //func(sockfd);
//
//    // close the socket
//    //close(sockfd);
//}

