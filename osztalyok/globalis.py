import pygame, sys
from pygame.locals import *
import numpy as np
import random



# AI paraméterek
darabszam = 100 # hány példány van egy generációban
mutRate = 0.2  # mutáció elemkénti esélye
kritFit = 100   # az a kígyó ami efölöttit ér el sokkal nagyobb eséllyel lesz kiválasztva
kritÉrt = 10    # ennyivel többször lesz beválogatva a kritikus fitnesszt elérő kígyó
bolyongas = 200 # max lépésszám kaja evés nélkül
megjel = False #Legyen e pgame ablak?

#globális változók: színek és méretek
FEKETE=(0,0,0)
FEHER=(255,255,255)
KEK=(0,0,255)
PIROS=(255,0,0)
ZOLD=(0,255,0)
MERET=(600) #az ablak mérete (Méret*Méret)
RACS=30 # NxN rács
#assert ((MERET/RACS)%1==0), 'MERET osztható kell legyen RACScsal'  de erre mi figyelünk

#A játék sebessége
FPS = 100 # FPS
if(megjel):
    pygame.init() # varázslat
    CLOCK=pygame.time.Clock() #óra objektum, ennek az "ütése" (tick) határozza majd meg a sebességet

    #ablak létrehozása:
    display=pygame.display.set_mode((MERET,MERET)) #létrehozunk egy adott méretű surface objektumot, ezt lehet kijelezni
    pygame.display.set_caption('Snake')#cím beállítása
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

#ha az adott ciklusban már mozgott a kígyó, ez jelzi. Egy ciklusban csak egyszer mozog: vagy mi mozgatjuk, vagy halad előre
global mozgott
mozgott=False

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
