import re

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

def close_enough(target_coord,coords):
    return sum([manhattan_distance(target_coord,coord) for coord in coords]) < 10000

min_x = min([coord.x for coord in coords])
max_x = max([coord.x for coord in coords])
min_y = min([coord.y for coord in coords])
max_y = max([coord.y for coord in coords])

print ('Answer 2:')
print (sum([close_enough(Coordinate(x=x, y=y),coords) for y in range(min_y,max_y) for x in range(min_x,max_x)]))
