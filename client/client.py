import socket
import curses
import time as t
import os

MAX = 20
HOSTd = '2.3.130.203'
PORTd = 45703
# HOSTd = '127.0.0.1'
# PORTd = 8081
# HOSTd = '192.168.43.254'
# PORTd = 45703

rows, columns = os.popen('stty size', 'r').read().split()
rows,columns = int(rows), int(columns)
charcontour = "#"
charseparation= "|"

###### MORPION ########
class Morpion:
    chargrilleLg="-"
    chargrilleCl="|"
    tligne = 3
    tcolone = 5

    taillemin = 3*tcolone + 2




    def __init__(self,stdscr,ml,dc):
        self.stdscr = stdscr
        self.ml = ml
        self.dc = dc
        self.maxc = 2*dc + self.taillemin


    def grilleV(self):

        #self.dc est le decallage des colones par rapport a 0
        L=[int(-(self.tligne+1)/2),int((self.tligne+1)/2)]
        for Ldec in L:
            for i in range(0,5):
                self.stdscr.addstr(self.ml+Ldec,self.dc+i, self.chargrilleLg)
                self.stdscr.addstr(self.ml+Ldec,self.dc+i+1+self.tcolone, self.chargrilleLg)
                self.stdscr.addstr(self.ml+Ldec,self.dc+i+2+2*self.tcolone, self.chargrilleLg)

        C = [int(-(self.tcolone + 1) / 2), int((self.tcolone + 1) / 2)]
        self.mc = int(self.dc+(self.tcolone + 1) / 2+self.tcolone)
        for Cdec in C:
            for j in range(0,3):
                self.stdscr.addstr(self.ml+(int(-(self.tligne-1)/2-1-self.tligne))+j, self.mc+Cdec, self.chargrilleCl)
                self.stdscr.addstr(self.ml-(int((self.tligne-1)/2))+j, self.mc+Cdec, self.chargrilleCl)
                self.stdscr.addstr(self.ml+self.tligne+j, self.mc+Cdec, self.chargrilleCl)
        return self.stdscr

    def affGr(self, G, play = False):
        posY=[int(self.dc+(self.tcolone - 1) / 2), int(1+self.dc+(self.tcolone - 1) / 2 + self.tcolone), int(2+self.dc+(self.tcolone - 1) / 2 + self.tcolone*2)]
        posX=[int(self.ml+(int(-(self.tligne-1)/2-2-(self.tligne-1)/2))),int(1+self.ml+(int(-(self.tligne-1)/2-2-(self.tligne-1)/2))+self.tligne), int(2+self.ml+(int(-(self.tligne-1)/2-2-(self.tligne-1)/2))+2*self.tligne) ]
        for i in range(len(G)):
            self.stdscr.addstr(posX[i//3], posY[i%3], G[i].replace(' ', '.'))

        n = None
        Yin = int(2 + self.ml + (int(-(self.tligne - 1) / 2 - (self.tligne - 1) / 2)) + 3 * self.tligne)
        Xin = self.dc
        if play:


            # self.stdscr.addstr(Yin, Xin, "> Where to play: ")
            # curses.echo()
            self.stdscr.addstr(Yin, Xin, "> Where to play:   ")
            curses.echo()
            while (1):
                n = self.stdscr.getstr(Yin, Xin + 17, 15)
                if n.isdigit():
                    break;

            # curses.textpad.Textbox(self.stdscr)
            curses.noecho()
        else:
            self.stdscr.addstr(Yin, Xin, "                   ")

        return self.stdscr, n

def morpion(s, stdscr, ml, l ,c):

    M = Morpion(stdscr, ml, 3)
    if l > M.taillemin and c > M.taillemin:
        stdscr = M.grilleV()
        stdscr = chat(stdscr, M.maxc, l).stdscr




    while (1):
        r = s.recv(MAX).decode("utf-8")
        # print("recu: ", r, ";fiiiin ")
        if "GG" in r:
            stdscr.addstr(3, 3, "WELL DONE")
            stdscr.refresh()
            return 0
        elif "L" in r:
            stdscr.addstr(3, 3, "You loooose ....")
            # print("You loooose...")
            stdscr.refresh()
            return 0
        elif "E" in r:
            stdscr.addstr(3, 3, "Equality")
            stdscr.refresh()
            # print("Equality")
            return 0
        elif "G" in r:

            gr = r.split('G')[1]
            if "T" in r:
                gr = r.split('G')[1].replace(' ','.')
                stdscr, n = M.affGr(gr, True)


                n = "P" + n.decode("utf-8") + "\n"
                envoi(s, n)
            else:
                stdscr, n = M.affGr(gr, False)

        elif "T" in r:
            r2 = s.recv(MAX).decode("utf-8")
            if "G" in r2:
                gr = r2.split('G')[1].replace(' ', '.')
                stdscr, n = M.affGr(gr, True)
                n = "P" + n.decode("utf-8") + "\n"
                envoi(s, n)

        else:
            return 0

        stdscr.refresh()


###### CHAT ########
class chat:
    charseparation = "|"

    def __init__(self, stdscr, c, lmax):
        self.c = c
        self.lmax = lmax
        self.stdscr = stdscr
        self.stdscr = self.separation()
        self.stdscr = self.cht()

    def separation(self):
        for i in range(1,self.lmax):
            self.stdscr.addstr(i, self.c, self.charseparation)
        return self.stdscr

    def cht(self):
        self.stdscr.addstr(1,self.c +2, "[XX] >>>")
        return self.stdscr


# i parcourt les colones
# j parcourt les lignes

def initscreen():
    curses.use_env(False)
    stdscr = curses.initscr()
    curses.resizeterm (rows,columns)
    curses.noecho()
    curses.cbreak()
    # stdscr.keypad(True)
    l,c = stdscr.getmaxyx()
    l,c = l-1,c-1
    ml = int(l/2)
    #stdscr = contour(stdscr,l,c)
    stdscr.border()
    return stdscr,l,c,ml

    #stdscr.addstr(curses.LINES-2,cols,"X")
def endscreen(stdscr):
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    curses.endwin()


def wait(s, c):
    while (1):
        r = s.recv(MAX).decode("utf-8")
        # print(r)
        if c in r:
            return r
def envoi(s, message, test=True):
    if test:
        n = s.send(bytes(message, 'utf-8'))
    else:
        n = s.send(message)
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

        # print(HOST, PORT)
        try:
            s.connect((HOST, PORT))
            break
        except:
            print("Unable to connect, try again")
            HOST = HOSTd
            PORT = PORTd
            s, HOST, PORT = initConnect()

    return s



def main():
    print("[--  Hello  --]")
    s = connection()
    print("You are now connected, enjoy !\n")
    message = input('Enter your username: ')
    message = "NC" + message + "\n"
    envoi(s, message)

    envoi(s, "M\n")
    wait(s, 'S')

    stdscr, l, c, ml = initscreen()
    morpion(s, stdscr, ml, l, c)

    t.sleep(5)
    endscreen(stdscr)
    # t.sleep(3000000)
    # print('Deconnexion.')
    s.close()
main()
