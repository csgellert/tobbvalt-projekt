import pygame, sys
from pygame.locals import *
import numpy as np
import random

#globális változók: színek és méretek
FEKETE=(0,0,0)
FEHER=(255,255,255)
KEK=(0,0,255)
PIROS=(255,0,0)
ZOLD=(0,255,0)
MERET=(600) #az ablak mérete (Méret*Méret)
RACS=30 #20*20-as rács
#assert ((MERET/RACS)%1==0), 'MERET osztható kell legyen RACScsal'

#A játék sebessége
FPS=10#FPS
CLOCK=pygame.time.Clock() #óra objektum, ennek az "ütése" (tick) határozza majd meg a sebességet

#ablak létrehozása:
display=pygame.display.set_mode((MERET,MERET)) #létrehozunk egy adott méretű surface objektumot, ezt lehet kijelezni
pygame.display.set_caption('Snake')#cím beállítása

#ha az adott ciklusban már mozgott a kígyó, ez jelzi. Egy ciklusban csak egyszer mozog: vagy mi mozgatjuk, vagy halad előre
global mozgott
mozgott=False

#kígyó osztály. Próbáltam Gege kódjának logikáját követni
#ahogy Gege kódjában, itt is egy négyzetes mátrix jelzi a kígyó helyét, egy "rácson" mozog, amely RACS osztásból áll (globális változó). A pozíció alapján rajzoljuk ki a képernyőre
class kigyo:
    fej=(3,3) #a kígyó feje
    snake=[] #a kígyó testét tartalmazza
    snake.append(fej)
    snake.append((fej[0]-1,fej[1]))
    snake.append((fej[0]-2,fej[1]))
    isAlive=True #él-e a kígyó
    steps=0 #lépésszámláló, majd jó lesz az AI-hoz
    utolso=2 #az utolsó lépése a kígyónak (balra, jobbra, föl, le), hogy ne tudjon a kígyó töbsször egy irányba mozogni ("ugrani")
    kaja=((random.randint(0,RACS),random.randint(0,RACS))) #kaja random helyen
    elozo=2

    #uj random kaja készítő
    def ujKaja(self):
       while True:
            x=random.randint(0,RACS)
            y=random.randint(0,RACS)
            if (x,y) in self.snake: # megnézem, hogy nem esik-e bele a kaja saját magába
                return self.ujKaja() # rekurzió
            return (x,y) # ha minden rendben van

    #mozgás: Gege kódja alapján
    def move(self, direction,mozgott):
        if mozgott==False:
            if direction==0:
                self.utolso=0
                mozgott=True
                self.fej = (self.fej[0]-1,self.fej[1])
                if self.fej==self.kaja:
                    self.snake.insert(0,self.fej)
                    self.kaja= self.ujKaja()
                else:
                    self.snake.pop()
                    self.snake.insert(0,self.fej)
            if direction==1:
                self.utolso=1
                mozgott=True
                self.fej = (self.fej[0],self.fej[1]+1)
                if self.fej==self.kaja:
                    self.snake.insert(0,self.fej)
                    self.kaja= self.ujKaja()
                else:
                    self.snake.pop()
                    self.snake.insert(0,self.fej)
            if direction==2:
                self.utolso=2
                mozgott=True
                self.fej = (self.fej[0]+1,self.fej[1])
                if self.fej==self.kaja:
                    self.snake.insert(0,self.fej)
                    self.kaja= self.ujKaja()
                else:
                    self.snake.pop()
                    self.snake.insert(0,self.fej)
            if direction==3:
                self.utolso=3
                mozgott=True
                self.fej = (self.fej[0],self.fej[1]-1)
                if self.fej==self.kaja:
                    self.snake.insert(0,self.fej)
                    self.kaja= self.ujKaja()
                else:
                    self.snake.pop()
                    self.snake.insert(0,self.fej)

    #a kígyó kirajzolása
    def kigyorajzol(self):
        for i in range(len(self.snake)): #minden egyes elem helyére rajzolunk egy négyzetet
            tmp=self.snake[i] #az aktuális kígyó-elem mérete
            sor=tmp[1]*MERET/(RACS+1)
            oszlop=tmp[0]*MERET/(RACS+1)
            négyzet=pygame.Rect(sor+MERET/RACS/10/2,oszlop+MERET/RACS/10/2,MERET/(RACS+1)-MERET/RACS/10,MERET/(RACS+1)-MERET/RACS/10)
            pygame.draw.rect(display,PIROS,négyzet,)
            if i==0: #a kígyó szemei, ez már high graphics
                pygame.draw.circle(display,KEK,(int(sor)+int(MERET/(RACS+1)/4),int(oszlop)+int(MERET/(RACS+1)/2)),5)
                pygame.draw.circle(display,KEK,(int(sor)+int(MERET/(RACS+1)/4*3),int(oszlop)+int(MERET/(RACS+1)/2)),5)

    #a kaja megrajzolása:zöld négyzet
    def kajarajzol(self):
         tmp=self.kaja
         sor=tmp[1]*MERET/(RACS+1)
         oszlop=tmp[0]*MERET/(RACS+1)
         négyzet=pygame.Rect(sor+2,oszlop+2,MERET/(RACS+1)-4,MERET/(RACS+1)-4)
         pygame.draw.rect(display,ZOLD,négyzet,)

    #megvizsgálja, hogy ütközik-e a kígyó. Azt is észreveszi, ha magába fut
    def utkozike(self):
        if self.fej[0]<0 or self.fej[0]>RACS or self.fej[1]<0 or self.fej[1]>RACS:
            return True
        for i in range(len(self.snake)-1):
            if self.snake[i+1]==self.fej:
                return True

