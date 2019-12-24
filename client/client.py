import socket
import time as t

MAX = 20
HOSTd = '2.3.130.203'
PORTd = 45703


# HOSTd = '127.0.0.1'
# PORTd = 8081
# HOSTd = '192.168.43.254'
# PORTd = 45703

def main():
    print("[--  Hello  --]")
    s = connection()
    print("You are now connected, enjoy !\n")
    message = input('Enter your username: ')
    message = "NC" + message + "\n"
    envoi(s, message)

    envoi(s, "M\n  ")
    wait(s, 'S')
    morpion(s)

    # t.sleep(3000000)
    print('Deconnexion.')
    s.close()


def envoi(s, message):
    n = s.send(bytes(message, 'utf-8'))
    if (n != len(message)):
        print('Erreur envoi')
        return False


def initConnect():
    HOST = input("Enter server host (default" + HOSTd + "): ")
    if HOST == "":
        HOST = HOSTd
    PORT = input("Enter server port (default" + str(PORTd) + "): ")
    if PORT == "":
        PORT = PORTd
    else:
        PORT = int(PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # s.connect(HOST, PORT)
    return s, HOST, PORT


def connection():
    s, HOST, PORT = initConnect()
    while (True):

        print(HOST, PORT)
        try:
            s.connect((HOST, PORT))
            break
        except:
            print("Unable to connect, try again")
            s = initConnect()
    return s


def wait(s, c):
    while (1):
        r = s.recv(MAX).decode("utf-8")
        print(r)
        if c in r:
            return r


def morpion(s):
    while (1):
        r = s.recv(MAX).decode("utf-8")
        print("recu: ",r)
        if "GG" in r:
            print("Well done!")
            return 0;
        if "L" in r:
            print("You loooose...")
            return 0;
        elif "G" in r:
            if "T" in r:
                grilleMor(r[2:] + "\n")
                n = input("Your turn, where to play: ")
                n = "P" + str(n) + "\n"
                envoi(s, n)
            else:
                grilleMor(r[2:] + "\n")


        elif "T" in r:
            r2 = s.recv(MAX).decode("utf-8")
            print("recu: ", r2)
            grilleMor(r2[1:])
            n=""
            n = input("Your turn, where to play: ")
            n = "P" + str(n) + "\n"
            print(n)
            envoi(s, n)





def grilleMor(g):
    print(g[:3])
    print("-----")
    print(g[4:6])
    print("-----")
    print(g[7:9])

main()
