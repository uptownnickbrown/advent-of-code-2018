from collections import defaultdict

lines = [l.strip() for l in open('input.txt','r').readlines()]

ids = defaultdict(lambda: defaultdict(int))

for id in lines:
	for c in id:
		ids[id][c] += 1

twos = sum([any([ids[id][c] == 2 for c in ids[id]]) for id in ids])
threes = sum([any([ids[id][c] == 3 for c in ids[id]]) for id in ids])

print(twos * threes)
