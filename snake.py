from osztalyok import *   # minden osztályt / függvényt az osztalyok csomagból importálunk

ai = load()
ai = train(ai,35)
ai.save()#Az utolsó (megjelenített) generáció játéka nincs benne hogy le lehessen lőni a programot
ai.play(megjel) #Ha ezt átírjátok True ra akkor megjeleníti a játékmenetet is
ai.fejlodes(True)
