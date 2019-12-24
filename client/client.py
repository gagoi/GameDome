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
    message = "NC"+message+"\n"
    n = s.send(bytes(message, 'utf-8'))
    if (n != len(message )):
        print('Erreur envoi')
        return False

    while(1):
        r = s.recv(MAX)
        print(r)
        if r=="S":
            # LUNCH GAME
            break

    # t.sleep(3000000)
    print('Deconnexion.')
    s.close()


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
    return s,HOST,PORT

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



main()