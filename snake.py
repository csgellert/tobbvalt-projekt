from osztalyok import *   # minden osztályt / függvényt az osztalyok csomagból importálunk

ai = load()
#ai = train(ai,iter=30) # kikommentelve ezzel lehet tovább fejleszteni az ai-t
#ai.save() # a továbbfejlesztést el lehet menteni
ai.fejlodes(show=True)
ai.play(megjel) # a globalis.py-ban lehet állítani. True esetén megjeleníti a utolsó generáció játékmenetét
