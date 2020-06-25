#egy négyzetes mátrix jelzi a kígyó helyét, egy "rácson" mozog, amely RACS osztásból áll (globális változó). A pozíció alapján rajzoljuk ki a képernyőre
from .globalis import *

class kigyo:
    isAlive = True # él-e a kígyó
    steps = 0 # hány lépést élt meg az adott példány
    score = 0 # hány kaját evett meg eddig
    fitness = 0
    div = 0  # diverzitás
    utolso = 2 # az utolsó lépése a kígyónak (balra, jobbra, föl, le)
    kanyargas = 0 # hányszor kanyarodott

    # konstruktor
    def __init__(self,child=0): 
        self.weights = [] # ebben tároljuk a neurális háló struktúráját
        if child == 0: # child = 0, ha ez az első populáció
            self.weights.append(np.random.rand(6,20)) # véletlen generált súlyokkal kezdünk
            #self.weights.append(np.random.rand(20,20))
            self.weights.append(np.random.rand(20,4))
        else: # ha ez már egy fejlődés által létrehozott populáció, akkor eltároljuk a child változóban beadott súlymátrixot
            self.weights = child

        self.fej=(round(RACS/2),round(RACS/2))  # a kígyó feje
        self.snake=[] # a kígyó testét tartalmazza
        self.snake.append(self.fej)
        self.snake.append((self.fej[0]-1,self.fej[1]))
        self.snake.append((self.fej[0]-2,self.fej[1]))

        # elhelyezzük az első kaját a pályán (ha true, akkor nem számol plusz score-t)
        self.kaja = self.ujKaja(True)

    # uj kaja helyét meghározó függvény
    def ujKaja(self,rekurzio=False):
        if rekurzio==False:
            self.score += 1
        while True:
            x=random.randint(0,RACS)
            y=random.randint(0,RACS)
            if (x,y) in self.snake: # megnézem, hogy nem esik-e a kígyó testébe a kaja
                return self.ujKaja(True) # rekurzió
            else:
                return (x,y)

    # mozgás kezelése
    def move(self, direction):
        if direction==0:    # fel
            self.utolso=0
            self.fej = (self.fej[0]-1,self.fej[1])
            if self.fej==self.kaja:
                self.snake.insert(0,self.fej)
                self.kaja= self.ujKaja()
            else:
                self.snake.pop()
                self.snake.insert(0,self.fej)
        if direction==1:    # jobbra
            self.utolso=1
            self.fej = (self.fej[0],self.fej[1]+1)
            if self.fej==self.kaja:
                self.snake.insert(0,self.fej)
                self.kaja= self.ujKaja()
            else:
                self.snake.pop()
                self.snake.insert(0,self.fej)
        if direction==2:    # le
            self.utolso=2
            self.fej = (self.fej[0]+1,self.fej[1])
            if self.fej==self.kaja:
                self.snake.insert(0,self.fej)
                self.kaja= self.ujKaja()
            else:
                self.snake.pop()
                self.snake.insert(0,self.fej)
        if direction==3:    # balra
            self.utolso=3
            self.fej = (self.fej[0],self.fej[1]-1)
            if self.fej==self.kaja:
                self.snake.insert(0,self.fej)
                self.kaja= self.ujKaja()
            else:
                self.snake.pop()
                self.snake.insert(0,self.fej)
            # lépésszámláló
            self.steps +=1 

    # a kígyó kirajzolása a pygame segítségével
    def kigyorajzol(self):
        for i in range(len(self.snake)): # minden egyes elem helyére rajzolunk egy négyzetet
            tmp=self.snake[i]
            sor=tmp[1]*MERET/(RACS+1)
            oszlop=tmp[0]*MERET/(RACS+1)
            négyzet=pygame.Rect(sor+MERET/RACS/10/2,oszlop+MERET/RACS/10/2,MERET/(RACS+1)-MERET/RACS/10,MERET/(RACS+1)-MERET/RACS/10)
            pygame.draw.rect(display,PIROS,négyzet,)
            if i==0: # a kígyó szemei, ez már high graphics
                pygame.draw.circle(display,KEK,(int(sor)+int(MERET/(RACS+1)/4),int(oszlop)+int(MERET/(RACS+1)/2)),5)
                pygame.draw.circle(display,KEK,(int(sor)+int(MERET/(RACS+1)/4*3),int(oszlop)+int(MERET/(RACS+1)/2)),5)

    # a kaja megrajzolása: zöld négyzet
    def kajarajzol(self):
         tmp=self.kaja
         sor=tmp[1]*MERET/(RACS+1)
         oszlop=tmp[0]*MERET/(RACS+1)
         négyzet=pygame.Rect(sor+2,oszlop+2,MERET/(RACS+1)-4,MERET/(RACS+1)-4)
         pygame.draw.rect(display,ZOLD,négyzet,)

    # megvizsgálja, hogy ütközik-e a kígyó. Azt is észreveszi, ha magába fut
    def utkozike(self):
        if self.fej[0]<0 or self.fej[0]>RACS or self.fej[1]<0 or self.fej[1]>RACS:
            return True
        for i in range(len(self.snake)-1):
            if self.snake[i+1]==self.fej:
                return True
