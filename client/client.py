# #!/usr/bin/python
# # -*- coding: utf-8 -*-

import socket
import curses
import time as t
import os

autoc = True
anim = False
MAX = 40
import os

cwd = os.getcwd()

fconfig = cwd + "/.GamesDomeUSR.txt"

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
    help = False
    valide = [k for k in range(9)]

    def __init__(self, stdscr, ml, dc):
        self.stdscr = stdscr
        self.ml = ml
        self.dc = dc
        self.maxc = 2 * dc + self.taillemin

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

    def affHgr(self, Y, X, lenofGr):
        if self.help:
            self.help = False
            for i in range(lenofGr):
                self.stdscr.addstr(Y[i // 3] + 1, X[i % 3] + 2, " ")

        else:
            self.help = True
            for i in range(lenofGr):
                self.stdscr.addstr(Y[i // 3] + 1, X[i % 3] + 2, str(i))
        return 0

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
                n = n.decode("utf-8")
                if n == "h" or n == "H":
                    self.affHgr(posX, posY, len(G))

                    self.stdscr.addstr(Yin, Xin + 17, " ")
                elif n == "q":
                    return stdscr,"9"
                    # abandon
                if n.isdigit() and int(n) in self.valide:

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
        if endofGame(stdscr, r1, ml, c//2) == 0:
            return 0
        elif "G" in r1:

            gr = r1.split('G')[1]
            if "T" in r1:
                gr = r1.split('G')[1].replace(' ', '.')
                stdscr, n = M.affGr(gr, True)

                n = "P" + n + "\n"
                envoi(s, n)
            else:
                stdscr, n = M.affGr(gr, False)

        elif "T" in r1:
            r2 = s.recv(MAX).decode("utf-8")
            if "G" in r2:
                gr = r2.split('G')[1].replace(' ', '.')
                stdscr, n = M.affGr(gr, True)
                n = "P" + n + "\n"
                envoi(s, n)

        else:
            return 0

        r(stdscr)

class tron():

    chargrilleLg = "-"
    chargrilleCl = "|"
    tligne = 3
    tcolone = 6
    nbcolone = 15
    nbligne = 10
    actual = [8,1]

    adv = [1,13]
    mywall = []
    advwall = []
    colorme = 1
    colormywall = 5
    coloradv = 2
    coloradvwall = 3

    def __init__(self, s, l, c, dc):
        self.s, self.l, self.c, self.dc = s, l, c, dc
        self.largeur = self.nbcolone * (self.tcolone + 1)
        self.hauteur = self.nbligne * (self.tligne + 1)
        self.y = self.l // 2 - self.hauteur // 2
        self.x = self.dc
        # self.actual[0] = self.nbligne - 2
        # self.actual[1] =  1
        self.affGr()


        self.color()


        # n = wait(self.s, 'S')
        # addtext(stdscr, 5,5,n)
        self.move()

    def affGr(self):
            # add columns
        for k in range(self.nbcolone + 1):
            for i in range(self.tligne):
                for j in range(self.nbligne):
                    addtext(stdscr, 1 + self.y + i + j + j * self.tligne, self.x + self.tcolone * k + k,
                            self.chargrilleCl)

        # add rows
        for k in range(self.nbligne + 1):
            for i in range(self.tcolone):
                for j in range(self.nbcolone):
                    if self.x + 1 + i + j * self.tcolone % self.tcolone != 0:
                        addtext(stdscr, self.y + self.tligne * k + k, self.x + 1 + +j + i + j * self.tcolone,
                                self.chargrilleLg)

    def colorCase(self, L, colorn = 0):
        y,x = L
        for j in range(self.tligne):
            for k in range(self.tcolone):
                i = self.tligne - 1 - j
                addtext(stdscr, self.y + 1 + i + (self.tligne + 1) * y, self.x + 1 + k + (self.tcolone + 1) * x, " ",
                        color=curses.color_pair(colorn))

    def color(self,):
        self.colorCase(self.actual, self.colorme)
        # self.colorCase(self.tmp, self.colorme)
        self.colorCase(self.adv, self.coloradv)
        for p in self.mywall:
            self.colorCase(p,self.colormywall)
        for p in self.advwall:
            self.colorCase(p, self.coloradvwall)

    def move(self):

        tmp = []

        while 1:
            poss = [
                [self.actual[0] - 1, self.actual[1]],
                [self.actual[0] + 1, self.actual[1]],
                [self.actual[0], self.actual[1] + 1],
                [self.actual[0], self.actual[1] - 1]
            ]
            key = stdscr.getch()
            addtext(stdscr, 3,3,str(key))
            if key == curses.KEY_UP and self.actual[0] > 0 and [self.actual[0]-1,self.actual[1]] not in self.mywall and [self.actual[0]-1,self.actual[1]] not in self.advwall:
                for p in poss:
                    if p[0] >= 0 and p[1] >= 0 and p[0] <= self.nbligne - 1 and p[1] <= self.nbcolone - 1:
                        self.colorCase(p, 0)
                self.colorCase(self.actual,self.colormywall)
                self.colorCase(poss[0], self.colorme)

                self.color()
                tmp = poss[0]

            elif key == curses.KEY_DOWN and self.actual[0] < self.nbligne - 1 and [self.actual[0]+1,self.actual[1]] not in self.mywall and [self.actual[0]+1,self.actual[1]] not in self.advwall:
                for p in poss:
                    if p[0] >= 0 and p[1] >= 0 and p[0] <= self.nbligne - 1 and p[1] <= self.nbcolone -1:
                        self.colorCase(p, 0)
                self.colorCase(self.actual,self.colormywall)
                self.colorCase(poss[1], self.colorme)
                self.color()
                tmp = poss[1]

            elif key == curses.KEY_RIGHT and self.actual[1] < self.nbcolone - 1 and [self.actual[0],self.actual[1]+1] not in self.mywall and [self.actual[0],self.actual[1]+1] not in self.advwall:
                for p in poss:
                    if p[0] >= 0 and p[1] >= 0 and p[0] <= self.nbligne - 1 and p[1] <= self.nbcolone - 1:
                        self.colorCase(p, 0)
                self.colorCase(self.actual,self.colormywall)
                self.colorCase(poss[2], self.colorme)
                self.color()
                tmp = poss[2]
            elif key == curses.KEY_LEFT and self.actual[1] > 0 and [self.actual[0],self.actual[1]-1] not in self.mywall and [self.actual[0],self.actual[1]-1] not in self.advwall:
                for p in poss:
                    if p[0] >= 0 and p[1] >= 0 and p[0] <= self.nbligne - 1 and p[1] <= self.nbcolone - 1:
                        self.colorCase(p, 0)
                self.colorCase(self.actual,self.colormywall)

                self.colorCase(poss[3], self.colorme)
                self.color()
                tmp = poss[3]

            elif key == curses.KEY_BACKSPACE:
                envoi(self.s, "P" + str(-1) + "/" + str(-1) + "\n")

            elif key == 32 or key == 77 or key == curses.KEY_ENTER or key == 10:
                if tmp != []:
                    wait(self.s, 'NOW')
                    addtext(stdscr,3,4,"IF")
                    self.mywall.append(self.actual)
                    self.actual = tmp
                    self.advwall.append(self.adv)


                    envoi(self.s, "P"+ str(tmp[0]) + "/" +str(tmp[1]) + "\n")
                    # t.sleep(0.5)
                    rtr = self.s.recv(MAX).decode("utf-8")
                    if endofGame(stdscr,rtr, self.x+int(self.largeur//2), self.y + int(self.hauteur//2)) == 0:
                        return 0
                    elif "P" in rtr:
                        rtr = rtr[1:].split('/')
                        self.adv[0] = int(rtr[0])
                        self.adv[1] = int(rtr[1])

                        tmp = []
                        self.color()




class bataillenavale():
    chargrilleLg = "-"
    chargrilleCl = "|"
    tligne = 3
    tcolone = 6
    nbcolone = 10
    nbligne = 10
    help = False
    # list des positions prises [[y,x], [y2,x2] ...]
    pocc = []
    # state of position occ
    # 0 dont know
    # 1 nothing
    # 2 touch
    # 3 down
    # 4 mine
    poccstate= []

    # list des bateaux [[[y0, x0], [y1,x1], True/False]], [ [] [] / ] ... ]
    listBoat = []
    # list of cible envoyees
    penv = []
    #state of position sent
    # 0 dont know
    # 1 nothing -> White
    # 2 touch -> yellow
    # 3 down -> red
    penvstate = []

    listAllBoat = [2,3,4,4,5]

    def __init__(self, s, l, c, dc):
        self.s, self.l, self.c, self.dc = s, l, c, dc
        self.largeur = self.nbcolone * (self.tcolone + 1)
        self.hauteur = self.nbligne * (self.tligne + 1)
        self.y = self.l // 2 - self.hauteur // 2
        self.x = self.dc
        self.marge =[0, self.dc*3 + self.largeur]
        self.middle = self.x+self.largeur+int(self.dc*1.5)
        # addtext(stdscr, 3, 3, str(self.x) + " " + str(self.c))

        if self.l > self.hauteur + 4 and self.c > self.largeur:
            stdscr.clear()
            addtext(stdscr, self.y -3,self.x+self.largeur//2,">> YOUR BOATS <<", True, curses.color_pair(4))
            addtext(stdscr, self.y -3,self.marge[1]+ self.x+self.largeur//2,">> ADV BOATS <<", True, curses.color_pair(2))
            self.affGr()
            self.affHGr()
            self.placeboat()

            stdscr.clear()
            addtext(stdscr, self.y - 3, self.x + self.largeur // 2, ">> YOUR BOATS <<", True, curses.color_pair(4))
            addtext(stdscr, self.y - 3, self.marge[1] + self.x + self.largeur // 2, ">> ADV BOATS <<", True,
                    curses.color_pair(2))
            self.affGr()
            self.affHGr()
            self.colorAllBoat(4)
            self.jeu()

    def colorTab2(self):
        for k in range(len(self.penv)):
            if self.penvstate[k] == 1:
                self.colorCase2(self.penv[k], 5)
            elif self.penvstate[k] == 2:
                self.colorCase2(self.penv[k], 3)
            elif self.penvstate[k] == 3:
                self.colorCase2(self.penv[k], 2)

    def shoot(self):
        self.colorTab2()
        actual = [5, 5]

        self.colorCase2(actual, 6)

        while 1:

            key = stdscr.getch()

            if key == curses.KEY_UP and actual[0] > 0:
                self.colorCase2(actual, 0)
                actual[0] -= 1
                self.colorTab2()
                self.colorCase2(actual, 6)
            elif key == curses.KEY_DOWN and actual[0] < self.nbligne - 1:
                self.colorCase2(actual, 0)
                actual[0] += 1
                self.colorTab2()
                self.colorCase2(actual, 6)

            elif key == curses.KEY_RIGHT and actual[1] < self.nbcolone - 1:
                self.colorCase2(actual, 0)
                actual[1] += 1
                self.colorTab2()
                self.colorCase2(actual, 6)
            elif key == curses.KEY_LEFT and actual[1] > 0:
                self.colorCase2(actual, 0)
                actual[1] -= 1
                self.colorTab2()
                self.colorCase2(actual, 6)

            elif key == 77 or key == 32 or key == curses.KEY_ENTER or key == 10:
                if actual not in self.penv:
                    self.colorCase2(actual, 1)
                    self.penv.append(actual)
                    self.penvstate.append(0)
                    break
        return actual
    def jeu(self):
        while(1):
            r1 = self.s.recv(MAX).decode("utf-8")
            if endofGame(stdscr, r1, self.y + self.hauteur // 2, self.x + self.largeur // 2) == 0:
                return 0
            else:
                if "K" in r1:
                    P = self.shoot()
                    envoi(self.s, "P" + str(P[0]) + "/" + str(P[1]) + "\n")
                if "P" in r1:
                    nadv = (r1.split('P')[1])
                    if "T" in nadv:
                        nadv = nadv[1:].split('/')
                        self.penvstate[self.penv.index([int(nadv[0]), int(nadv[1])])] = 2
                        self.colorCase2([int(nadv[0]), int(nadv[1])], 3)
                    elif "C" in nadv:
                        nadv = nadv[1:].split('/')
                        self.colorBoat2([int(nadv[0]), int(nadv[1])], [int(nadv[2]), int(nadv[3])], 2)
                    elif "R" in nadv:
                        nadv = nadv[1:].split('/')
                        self.pocc.append([int(nadv[0]), int(nadv[1])])

                        self.poccstate.append(1)
                        self.colorCase([int(nadv[0]), int(nadv[1])],5)

                    P = self.shoot()
                    envoi(self.s, "P" + str(P[0]) + "/" + str(P[1]) + "\n" )


                elif "B" in r1:
                    nadv = (r1.split('B')[1])
                    # addstr(stdscr,3,3,nadv)
                    if "T" in nadv:
                        nadv = nadv[1:].split('/')

                        self.poccstate[self.pocc.index([int(nadv[0]), int(nadv[1])])] =  2
                        self.colorCase([int(nadv[0]), int(nadv[1])], 3)
                    elif "C" in nadv:
                        nadv = nadv[1:].split('/')
                        self.changeBoatState([int(nadv[0]), int(nadv[1])],[int(nadv[2]), int(nadv[3])])
                        self.colorBoat([int(nadv[0]), int(nadv[1])],[int(nadv[2]), int(nadv[3])], 2)



                    elif "R" in nadv:
                        nadv = nadv[1:].split('/')
                        self.penvstate[self.penv.index([int(nadv[0]), int(nadv[1])])] = 1
                        self.colorCase2([int(nadv[0]), int(nadv[1])], 5 )

    def checkHorizon(self, actual, end):
        if actual[0] == end[0]:
            return True
        else:
            return False

    def verif(self, actual, end, horizon):
        if horizon:
            for i in range(0, end[1]-actual[1]+1):
                p =[actual[0], actual[1]+i]
                if p in self.pocc:
                    return False
        else:
            for i in range(0, end[0]-actual[0]+1):
                p = [actual[0]+i, actual[1]]
                if p in self.pocc:
                    return False
        return True
    def colorAllBoat(self, colorn):
        for L in self.listBoat:
            actual, end, horizon = L
            if horizon:
                for i in range(0, end[1]-actual[1]+1):
                    self.colorCase([actual[0], actual[1] + i], colorn)
            else:
                for i in range(0, end[0]-actual[0]+1):
                    self.colorCase([actual[0]+i, actual[1]], colorn)

    def calcend(self,L, taille, horizon,):
        maxsize = [self.nbligne - 1, self.nbligne - 1]

        y,x = L
        if horizon:
            if x+taille-1 > maxsize[1]:
                return None
            else:
                return [y,x+taille-1]
        else:
            if y+taille-1 > maxsize[0]:
                return None
            else:
                return [y+taille-1, x]

    def changeBoatState(self, actual, end,state = 3):
        horizon = self.checkHorizon(actual, end)
        if horizon:
            for i in range(0, end[1] - actual[1] + 1):
                self.poccstate[self.pocc.index([actual[0], i+ actual[1]])] = state

        else:
            for i in range(0, end[0] - actual[0] + 1):
                self.poccstate[self.pocc.index([actual[0]+ i, actual[1]])] = state

    def colorBoat(self,actual, end, colorn= 1):
        horizon = self.checkHorizon(actual,end)
        if horizon:
            for i in range(0, end[1]-actual[1]+1):
                self.colorCase([actual[0], actual[1] + i], colorn)

        else:
            for i in range(0, end[0]-actual[0]+1):
                self.colorCase([actual[0]+i, actual[1]], colorn)




    def colorBoat2(self,actual, end, colorn= 1):
        horizon = self.checkHorizon(actual,end)
        if horizon:
            for i in range(0, end[1]-actual[1]+1):
                self.penvstate[self.penv.index([actual[0], actual[1] + i])] = 3
                self.colorCase2([actual[0], actual[1] + i], colorn)

        else:
            for i in range(0, end[0]-actual[0]+1):
                self.penvstate[self.penv.index([actual[0]+i, actual[1]])] = 3

                self.colorCase2([actual[0]+i, actual[1]], colorn)

    def colorend(self,actual, end, horizon, colorn= 1):
        if horizon:
            for i in range(1, end[1]-actual[1]+1):
                self.colorCase([actual[0], actual[1] + i], colorn)

        else:
            for i in range(1, end[0]-actual[0]+1):
                self.colorCase([actual[0]+i, actual[1]], colorn)

    def placeboat(self):
        addtext(stdscr,self.y -5, self.middle, "> Enter 'Space' to rotate <", True, 3)
        addtext(stdscr,self.y -4, self.middle, "> Enter 'Enter' to validate <", True, 3)

        for taille in self.listAllBoat:

            horizon = True
            actual = [5, 5]
            end = self.calcend(actual, taille, horizon)
            self.colorCase(actual, 5)
            self.colorend(actual, end, 1)

            while 1:

                key = stdscr.getch()

                if key == curses.KEY_UP and actual[0] > 0:
                    self.colorCase(actual,0)
                    self.colorend(actual,end,horizon,0)
                    actual[0] -=1
                    end = self.calcend(actual, taille, horizon)
                    self.colorCase(actual,5)
                    self.colorend(actual,end,horizon,1)
                elif key == curses.KEY_DOWN and end[0] < self.nbligne - 1:
                    self.colorCase(actual, 0)
                    self.colorend(actual,end,horizon,0)
                    actual[0] += 1
                    end = self.calcend(actual, taille, horizon)
                    self.colorCase(actual, 5)
                    self.colorend(actual,end, horizon,1)

                elif key == curses.KEY_RIGHT and end[1] < self.nbcolone - 1:
                    self.colorCase(actual, 0)
                    self.colorend(actual,end,horizon,0)
                    actual[1] += 1
                    end = self.calcend(actual, taille, horizon)
                    self.colorCase(actual, 5)
                    self.colorend(actual,end,horizon,1)

                elif key == curses.KEY_LEFT and actual[1] > 0:
                    self.colorCase(actual, 0)
                    self.colorend(actual,end,horizon,0)
                    actual[1] -= 1
                    end = self.calcend(actual, taille ,horizon)
                    self.colorCase(actual, 5)
                    self.colorend(actual,end,horizon,1)

                elif key == 32:
                    horizon = not horizon
                    tempend = self.calcend(actual, taille,  horizon)
                    if tempend != None:
                        horizon = not horizon
                        self.colorend(actual, end, horizon,0)
                        horizon = not horizon
                        end = tempend
                        self.colorend(actual, end, horizon,1)
                    else:
                        horizon = not horizon

                elif key == 77 or key == curses.KEY_ENTER or key == 10:
                    b= self.verif(actual, end, horizon)
                    if b:
                        self.addBoat(actual, end, horizon)
                        break
                self.colorAllBoat(4)

        addtext(stdscr, self.y - 5, self.middle, "                           ", True)
        addtext(stdscr, self.y - 4, self.middle, "                             ", True)
        addtext(stdscr, self.y - 4, self.middle, "WAITING FOR THE OTHER PLAYER", True, curses.color_pair(3))

        wait(self.s, 'NOW')
        tosend = "B"
        for actual,end,h in self.listBoat:

             tosend += str(actual[0]) + "/" + str(actual[1]) + "/" + str(end[0]) + "/" + str(end[1]) + "#"
        tosend += '\n'
        envoi(self.s, tosend)
        addtext(stdscr, self.y - 5, self.middle, "                           ", True)
        addtext(stdscr, self.y - 4, self.middle, "                             ", True)

        wait(self.s, "SS")


    #     envoi des bateau
    #  wait autre joueur

    def addBoat(self, actual, end, horizon):
        self.listBoat.append([actual, end, horizon])
        if horizon:
            for i in range(0, end[1]-actual[1]+1):
                self.pocc.append([actual[0], actual[1]+i])
                self.poccstate.append(4)

        else:
            for i in range(0, end[0]-actual[0]+1):
                self.pocc.append([actual[0]+i, actual[1]])
                self.poccstate.append(4)

    def affGr(self):
        for o in self.marge:
            # add columns
            for k in range(self.nbcolone + 1):
                for i in range(self.tligne):
                    for j in range(self.nbligne):
                        addtext(stdscr, 1 + self.y + i + j + j * self.tligne, o +self.x + self.tcolone * k + k,
                                self.chargrilleCl)

            # add rows
            for k in range(self.nbligne + 1):
                for i in range(self.tcolone):
                    for j in range(self.nbcolone):
                        if self.x + 1 + i + j * self.tcolone % self.tcolone != 0:
                            addtext(stdscr, self.y + self.tligne * k + k, o +self.x + 1 + +j + i + j * self.tcolone,
                                    self.chargrilleLg)
    def affHGr(self):
        for o in self.marge:
            if self.help:
                for k in range(self.nbcolone):
                    addtext(stdscr, self.y - 1, o +self.x + self.tcolone // 2 + k + k * self.tcolone, " ")
            else:
                for k in range(self.nbcolone):
                    addtext(stdscr, self.y - 1, o +self.x + self.tcolone // 2 + k + k * self.tcolone, str(k))

        for k in range(self.nbligne):
            addtext(stdscr, self.y + self.tligne // 2 + k + k * self.tligne+1, self.x -2, str(k))
            addtext(stdscr, self.y + self.tligne // 2 + k + k * self.tligne+1 , self.x -2 + self.marge[1], str(k))
    def colorCase(self, L, colorn = 0):
        y,x = L
        for j in range(self.tligne):
            for k in range(self.tcolone):
                i = self.tligne - 1 - j
                addtext(stdscr, self.y + 1 + i + (self.tligne + 1) * y, self.x + 1 + k + (self.tcolone + 1) * x, " ",
                        color=curses.color_pair(colorn))
                # t.sleep(0.00005)

    def colorCase2(self, L, colorn = 0):
        y,x = L
        for j in range(self.tligne):
            for k in range(self.tcolone):
                i = self.tligne - 1 - j
                addtext(stdscr, self.y + 1 + i + (self.tligne + 1) * y, self.marge[1]+ self.x + 1 + k + (self.tcolone + 1) * x, " ",
                        color=curses.color_pair(colorn))
                # t.sleep(0.00005)
class puissanceq():
    chargrilleLg = "-"
    chargrilleCl = "|"
    tligne = 6
    tcolone = 10
    nbcolone = 7
    nbligne = 6
    help = False
    colorn = 2
    colornadv = 3

    def __init__(self, s, l, c, dc):
        self.s, self.l, self.c, self.dc = s, l, c, dc
        self.largeur = self.nbcolone * (self.tcolone + 1)
        self.hauteur = self.nbligne * (self.tligne + 1)

        self.y = self.l // 2 - self.hauteur // 2 - 2
        self.x = self.dc
        self.coloneMax = [self.nbligne for k in range(self.nbcolone)]

        if self.l > self.hauteur + 4 and self.c > self.largeur:
            stdscr.clear()

            # r(stdscr)
            self.affGr()
            self.affHGr()
            self.jeu()

    def jeu(self):
        while (1):
            r1 = self.s.recv(MAX).decode("utf-8")
            if endofGame(stdscr,r1,self.y+self.hauteur//2,self.x+self.largeur//2) == 0:
                return 0
            else:
                if "T" in r1:
                    nadv = int(r1.split('T')[1])
                    if nadv != -1:
                        self.colorCase(self.coloneMax[nadv], nadv, True)
                        self.coloneMax[nadv] -= 1
                        rtr = wait(self.s,'C')
                        if endofGame(stdscr,rtr, self.y+self.hauteur//2,self.x+self.largeur//2)==0:
                            return 0
                        rtr = int(rtr.split('C')[1])
                    else:
                        rtr =1

                    if rtr == 1:

                        addtext(stdscr, self.y + self.hauteur + 2, self.x + self.tcolone, "> Enter the columns to play: ")
                        addtext(stdscr, self.y + self.hauteur + 3, self.x + self.tcolone, ">")

                        # n = gettxt(stdscr, self.y + self.hauteur + 3, self.x + self.tcolone + 1, 2)
                        while(1):
                            n = gettxt(stdscr, self.y + self.hauteur + 3, self.x + self.tcolone + 1, 2)
                            if n == "h" or n == "H":
                                self.affHGr()
                                addtext(stdscr, self.y + self.hauteur + 3, self.x + self.tcolone+1, "   ")

                            # help page
                            elif "q" in n:
                                envoi(self.s,"C9\n")
                                break
                            elif n.isdigit():
                                addtext(stdscr, self.y + self.hauteur + 3, self.x + self.tcolone, ">  ")
                                n = int(n)
                                if n < self.nbcolone:
                                    if self.coloneMax[n] != 0:
                                        self.colorCase(self.coloneMax[n], n)
                                        self.coloneMax[n] -= 1
                                        envoi(self.s, "P"+ str(n)+ "\n")
                                        addtext(stdscr, self.y + self.hauteur + 2, self.x + self.tcolone,
                                                "                             ")
                                        addtext(stdscr, self.y + self.hauteur + 3, self.x + self.tcolone, " ")

                                        addtext(stdscr, self.y + self.hauteur + 3, self.x + self.tcolone + 1, "   ")
                                        break


                            else:
                                addtext(stdscr, self.y + self.hauteur + 3, self.x + self.tcolone+1, "   ")
                                break



    def colorCase(self, y, x, adv  = False):
        if adv:
            colorn = self.colornadv
        else:
            colorn = self.colorn
        for j in range(self.tligne):
            for k in range(self.tcolone):
                i = self.tligne - 1 - j
                addtext(stdscr, self.y + (self.tligne+1) * y-1-j, self.x + 1 + k + (self.tcolone + 1) * x, " ",
                        color=curses.color_pair(colorn))
                t.sleep(0.005)

    def affHGr(self):
        if self.help:
            self.help = False
            for k in range(self.nbcolone):
                addtext(stdscr, self.y - 1, self.x + self.tcolone // 2 + k + k * self.tcolone, " ")
        else:
            self.help = True
            for k in range(self.nbcolone):
                addtext(stdscr, self.y - 1, self.x + self.tcolone // 2 + k + k * self.tcolone, str(k))

    def affGr(self):
        # add columns
        for k in range(self.nbcolone + 1):
            for i in range(self.tligne):
                for j in range(self.nbligne):
                    addtext(stdscr, 1 + self.y + i + j + j * self.tligne, self.x + self.tcolone * k + k,
                            self.chargrilleCl)

        # add rows
        for k in range(self.nbligne + 1):
            for i in range(self.tcolone):
                for j in range(self.nbcolone):
                    if self.x + 1 + i + j * self.tcolone % self.tcolone != 0:
                        addtext(stdscr, self.y + self.tligne * k + k, self.x + 1 + +j + i + j * self.tcolone,
                                self.chargrilleLg)

def endofGame(stdscr,r1,y,x):
    if "GG" in r1:
        stdscr.clear()
        addtext(stdscr, y,x,"WELL DONE !", True, curses.color_pair(4))
        t.sleep(2)
        return 0
    elif "L" in r1:
        stdscr.clear()
        addtext(stdscr, y, x, "You lose....", True, curses.color_pair(2))
        t.sleep(2)
        return 0
    elif "E" in r1:

        stdscr.clear()
        addtext(stdscr, y, x, "Equality", True, curses.color_pair(3))
        t.sleep(2)
        # print("Equality")
        return 0
    else:
        return 1
###### CHAT ########
class chat:
    charseparation = "|"

    def __init__(self, stdscr, c, lmax):
        self.c = c
        self.lmax = lmax
        self.stdscr = stdscr
        self.stdscr = self.separation()
        self.stdscr = self.cht()
        r(self.stdscr)

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
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

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


def gettxt(stdscr, y, x, lenofstr, inputtext=""):
    curses.echo()
    stdscr.keypad(False)
    while True:
        if len(inputtext) != 0:
            break
        else:
            inputtext = stdscr.getstr(y, x, lenofstr)
            r(stdscr)
    stdscr.keypad(True)
    curses.noecho()
    inputtext = inputtext.decode("utf-8")
    return inputtext


def addtext(stdsrc, y, x, text="", center=False, color=""):
    if color == "":
        if center:
            stdscr.addstr(y, x - len(text) // 2, text)
        else:
            stdscr.addstr(y, x, text)

    else:
        if center:
            stdscr.addstr(y, x - len(text) // 2, text, color)
        else:
            stdscr.addstr(y, x, text, color)
    r(stdscr)


def r(stdscr):
    stdscr.move(0, 0)
    stdscr.refresh()


class Menu:
    # HOSTd = '2.3.130.203'
    PORTd = 45703
    HOSTd = '192.168.43.254'

    nom = ""

    def __init__(self, stdscr, y, x):
        self.stdscr = stdscr
        self.y = y
        self.x = x
        self.connected = False
        self.items = ['> Connect', '> Games', '> Settings', '> Exit']
        self.gamesItems = ['> Morpion', '> Puissance 4', '> Bataille Navale', '> TRON','> Back to main menu']
        self.settingsItems = ['> Change username', '> Back to main menu']

        self.initusr()
        if autoc:
            self.autoConnect()
        self.bienvenu()

    def initusr(self):
        try:
            self.fconf = open(fconfig, 'r')
            self.new = False

            return 0
        except:
            self.fconf = open(fconfig, 'w')
            self.new = True
            return 0

    def bienvenu(self):
        if anim:
            if self.new:
                tanim = 0.2
            else:
                tanim = 0.1
            text = " Hello "
            x = self.x // 2
            y = self.y // 2
            for k in range(7):
                self.stdscr.addstr(y, x - k - len(text) // 2, "-" * k + text + "-" * k)

                r(stdscr)
                t.sleep(tanim)
            if self.new:
                textEnter = "Enter your username:"
                x1 = self.x // 2 - len(textEnter) // 2
                addtext(stdscr, y + 1, x1, textEnter)
                addtext(stdscr, y + 2, x1, ">")
                u = gettxt(stdscr, y + 2, x1 + 1, 10)
                stdscr.clear()

                addtext(stdscr, y, x, "Welcome " + u + " !", True)
                self.fconf.write(u)
            else:
                stdscr.clear()
                u = self.fconf.read()
                addtext(stdscr, y, x, "Welcome back " + u + " !", True, color=curses.color_pair(2))
            self.nom = u
            t.sleep(1)

        # self.stdscr.addstr(y, x-k, " " *len("-"*k + text + "-"*k))

        self.menu()
        self.fconf.close()

    def lunchGame(self,y,x,name):
        while (1):
            dmdcode = "Entrer le code la partie: [4char]"

            addtext(stdscr, y + 2, x - len(dmdcode) // 2, dmdcode)
            addtext(stdscr, y + 3, x - len(dmdcode) // 2, ">")

            code = gettxt(stdscr, y + 3, 1 + x - len(dmdcode) // 2, 4)
            if len(code) == 4:
                stdscr.clear()
                break
            else:
                addtext(stdscr, y + 3, x - len(dmdcode) // 2, ">" + " " * 10)

        envoi(self.s, name + code + "\n")
        addtext(stdscr, y, x, "En attente d'autre joueur sur la partie: " + code, True)
        wait(self.s, 'S')
        stdscr.clear()

    def connectedState(self):
        text = ">>> You are not connected <<<"
        h, w = stdscr.getmaxyx()
        x = w // 2
        y = h // 2
        if not self.connected:
            addtext(stdscr, 3, x, text, True, color=curses.color_pair(2))
        else:
            addtext(stdscr, 3, x, ">>> You are connected <<<", True, color=curses.color_pair(4))

        if self.nom != "":
            addtext(stdscr, 5, x, "> Welcome " + self.nom + " <", True)

    def menu(self):
        current_row = 0
        self.print_menu(current_row)
        while 1:
            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.items) - 1:
                current_row += 1
            elif key == curses.KEY_RIGHT or key == 77:
                self.print_center(self.items[current_row])
                # self.stdscr.getch()
                # if user selected last row, exit the program
                if current_row == len(self.items) - 1:
                    break

            self.print_menu(current_row)

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
        elif text == "> Settings":
            self.settingsMenu()
        else:
            text = "You selected " + text
        h, w = stdscr.getmaxyx()
        x = w // 2
        y = h // 2
        r(self.stdscr)

    def gamesMenu(self):
        current_row = 0
        self.print_gamesmenu(current_row)
        while 1:
            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.gamesItems) - 1:
                current_row += 1
            elif key == curses.KEY_RIGHT or key == 77:
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
                self.lunchGame(y,x, "Morpion")
                morpion(self.s, stdscr, y, h, w)
            else:
                addtext(stdscr, y, x, "You must be connected to the server to play", True)
                self.stdscr.getch()
                return 0
        elif text == '> Puissance 4':
            if self.connected:
                self.lunchGame(y,x, "Puissance")
                puissanceq(self.s, h, w, 5)
            else:
                addtext(stdscr, y, x, "You must be connected to the server to play", True)
                self.stdscr.getch()
                return 0

        elif text == '> Bataille Navale':
            if self.connected:
                self.lunchGame(y,x, "Battleship")
                bataillenavale(self.s, h, w, 5)
            else:
                addtext(stdscr, y, x, "You must be connected to the server to play", True)
                self.stdscr.getch()
                return 0
        elif text == '> TRON':
            if self.connected:
                self.lunchGame(y,x, "Tron")
                tron(self.s, h,w,5)
            else:
                addtext(stdscr, y, x, "You must be connected to the server to play", True)
                self.stdscr.getch()
                return 0
        r(self.stdscr)

    def minitConnect(self, first=True):
        txt = "Enter server hostname (default" + str(self.HOSTd) + ")"
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(txt) // 2
        y = h // 2 - 3
        if not first:
            addtext(stdscr, y - 3, x, "/!\ Unable to connect, try again")
            addtext(stdscr, y + 1, x, " " * 16)
            addtext(stdscr, y + 4, x, " " * 10)

        addtext(stdscr, y - 2, x, "Enter \'quit\' to exit this menu")
        addtext(stdscr, y, x, txt)
        addtext(stdscr, y + 3, x, "Enter server port (default" + str(self.PORTd) + ")")

        addtext(stdscr, y + 1, x, ">")
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

    def autoConnect(self):
        s, HOST, PORT = socket.socket(socket.AF_INET, socket.SOCK_STREAM), self.HOSTd, self.PORTd
        while (True):
            try:
                s.connect((HOST, PORT))
                break
            except:
                return 0
        self.s, self.HOST, self.PORT = s, HOST, PORT
        self.connected = True
        envoi(self.s, "NC" + self.nom + "\n")
        return 0
    def mconnect(self):
        stdscr.clear()
        s, HOST, PORT = self.minitConnect()
        while (True):
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

    def settingsMenu(self):
        current_row = 0
        self.print_settingsmenu(current_row)
        while 1:
            key = self.stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(self.settingsItems) - 1:
                current_row += 1
            elif key == curses.KEY_RIGHT or key ==77:
                self.print_settingscenter(self.settingsItems[current_row])

                # self.stdscr.getch()
                # if user selected last row, exit the program
                if current_row == len(self.settingsItems) - 1:
                    break

            self.print_settingsmenu(current_row)

    def print_settingsmenu(self, selected_row_idx):
        self.stdscr.clear()
        self.connectedState()
        for idx, row in enumerate(self.settingsItems):
            h, w = stdscr.getmaxyx()
            x = w // 2 - len(row) // 2
            y = h // 2 - len(self.settingsItems) // 2 + 2 * idx
            if idx == selected_row_idx:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        r(self.stdscr)

    def print_settingscenter(self, text):

        stdscr.clear()
        h, w = stdscr.getmaxyx()
        x = w // 2
        y = h // 2

        if text == self.settingsItems[-1]:
            return 0

        elif text == '> Change username':
            textEnter = "Enter your new username:"
            x1 = self.x // 2 - len(textEnter) // 2
            stdscr.clear()
            addtext(stdscr, y, x1, "Actual username: " + self.nom)
            addtext(stdscr, y + 1, x1, textEnter)
            addtext(stdscr, y + 2, x1, ">")
            u = gettxt(stdscr, y + 2, x1 + 1, 10)
            self.fconf = open(fconfig, 'w')
            self.fconf.write(u)
            self.fconf.close()
            self.nom = u
            self.fconf = open(fconfig, 'r')
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
