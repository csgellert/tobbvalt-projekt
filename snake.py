from osztalyok import *   # minden osztályt / függvényt az osztalyok csomagból importálunk

#main()
#mozgott = False    # nem tudjuk mit csinál, lehet hogy még később kell
ai = evol() # kezdő generáció
genszam = 50
for i in range(genszam):
    ai.play()
    ai.fejlodes()
    ai = newgen(ai) # következő gen
    print(i)
ai.play(0) #Ha ezt átírjátok 1 re akkor megjeleníti a játékmenetet is
ai.fejlodes(True)
