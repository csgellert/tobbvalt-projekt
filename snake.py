import pygame, sys
from pygame.locals import *
import numpy as np
import random
from osztalyok import *   # minden osztályt / függvényt az osztalyok csomagból importálunk

#main()
#mozgott = False    # nem tudjuk mit csinál, lehet hogy még később kell
ai = evol() # kezdő generáció
ai2 = newgen(ai) # következő gen

ai2.play()