import pygame, sys
from .globalis import *
from .kigyo import kigyo

class evol:
    gen = 0 # hanyadik generációnál járunk... EZ EGY STATIKUS ADATTAG
    def __init__(self):
        evol.gen += 1 # statikus adattagot egyel növeljük
        self.gen = evol.gen # létrehozunk egy csak az adott példányhoz tartozó "gen" adattagot
        global darabszam
        self.peldanySzam = darabszam
        self.peldanyok = [] #A kezdeti állományok...
        if self.gen == 1: # az első generációnál tölti fel randomokkal
            for i in range(self.peldanySzam):
                self.peldanyok.append(kigyo()) #töltsük fel az állományt
    def add(self,inKigyo):
        self.peldanyok.append(inKigyo)
    def mutat(self,a):
        display.fill(FEKETE) #minden ciklus elején töröljük a képernyő tartalmát
        határrajzol() #a határok megrajzolása
        a.kigyorajzol()
        a.kajarajzol()
        pygame.display.update()
        CLOCK.tick(FPS)
    def play(self): #Mindegyik példány lejátszik egy meccset
        for idx, i in enumerate(self.peldanyok):# bevezettem egy index változót is a fv-k miatt
            for k in range(100): # Ne bolyonghasssanak a végtelenségig...
                irany = self.network(self.inpLayer(idx),idx) #továbbra is random mozgás, de már NN -nel
                if(i.isAlive):
                    i.move(irany,mozgott)
                    if i.utkozike():
                      i.isAlive=False
                    self.mutat(i)
                else:
                    display.blit(szoveg1,szoveg2)
                    pygame.display.update()
                    CLOCK.tick(1)
                    break # Ha meghal ne csinálja tovább...
            else:
                i.fitness = i.steps + i.score *100 #Ez a sor szerintem nem münködik
    #sigmoid fv...
    def sigm(self, x):
        return 1/(1+np.exp(-x))
    #maga a neurális háló
    def network(self, inp, idx):
        out = inp
        for i in self.peldanyok[idx].weights: #hogy bárhány hidden layerrel munködjön
            out = self.sigm(np.dot(out, i))
        return np.argmax(out)
    # ide majd meg kellene adni mit lásson a kígyó...
    def inpLayer(self, idx):
        return np.random.rand(1,2)
    def select(self):
        return (random.randint(0,self.peldanySzam-1),random.randint(0,self.peldanySzam-1))
    def crossover(self):
        a,b = self.select()
        dad = self.peldanyok[a].weights
        mom = self.peldanyok[b].weights
        child = []
        for i in range(len(dad)):
            child.append((dad[i]+mom[i])/2)
        return child


# új generációk előállítása, select, crossover ... (mutáció)
def newgen(elozo):
    ujgen = evol() # új generációnak az objektuma
    for i in range(darabszam):
        ujgen.add(kigyo(elozo.crossover())) # az új generációhoz hozzáadjuk az gyerek példányt, amibe először berakjuk az új súlyfüggvényeket
    return ujgen