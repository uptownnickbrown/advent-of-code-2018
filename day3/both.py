import re
from operator import attrgetter

class Claim:
	def __init__(self, claim):
		# Example: '#3 @ 806,573: 20x19'
		regex = '#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'
		(self.id,self.left,self.top,self.width,self.height) = map(int,re.findall(regex,claim)[0])
		self.right = self.left + self.width
		self.bottom = self.top + self.height
		self.overlapped = False

claims = [Claim(l) for l in open('input.txt','r').readlines()]

max_right = max(claims, key=attrgetter('right')).right
max_bottom = max(claims, key=attrgetter('bottom')).bottom

fabric = [[[] for i in range(max_right)] for j in range(max_bottom)]

for claim in claims:
	for i in range(claim.left,claim.right):
		for j in range(claim.top,claim.bottom):
			if fabric[j][i] != []:
				fabric[j][i].append(claim)
				for overlapped_claim in fabric[j][i]:
					overlapped_claim.overlapped = True
			else:
				fabric[j][i].append(claim)

overlaps = sum([sum([len(cell) > 1 for cell in row]) for row in fabric])
print (overlaps)

non_overlapped_claims = [claim.id for claim in claims if claim.overlapped == False]
print (non_overlapped_claims[0])
