from osztalyok import *   # minden osztályt / függvényt az osztalyok csomagból importálunk
from tqdm import tqdm
#main()
#mozgott = False    # nem tudjuk mit csinál, lehet hogy még később kell
ai = evol() # kezdő generáció
genszam = 50
for i in tqdm(range(genszam)):
    ai.play()
    ai.fejlodes()
    ai = newgen(ai) # következő gen
    #print(i)
ai.play() #Ha ezt átírjátok True ra akkor megjeleníti a játékmenetet is
ai.fejlodes(True)