#a rács megrajzolása. 
def racsrajzol():
    for i in range(RACS+3): #rácsvonalak függőlegesen
        pygame.draw.line(display, FEHER,(MERET*(i)/(RACS+1),0),(MERET*(i)/(RACS+1),MERET))
    for j in range(RACS+3): #rácsvonalak vízszintesen
        pygame.draw.line(display, FEHER,(0,MERET*(j)/(RACS+1)),(MERET,MERET*(j)/(RACS+1)))
def határrajzol():
    #a határok vastag kék vonallal, ez is csak szépítés
    pygame.draw.line(display, KEK,(0,0),(0,MERET),5)
    pygame.draw.line(display, KEK,(0,0),(MERET,0),5)
    pygame.draw.line(display, KEK,(0,MERET),(MERET,MERET),5)
    pygame.draw.line(display, KEK,(MERET,0),(MERET,MERET),5)

#main. Külön megírva menő :D
def main():
    piton=kigyo() #mi más lenne a neve?
    pygame.init() #ez mindig kell, hogy a pygame függvényei és objektumai jól meghívódjanak

    #a szoveg kiiratás előkészítése különböző objektumokkal. Ez elég macerás, három lépcsős folyamat, de annyira nem is fontos a projekt szempontjából
    #szoveg: Game over
    szoveg=pygame.font.Font('freesansbold.ttf',32) 
    #pont: 'Pontok' felira
    pont=pygame.font.Font('freesansbold.ttf',16)
    szoveg1=szoveg.render('Game over!',True,KEK,PIROS)
    pont1=pont.render('Pontok:',True,KEK,PIROS)
    #pontszam: az aktuális pontszám (megevett kaják száma)
    pont2=pont1.get_rect()
    szoveg2=szoveg1.get_rect()
    pont2.center=(MERET/2, MERET-MERET/RACS/2)
    szoveg2.center=(MERET/2,MERET/2)
    
    while True: #game loop: mindig fut, ebben történnek az események, és itt frissül a képernyő
       
        display.fill(FEKETE) #minden ciklus elején töröljük a képernyő tartalmát
        #racsrajzol() #racs rajzolása. kikommentelve jobb a játékélmény szerintem :D
        határrajzol() #a határok megrajzolása
        mozgott=False #minden kör elején False
        key=pygame.key.get_pressed() #gombnyomás objektum (?)
        l=len(kigyo.snake) #a kígyó aktuális hossza

        for event in pygame.event.get(): #végigmegy a ciklus alatt történt összes eventen: event handling
            if event.type==QUIT: #ezt mindig bele kell írni, nem egészen tiszta, hogy mit csinál, mert nem ez léptet ki
                pygame.quit
                sys.exit
            #ha az event gomb lenyomása:
            if event.type==KEYDOWN:
                #ha a gomb a fel/le/jobbra/balra
                if event.key==K_UP and piton.utolso!=0 and piton.utolso!=2:
                    piton.move(0,mozgott)
                    
                elif event.key==K_RIGHT and piton.utolso!=1 and piton.utolso!=3:
                    piton.move(1,mozgott)
                    
                elif event.key==K_DOWN and piton.utolso!=2 and piton.utolso!=0:
                    piton.move(2,mozgott)
                    
                elif event.key==K_LEFT and piton.utolso!=3 and piton.utolso!=1:
                    piton.move(3,mozgott)
                #a tesztelés alatt az tűnt jobbnak a "játékélmény" szempontjából, ha ide van berakva a kirajzolás
                piton.kigyorajzol()
                piton.kajarajzol()
                #a szoveget rá kell másolni (blit) az ablakra
                pontszam1=pont.render(str(l-3),True,KEK,PIROS)
                pontszam2=pontszam1.get_rect()
                pontszam2.center=(MERET/2+40, MERET-MERET/RACS/2)
                display.blit(pont1,pont2)
                display.blit(pontszam1,pontszam2)
                #ez nagyon fontos: ez frissíti a kijelzőt minden ciklusban
                pygame.display.update()
                continue #ez hasznosnak tűnt
        if mozgott==False: #ha a kígyó még nem mozgott a ciklusban, akkor automatikusan mozog
            piton.move(piton.utolso,mozgott)
            piton.kigyorajzol()
            piton.kajarajzol()
            #ide is jobbnak tűnt berakni
            pontszam1=pont.render(str(l-3),True,KEK,PIROS)
            pontszam2=pontszam1.get_rect()
            pontszam2.center=(MERET/2+40, MERET-MERET/RACS/2)
            display.blit(pont1,pont2)
            display.blit(pontszam1,pontszam2)
            pygame.display.update()
        #ha a kígyó meghal, kilép a game loop-ból
        if piton.utkozike():
            isAlive=False
            break
        CLOCK.tick(FPS)#csak akkor megy továb, ha 1/FPS sec eltelt az előző hívás óta, ez a sebesség szabályozója
        #game loop vége

    #a játék vége: Game over kiírása, majd kilépés
    display.blit(szoveg1,szoveg2)
    pygame.display.update()
    CLOCK.tick(1)
    del piton
    pygame.quit()
    sys.exit


main()

