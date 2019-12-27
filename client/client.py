# #!/usr/bin/python
# # -*- coding: utf-8 -*-

import socket
import curses
import time as t
import os

MAX = 20

# HOSTd = '127.0.0.1'
# PORTd = 8081
# HOSTd = '192.168.43.254'
# PORTd = 45703

rows, columns = os.popen('stty size', 'r').read().split()
rows, columns = int(rows), int(columns)
charcontour = "#"
charseparation = "|"


###### MORPION ########
class Morpion:
    chargrilleLg = "-"
    chargrilleCl = "|"
    tligne = 3
    tcolone = 5

    taillemin = 3 * tcolone + 2

    def __init__(self, stdscr, ml, dc):
        self.stdscr = stdscr
        self.ml = ml
        self.dc = dc
        self.maxc = 2* dc + self.taillemin

    def grilleV(self):


        # self.dc est le decallage des colones par rapport a 0
        L = [int(-(self.tligne + 1) / 2), int((self.tligne + 1) / 2)]
        for Ldec in L:
            for i in range(0, 5):
                self.stdscr.addstr(self.ml + Ldec, self.dc + i, self.chargrilleLg)
                self.stdscr.addstr(self.ml + Ldec, self.dc + i + 1 + self.tcolone, self.chargrilleLg)
                self.stdscr.addstr(self.ml + Ldec, self.dc + i + 2 + 2 * self.tcolone, self.chargrilleLg)

        C = [int(-(self.tcolone + 1) / 2), int((self.tcolone + 1) / 2)]
        self.mc = int(self.dc + (self.tcolone + 1) / 2 + self.tcolone)
        for Cdec in C:
            for j in range(0, 3):
                self.stdscr.addstr(self.ml + (int(-(self.tligne - 1) / 2 - 1 - self.tligne)) + j, self.mc + Cdec,
                                   self.chargrilleCl)
                self.stdscr.addstr(self.ml - (int((self.tligne - 1) / 2)) + j, self.mc + Cdec, self.chargrilleCl)
                self.stdscr.addstr(self.ml + self.tligne + j, self.mc + Cdec, self.chargrilleCl)



        return self.stdscr

    def affGr(self, G, play=False):
        posY = [int(self.dc + (self.tcolone - 1) / 2), int(1 + self.dc + (self.tcolone - 1) / 2 + self.tcolone),
                int(2 + self.dc + (self.tcolone - 1) / 2 + self.tcolone * 2)]
        posX = [int(self.ml + (int(-(self.tligne - 1) / 2 - 2 - (self.tligne - 1) / 2))),
                int(1 + self.ml + (int(-(self.tligne - 1) / 2 - 2 - (self.tligne - 1) / 2)) + self.tligne),
                int(2 + self.ml + (int(-(self.tligne - 1) / 2 - 2 - (self.tligne - 1) / 2)) + 2 * self.tligne)]
        for i in range(len(G)):
            self.stdscr.addstr(posX[i // 3], posY[i % 3], G[i].replace(' ', '.'))

        n = None
        Yin = int(2 + self.ml + (int(-(self.tligne - 1) / 2 - (self.tligne - 1) / 2)) + 3 * self.tligne)
        Xin = self.dc
        if play:

            # self.stdscr.addstr(Yin, Xin, "> Where to play: ")
            # curses.echo()
            self.stdscr.addstr(Yin, Xin, "> Where to play: ")
            curses.echo()

            stdscr.keypad(False)
            while (1):

                n = self.stdscr.getstr(Yin, Xin + 17, 1)
                if n == "h" or n =="H":
                    pass
                    #aff Help
                elif n == "q":
                    pass
                    #abandon
                if n.isdigit():
                    break;

            # curses.textpad.Textbox(self.stdscr)

            stdscr.keypad(True)
            curses.noecho()
        else:
            self.stdscr.addstr(Yin, Xin, "                   ")

        return self.stdscr, n


def morpion(s, stdscr, ml, l, c):
    M = Morpion(stdscr, ml, 7)
    if l > M.taillemin and c > M.taillemin:
        stdscr = M.grilleV()
        stdscr = chat(stdscr, M.maxc, l).stdscr

    while (1):
        r1 = s.recv(MAX).decode("utf-8")
        # print("recu: ", r, ";fiiiin ")
        if "GG" in r1:
            stdscr.addstr(3, 3, "WELL DONE")
            r(stdscr)
            return 0
        elif "L" in r1:
            stdscr.addstr(3, 3, "You loooose ....")
            # print("You loooose...")
            r(stdscr)
            return 0
        elif "E" in r1:
            stdscr.addstr(3, 3, "Equality")
            r(stdscr)
            # print("Equality")
            return 0
        elif "G" in r1:

            gr = r1.split('G')[1]
            if "T" in r1:
                gr = r1.split('G')[1].replace(' ', '.')
                stdscr, n = M.affGr(gr, True)

                n = "P" + n.decode("utf-8") + "\n"
                envoi(s, n)
            else:
                stdscr, n = M.affGr(gr, False)

        elif "T" in r1:
            r2 = s.recv(MAX).decode("utf-8")
            if "G" in r2:
                gr = r2.split('G')[1].replace(' ', '.')
                stdscr, n = M.affGr(gr, True)
                n = "P" + n.decode("utf-8") + "\n"
                envoi(s, n)

        else:
            return 0

        r(stdscr)


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
        for i in range(1, self.lmax):
            self.stdscr.addstr(i, self.c, self.charseparation)
        return self.stdscr

    def cht(self):
        self.stdscr.addstr(1, self.c + 2, "[XX] >>>")
        return self.stdscr


# i parcourt les colones
# j parcourt les lignes

def initscreen():
    curses.use_env(False)
    stdscr = curses.initscr()
    curses.resizeterm(rows, columns)
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    stdscr.keypad(True)
    l, c = stdscr.getmaxyx()
    l, c = l - 1, c - 1
    ml = int(l / 2)
    # stdscr = contour(stdscr,l,c)
    stdscr.border()
    return stdscr, l, c, ml

    # stdscr.addstr(curses.LINES-2,cols,"X")


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


def gettxt(stdscr, y, x, lenofstr, inputtext = ""):
    curses.echo()
    stdscr.keypad(False)
    while True:
        if len(inputtext) != 0:
            break
        else:
            inputtext = stdscr.getstr(y, x , lenofstr)
            r(stdscr)
    stdscr.keypad(True)
    curses.noecho()
    inputtext = inputtext.decode("utf-8")
    return inputtext


def addtext(stdsrc, y, x, text="", center=False):
    if center:
        stdscr.addstr(y, x - len(text) // 2, text)
    else:
        stdscr.addstr(y, x, text)
    r(stdscr)


def r(stdscr):
    stdscr.move(0, 0)
    stdscr.refresh()


class Menu:
    HOSTd = '2.3.130.203'
    PORTd = 45703

    def __init__(self, stdscr, y, x):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.connected = False
        self.items = ['> Connect', '> Games', '> Exit']
        self.gamesItems = ['> Morpion', '> Back to main menu']

        self.bienvenu()

    def bienvenu(self):
        text = " Hello "
        x = self.x // 2
        y = self.y // 2
        for k in range(7):
            self.stdscr.addstr(y, x - k - len(text) // 2, "-" * k + text + "-" * k)

            r(stdscr)
            t.sleep(0.2)
        textEnter = "Enter your username:"
        x = self.x // 2 - len(textEnter)//2
        addtext(stdscr, y + 1, x, textEnter)
        addtext(stdscr, y + 2, x, ">")
        u = gettxt(stdscr, y + 2, x + 1, 10)
        stdscr.clear()
        addtext(stdscr, y, x, "Welcome " + u + " !")
        self.nom = u
        t.sleep(0.5)

        # self.stdscr.addstr(y, x-k, " " *len("-"*k + text + "-"*k))

        self.menu()

    def connectedState(self):
        text = ">>> You are not connected <<<"
        h, w = stdscr.getmaxyx()
        x = w // 2
        y = h // 2
        if not self.connected:
            addtext(stdscr, 3, x, text, True)
        else:
            addtext(stdscr, 3, x, " " * len(text), True)

        if self.nom != "":
            addtext(stdscr, 4, x, "> Welcome " + self.nom + " <", True)

    def menu(self):
        current_row = 0
        self.print_menu(current_row)
        while 1:
            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.items) - 1:
                current_row += 1
            elif key == curses.KEY_RIGHT or key in [10, 13]:
                self.print_center(self.items[current_row])
                # self.stdscr.getch()
                # if user selected last row, exit the program
                if current_row == len(self.items) - 1:
                    break

            self.print_menu(current_row)

    def gamesMenu(self):
        current_row = 0
        self.print_gamesmenu(current_row)
        while 1:
            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.gamesItems) - 1:
                current_row += 1
            elif key == curses.KEY_RIGHT or key in [10, 13]:
                self.print_gamescenter(self.gamesItems[current_row])

                # self.stdscr.getch()
                # if user selected last row, exit the program
                if current_row == len(self.gamesItems) - 1:
                    break

            self.print_gamesmenu(current_row)

    def print_gamesmenu(self, selected_row_idx):
        self.stdscr.clear()
        self.connectedState()
        for idx, row in enumerate(self.gamesItems):
            h, w = stdscr.getmaxyx()
            x = w // 2 - len(row) // 2
            y = h // 2 - len(self.gamesItems) // 2 + 2 * idx
            if idx == selected_row_idx:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        r(self.stdscr)

    def print_gamescenter(self, text):

        stdscr.clear()
        h, w = stdscr.getmaxyx()
        x = w // 2
        y = h // 2

        if text == self.gamesItems[-1]:
            return 0
        elif text == "> Morpion":
            if self.connected:
                envoi(self.s, "M\n")
                addtext(stdscr,y,x, "En attente d'autre joueur...", True)
                wait(self.s, 'S')
                stdscr.clear()
                morpion(self.s, stdscr, y, h,w)
            else:
                addtext(stdscr, y, x, "You must be connected to the server to play", True)
                self.stdscr.getch()
                return 0
        r(self.stdscr)

    def print_center(self, text):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        x = w // 2
        y = h // 2

        if text == self.items[-1]:
            addtext(self.stdscr, y, x, "Bye !", True)
            self.stdscr.getch()
        elif text == "> Connect":
            self.mconnect()
        elif text == "> Games":
            self.gamesMenu()
        else:
            text = "You selected " + text
        h, w = stdscr.getmaxyx()
        x = w // 2
        y = h // 2
        r(self.stdscr)

    def minitConnect(self, first = True):
        txt =  "Enter server hostname (default" + str(self.HOSTd) + ")"
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(txt) // 2
        y = h // 2 - 3
        if not first:
            addtext(stdscr, y - 3, x, "/!\ Unable to connect, try again")
            addtext(stdscr, y + 1, x, " "* 16)
            addtext(stdscr, y + 4, x, " "* 10)

        addtext(stdscr, y-2, x, "Enter \'quit\' to exit this menu")
        addtext(stdscr, y , x, txt)
        addtext(stdscr, y+3 , x ,"Enter server port (default" + str(self.PORTd) + ")")

        addtext(stdscr, y+1, x, ">")
        HOST = gettxt(stdscr, y + 1, x + 1, 15)
        if HOST == " ":
            HOST = self.HOSTd
        elif "quit" in HOST:
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM), HOST, None
        addtext(stdscr, y + 4, x, ">")
        PORT = gettxt(stdscr, y + 4, x + 1, 6)

        if PORT == " ":
            PORT = self.PORTd
        else:
            if "quit" not in PORT and PORT.isdigit():
                PORT = int(PORT)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s, HOST, PORT

    def mconnect(self):
        stdscr.clear()
        s, HOST, PORT = self.minitConnect()
        while (True):
            addtext(stdscr,2,2, HOST + " "+str(PORT))
            try:
                s.connect((HOST, PORT))
                break
            except:
                if "quit" in HOST:
                    return 0
                if isinstance(PORT, str):
                    if "quit" in PORT:
                        return 0
                s, HOST, PORT = self.minitConnect(False)

        self.s, self.HOST, self.PORT = s, HOST, PORT
        self.connected = True
        envoi(self.s, "NC" + self.nom + "\n")
        return 0

    def print_menu(self, selected_row_idx):
        self.stdscr.clear()
        self.connectedState()
        for idx, row in enumerate(self.items):
            h, w = stdscr.getmaxyx()
            x = w // 2 - len(row) // 2
            y = h // 2 - len(self.items) // 2 + 2 * idx
            if idx == selected_row_idx:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        r(self.stdscr)


if __name__ == "__main__":
    stdscr, l, c, ml = initscreen()
    mu = Menu(stdscr, l, c)

    # stdscr.addstr()
    # r(stdscr)
    #
    # print("[--  Hello  --]")
    # s = connection()
    # print("You are now connected, enjoy !\n")
    # message = input('Enter your username: ')
    # message = "NC" + message + "\n"
    # envoi(s, message)
    #
    # envoi(s, "M\n")
    # wait(s, 'S')
    #
    # morpion(s, stdscr, ml, l, c)
    #
    # t.sleep(5)
    endscreen(stdscr)
    # t.sleep(3000000)
    # print('Deconnexion.')
    # s.close()
