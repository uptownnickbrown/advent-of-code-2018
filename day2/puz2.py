from collections import defaultdict

lines = [l.strip() for l in open('input.txt','r').readlines()]

mask_map = defaultdict(list)

for id in lines:
	for i in range(len(id)):
		masked = list(id)
		masked[i] = '*'
		mask_map[''.join(masked)].append(id)

for masked in mask_map:
	if len(mask_map[masked]) > 1:
		print masked.replace('*','')
