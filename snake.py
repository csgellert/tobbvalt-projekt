from osztalyok import *   # minden osztályt / függvényt az osztalyok csomagból importálunk

#main()
#mozgott = False    # nem tudjuk mit csinál, lehet hogy még később kell
ai = evol() # kezdő generáció
ai.play()
ai = newgen(ai) # következő gen