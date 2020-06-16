class evol:
	a = 0
	def __init__(self,szoveg):
		self.a = evol.a    # sorszám
		evol.a += 1
		self.b = szoveg
ai = evol('szoveg')
ai2 = evol('nem szoveg')
print(ai.a,ai.b)
print(ai2.a,ai2.b)
