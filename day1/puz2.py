lines = [int(l.strip()) for l in open('input.txt','r').readlines()]
freq = 0
seen = set()
repeat = None
i = 0

while (repeat == None):
	freq = freq + lines[i]
	if freq in seen:
		repeat = freq
		break
	else:
		seen.add(freq)
	i += 1
	if (i == len(lines)):
		i = 0

print (repeat)
