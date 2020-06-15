gen = 0
class evol:
	def __init__(self,szoveg):
		#global gen
		#gen += 1
		self.text = szoveg
	def function(self):
		global gen
		print(gen+2)
gener = []
gener.append(evol('elso'))
gener.append(evol('masodik'))
gener[0].function()
gener.pop(0)
print(gener[0].text)
