import pygame, sys
from .globalis import *
from .kigyo import kigyo
from statistics import mean
from matplotlib import pyplot as plt
import pickle
from tqdm import tqdm

class evol: # Ez az osztály tartalmazza a Evolúciós AI algoritmushoz szükgséges függvényeket, és tárolja a populációt a "self.peldanyok"-ban
    gen = 0 # hanyadik generációnál járunk... EZ EGY STATIKUS ADATTAG
    maxFit = [] # statisztikához szükséges adattagok
    minFit = []
    avgFit = []
    elit = 0 # nagyon béna kígyók kizárásához

    # konstruktor
    def __init__(self):
        evol.gen += 1 # statikus adattagot egyel növeljük
        self.gen = evol.gen # létrehozunk egy csak az adott osztálypéldányhoz tartozó "gen" adattagot => Generáció sorszáma
        global darabszam
        self.peldanySzam = darabszam

        self.peldanyok = [] # Itt tároljuk az adott generációba tartozó kígyókat
        if self.gen == 1: # az első generációt véletlenszerű kígyókkal szeretnénk feltölteni
            print("Kezdeti inicializalas")
            for i in range(self.peldanySzam):
                self.peldanyok.append(kigyo())

    def add(self,inKigyo): # későbbi generációkhoz így adjuk hozzá a kígyókat
        self.peldanyok.append(inKigyo)

    # Pygame megjelenítés
    def mutat(self,obj):
        display.fill(FEKETE) # minden ciklus elején töröljük a képernyő tartalmát
        határrajzol()        # a határok megrajzolása
        obj.kigyorajzol()
        obj.kajarajzol()
        pygame.display.update()
        CLOCK.tick(FPS)
    
    # AI játszik
    def play(self, mode = False):
        global bolyongas
        for idx, obj in enumerate(self.peldanyok): # mindegyik példány lejátszik egy meccset
            maradekLepes = bolyongas
            while maradekLepes > 0: # Ne bolyonghassanak a végtelenségig...
                irany = self.network(self.inpLayer(idx),idx) # ITT mondja meg az AI, hogy merre akar lépni
                if(obj.isAlive):
                    if irany != obj.utolso: # kanyargás számlálása
                        obj.kanyargas += 1
                    startScore = obj.score  # mozgás előtti score
                    obj.move(irany) # mozgás
                    endScore = obj.score    # mozgás utáni score
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
                maradekLepes -= 1
            # fitness kiszámolása
            self.fitness(obj) 

    # szigmoid függvény
    def sigm(self, x):
        return 1/(1+np.exp(-x))

    # Neurális háló működése => itt választja ki az AI, hogy merre szeretne lépni
    def network(self, inp, idx):
        out = inp
        for i in self.peldanyok[idx].weights:
            out = self.sigm(np.dot(out, i))
        return np.argmax(out)

    # itt adjuk meg, hogy mit lát a kígyó
    def inpLayer(self, idx):
        layer = [] # felépítése: [0],[1]: irányvektor koordinátái a kajához, [2],[3],[4],[5]: lehetséges mozgásirányokban akadályok vannak-e

        fejHely = np.asarray(self.peldanyok[idx].fej)
        kajaHely = np.asarray(self.peldanyok[idx].kaja)
        iranyvektor = kajaHely-fejHely
        # normalizálás
        layer.append(iranyvektor[0]/RACS)
        layer.append(iranyvektor[1]/RACS)

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

    def fitness(self,obj): # fitness számítás
        obj.fitness = obj.kanyargas*2 + obj.steps + (2**obj.score - 1)

    # kiválasztás
    def select(self,mode=0):
        if mode == 0: # rulettkerékre felpakolunk minden kígyóból annyit, amennyi fitnesst elért ezután kétszer pörgetünk
            global kritFit, kritÉrt
            selectionList = []
            for idx, obj in enumerate(self.peldanyok):
                if obj.fitness > kritFit: # megnöveljük a nagyon jó kígyók kiválasztásának esélyét
                    for i in range(obj.fitness*kritÉrt):
                        selectionList.append(idx)
                else:
                    for i in range(obj.fitness):
                        selectionList.append(idx)
            while True: # do-while loop pythonban, két ugyanolyan kígyó kiválasztásának kizárására
                idx1 = selectionList[random.randint(0,len(selectionList)-1)]
                idx2 = selectionList[random.randint(0,len(selectionList)-1)]
                if self.peldanyok[idx1] != self.peldanyok[idx2]:
                    break
            return (idx1,idx2)
        if mode == 1: # két oldalú rulettkerék
            selectionList = []
            for idx, obj in enumerate(self.peldanyok):
                if obj.fitness >= evol.elit: # béna kígyókat kizárjuk
                    for i in range(obj.fitness):
                        selectionList.append(idx)
            rnd = random.randint(0,len(selectionList)-1)
            idx1 = selectionList[rnd]
            idx2 = selectionList[rnd-round(len(selectionList)/2)]
            return (idx1, idx2)

    # keresztezés
    def crossover(self):
        a,b = self.select()
        dad = self.peldanyok[a].weights
        mom = self.peldanyok[b].weights
        child = []
        for i in range(len(dad)):
            dns1 = np.matrix.flatten(dad[i])
            dns2 = np.matrix.flatten(mom[i])
            torespont = random.randint(1,len(dns1)-1)
            ures = np.zeros((len(dns1),))
            ures[0:torespont] = dns1[0:torespont]
            ures[torespont:] = dns2[torespont:]
            ures = self.mutate(ures)
            child.append(ures.reshape(dad[i].shape))
        return child

    # mutáció
    def mutate(self,array):
        global mutRate
        for i in array:
            if random.random() < mutRate:
                i = random.random()
        return array

    # statisztikák készítése
    def fejlodes(self,show = False): 
        global kritFit
        fit = []
        for obj in self.peldanyok:
            fit.append(obj.fitness)
        evol.maxFit.append(max(fit))
        evol.minFit.append(min(fit))
        evol.avgFit.append(mean(fit))
        evol.elit = np.quantile(fit,0.5) # nagyon béna kígyók kizárásához (kétoldalú rulettkeréknél alkalmazzuk)
        for obj in self.peldanyok:
            obj.div = abs(obj.fitness - evol.avgFit[-1])

        if (show):
            plt.plot(evol.maxFit)
            plt.plot(evol.minFit)
            plt.plot(evol.avgFit)
            plt.show()

    # legutolsó generáció, és korábbi statisztikák elmentése
    def save(self):
        self.maxFit = evol.maxFit # a statikus adattagokat csak így tudjuk átmenteni...
        self.minFit = evol.minFit
        self.avgFit = evol.avgFit
        with open("./Mentett/mentett.pkl", mode="wb") as f:
            pickle.dump(self, f) # Elmentjük az objektumot
        print("Status saved sucsessfully")

# legutolsó mentett generáció betöltése
def load():
    print("Loading in...")
    try:
        with open("./Mentett/mentett.pkl", mode="rb") as opened_file:
            ai = pickle.load(opened_file)
            evol.gen=ai.gen
            evol.maxFit=ai.maxFit
            evol.minFit=ai.minFit
            evol.avgFit=ai.avgFit 
        print("File loaded in")
    except:
        ai = evol() # kezdő generáció
        print("Error: 404 File not found")
    return ai

# új generációk előállítása, select, crossover, mutáció
def newgen(elozo):
    ujgen = evol() # új generációnak az objektuma
    for i in range(darabszam):
        ujgen.add(kigyo(elozo.crossover())) # az új generációhoz hozzáadjuk az gyerek példányt, amibe először berakjuk az új súlyfüggvényeket
    return ujgen

# az egész AI evolúciót kezelő függvény
def train(ai, iter):
    for i in tqdm(range(iter)):
        ai.play()
        ai.fejlodes()
        ai = newgen(ai) # következő gen
    return ai