import re
from collections import defaultdict, Counter

class Coordinate:
    def __init__(self, input_string = '', x = None, y = None):
        if (x == None and y == None):
            # Example: '220, 349'
            regex = '(\d+), (\d+)'
            (x,y) = re.findall(regex,input_string)[0]
            self.x = int(x)
            self.y = int(y)
        else:
            self.x = x
            self.y = y

coords = [Coordinate(input_string=l) for l in open('input.txt','r').readlines()]

def manhattan_distance(c1,c2):
    x_dist = abs(c1.x-c2.x)
    y_dist = abs(c1.y-c2.y)
    return x_dist + y_dist

def find_closest(target_coord,coords):
    min_dist = 999999
    min_coord = None
    tie = False
    for coord in coords:
        dist = manhattan_distance(target_coord,coord)
        if dist == min_dist:
            tie = True
            min_coord = None
        elif dist < min_dist:
            tie = False
            min_coord = coord
            min_dist = dist
    if tie == False:
        return min_coord

min_x = min([coord.x for coord in coords])
max_x = max([coord.x for coord in coords])
min_y = min([coord.y for coord in coords])
max_y = max([coord.y for coord in coords])

map = defaultdict(lambda: defaultdict(str))

# if you win a coordinate on the border of the map, you win infinite coordinates
# we need to remove these from our result set
edge_winners = set()

for x in range(min_x,max_x + 1):
    for y in range(min_y,max_y + 1):
        closest = find_closest(Coordinate(x=x, y=y),coords)
        if closest != None:
            map[x][y] = closest
            if (x == min_x or x == max_x or y == min_y or y == max_y):
                edge_winners.add(closest)

results = Counter([map[x][y] for x in map.keys() for y in map[x].keys()])

print ('Answer 1:')
print (max([count for (result,count) in results.most_common() if result not in edge_winners]))
