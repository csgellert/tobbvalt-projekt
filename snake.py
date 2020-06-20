from osztalyok import *   # minden osztályt / függvényt az osztalyok csomagból importálunk
from tqdm import tqdm
import pickle
#main()
#mozgott = False    # nem tudjuk mit csinál, lehet hogy még később kell
try:
    with open("mentett.pkl", mode="rb") as opened_file:
        ai = pickle.load(opened_file)
        evol.gen=ai.gen
        evol.maxFit=ai.maxFit
        evol.minFit=ai.minFit
        evol.avgFit=ai.avgFit 
    print("File loaded in")
except:
    ai = evol() # kezdő generáció
    print("Error: 404 File not found")
genszam = 20
for i in tqdm(range(genszam)):
    ai.play()
    ai.fejlodes()
    ai = newgen(ai) # következő gen
    #print(i)
ai.save()#Az utolsó (megjelenített) generáció játéka nincs benne hogy le lehessen lőni a programot
ai.play() #Ha ezt átírjátok True ra akkor megjeleníti a játékmenetet is
ai.fejlodes(True)
