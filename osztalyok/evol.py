import pygame, sys
from .globalis import *
from .kigyo import kigyo
from statistics import mean
from matplotlib import pyplot as plt
import pickle

class evol:
    gen = 0 # hanyadik generációnál járunk... EZ EGY STATIKUS ADATTAG
    maxFit = []# statikus adattagok
    minFit = []
    avgFit = []
    def __init__(self):
        evol.gen += 1 # statikus adattagot egyel növeljük
        self.gen = evol.gen # létrehozunk egy csak az adott példányhoz tartozó "gen" adattagot
        global darabszam
        self.peldanySzam = darabszam
        self.peldanyok = [] #A kezdeti állományok...
        if self.gen == 1: # az első generációnál tölti fel randomokkal
            print("Kezdeti inicializalas")
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
    def play(self, mode  = False): #Mindegyik példány lejátszik egy meccset
        global bolyongas
        maradekLepes = bolyongas
        for idx, obj in enumerate(self.peldanyok):# bevezettem egy index változót is a fv-k miatt
            while maradekLepes > 0: # Ne bolyonghasssanak a végtelenségig...
                irany = self.network(self.inpLayer(idx),idx) #továbbra is random mozgás, de már NN -nel
                if(obj.isAlive):
                    startScore = obj.score
                    obj.move(irany,mozgott)
                    endScore = obj.score
                    if endScore > startScore:  # ha evett kaját, akkor újra van még "bolyongásnyi" lépése
                        maradekLepes = bolyongas
                    if obj.utkozike():
                      obj.isAlive=False
                    if (mode ==1):
                        self.mutat(obj)
                else:
                    if (mode):
                        display.blit(szoveg1,szoveg2)
                        pygame.display.update()
                        CLOCK.tick(1)
                    break # Ha meghal ne csinálja tovább...
            obj.fitness = (obj.steps - round(RACS/2)) + (2**obj.score - 1)*20 # fitness számítás
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
        #ha felfele van a fal vagy a teste:
        if fejHely[0]-1 < 0 or (fejHely[0]-1,fejHely[1]) in self.peldanyok[idx].snake:
            layer.append(1)
        else:
            layer.append(0)

        #ha jobbra van a kigyó vagy a teste:
        if fejHely[1]+1 > RACS-1 or (fejHely[0],fejHely[1]+1) in self.peldanyok[idx].snake:
            layer.append(1)
        else:
            layer.append(0)

        #ha lefele van a fal vagy a teste: (elvileg mindig 1)
        if fejHely[0]+1 > RACS-1 or (fejHely[0]+1,fejHely[1]) in self.peldanyok[idx].snake:
            layer.append(1)
        else:
            layer.append(0)

        #ha balra van a fal vagy a teste:
        if fejHely[1]-1 < 0 or (fejHely[0],fejHely[1]-1) in self.peldanyok[idx].snake:
            layer.append(1)
        else:
            layer.append(0)

        return np.asarray(layer)

    def select(self):
        global kritFit, kritÉrt
        selectionList = []
        for idx, obj in enumerate(self.peldanyok):
            if obj.fitness > kritFit:               # megnöveljük a jobb kígyók kiválasztásának esélyét
                for i in range(obj.fitness*kritÉrt):
                    selectionList.append(idx)
            else:
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
            ures = self.mutate(ures)
            child.append(ures.reshape(dad[i].shape))
        return child
    def mutate(self,array): # legyen 5% a mutáció esélye elemenként
        global mutRate
        for i in array:
            if random.random() < mutRate:
                i = random.random()
        return array
    def fejlodes(self,show = False):
        global kritFit
        fit = []
        for i in self.peldanyok:
            fit.append(i.fitness)
        evol.maxFit.append(max(fit))
        evol.minFit.append(min(fit))
        evol.avgFit.append(mean(fit))
        #kritFit = mean(fit)*1.2

        if (show):
            plt.plot(evol.maxFit)
            plt.plot(evol.minFit)
            plt.plot(evol.avgFit)
            plt.show()
    def save(self):
        self.maxFit = evol.maxFit # a statikus adattagokat csak így tudjuk átmenteni...
        self.minFit = evol.minFit
        self.avgFit = evol.avgFit
        with open("mentett.pkl", mode="wb") as f:
            pickle.dump(self, f) #Elmentjük az objektumot
        print("Status saved sucsessfully")
                
        




# új generációk előállítása, select, crossover ... (mutáció)
def newgen(elozo):
    ujgen = evol() # új generációnak az objektuma
    for i in range(darabszam):
        ujgen.add(kigyo(elozo.crossover())) # az új generációhoz hozzáadjuk az gyerek példányt, amibe először berakjuk az új súlyfüggvényeket
    return ujgen