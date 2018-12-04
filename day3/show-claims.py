import re
from operator import attrgetter

class Claim:
	def __init__(self, claim):
		# Example: '#3 @ 806,573: 20x19'
		regex = '#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'
		(self.id,self.left,self.top,self.width,self.height) = map(int,re.findall(regex,claim)[0])
		self.right = self.left + self.width
		self.bottom = self.top + self.height

claims = [Claim(l) for l in open('toy-input.txt','r').readlines()]

max_right = max(claims, key=attrgetter('right')).right
max_bottom = max(claims, key=attrgetter('bottom')).bottom

fabric = [['.' for i in range(max_right)] for j in range(max_bottom)]

for claim in claims:
	for i in range(claim.left,claim.right):
		for j in range(claim.top,claim.bottom):
			if fabric[j][i] == '.':
				fabric[j][i] = str(claim.id)
			else:
				fabric[j][i] = 'x'

for row in fabric:
	print(''.join(row))
