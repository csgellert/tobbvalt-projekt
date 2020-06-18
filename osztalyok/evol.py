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
    def play(self, mode = 0): #Mindegyik példány lejátszik egy meccset
        for idx, obj in enumerate(self.peldanyok):# bevezettem egy index változót is a fv-k miatt
            for k in range(100): # Ne bolyonghasssanak a végtelenségig...
                irany = self.network(self.inpLayer(idx),idx) #továbbra is random mozgás, de már NN -nel
                if(obj.isAlive):
                    obj.move(irany,mozgott)
                    if obj.utkozike():
                      obj.isAlive=False
                    if (mode ==1):
                        self.mutat(obj)
                else:
                    display.blit(szoveg1,szoveg2)
                    pygame.display.update()
                    if (mode == 1):
                        CLOCK.tick(1)
                    break # Ha meghal ne csinálja tovább...
            obj.fitness = obj.steps + (2**obj.score)*20 # fitness számítás
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
        layer = [] # irányvektor, falak vannak-e

        fejHely = np.asarray(self.peldanyok[idx].fej)
        kajaHely = np.asarray(self.peldanyok[idx].kaja)
        iranyvektor = kajaHely-fejHely
        iranyvektor = iranyvektor/np.hypot(iranyvektor[0],iranyvektor[1]) # normalizálás
        layer.append(iranyvektor[0])
        layer.append(iranyvektor[1])

        # négy irányba végignézni, hogy van-e test vagy fal => true / false
        return np.asarray(layer)

    def select(self):
        selectionList = []
        for idx, obj in enumerate(self.peldanyok):
            for i in range(obj.fitness):
                selectionList.append(idx)
        idx1 = selectionList[random.randint(0,len(selectionList)-1)]
        idx2 = selectionList[random.randint(0,len(selectionList)-1)]  # még nincs kizárva, hogy ugyanazt válasszuk ki
        return (idx1,idx2)
    def crossover(self):
        a,b = self.select()
        dad = self.peldanyok[a].weights
        mom = self.peldanyok[b].weights
        child = []
        for i in range(len(dad)):
            sor1 = np.matrix.flatten(dad[i])
            sor2 = np.matrix.flatten(mom[i])
            torespont = random.randint(1,len(sor1)-1)
            ures = np.zeros((len(sor1),))
            ures[0:torespont] = sor1[0:torespont]
            ures[torespont:] = sor2[torespont:]
            child.append(ures.reshape(dad[i].shape))
        return child
    def mutate(self):
        pass



# új generációk előállítása, select, crossover ... (mutáció)
def newgen(elozo):
    ujgen = evol() # új generációnak az objektuma
    for i in range(darabszam):
        ujgen.add(kigyo(elozo.crossover())) # az új generációhoz hozzáadjuk az gyerek példányt, amibe először berakjuk az új súlyfüggvényeket
    return ujgen