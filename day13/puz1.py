from defaultlist import defaultlist

# ok, executive decision - we're using degrees for turning

# > = 0 degrees
# v = 90 degrees
# < = 180 degrees
# ^ = 270 degrees

# meaning, to turn right, add 90 degrees, to turn left add 90 degrees (then mod 360 to keep all directions between 0-360)

direction_to_degrees = {
    '>' : 0,
    'v' : 90,
    '<' : 180,
    '^' : 270
}

# the carts rotate through these in a loop
turn_strategies = [-90, 0, 90]

class Cart:
    def __init__(self, x, y, c, cell):
        self.degrees = direction_to_degrees[c]
        self.occupying = cell

        self.turn_strategy_id = 0

class Cell:
    def __init__(self, x, y, c):
        self.x = x # x = column, second index to map[i][j]
        self.y = y # y = row, first index to map[i][j]
        self.track = c
        self.occupied_by = None
        if c in '>v<^':
            self.occupied_by = Cart(x,y,c,self)
            if c in '<>':
                self.track = '-'
            else:
                self.track = '|'

map = defaultlist(lambda: defaultlist(None))
carts = []

for i,row in enumerate(open('input.txt','r').readlines()):
    for j, c in enumerate(row):
        if c != '\n':
            map[i][j] = Cell(j,i,c)
            if map[i][j].occupied_by != None:
                carts.append(map[i][j].occupied_by)

collision = False
while (collision == False):
    for cart in sorted(sorted(carts, key=lambda cart:cart.occupying.x), key=lambda cart:cart.occupying.y):
        previous_cell = cart.occupying
        previous_cell.occupied_by = None

        if cart.degrees == 0:
            new_cell = map[previous_cell.y][previous_cell.x + 1]
        if cart.degrees == 90:
            new_cell = map[previous_cell.y + 1][previous_cell.x]
        if cart.degrees == 180:
            new_cell = map[previous_cell.y][previous_cell.x - 1]
        if cart.degrees == 270:
            new_cell = map[previous_cell.y - 1][previous_cell.x]

        if new_cell.occupied_by != None:
            print ('Oh no! Collision!')
            print (new_cell.x,new_cell.y)
            collision = True
            break

        if new_cell.track == '\\':
            if cart.degrees % 180 == 0:
                cart.degrees = (cart.degrees + 90) % 360
            else:
                cart.degrees = (cart.degrees - 90) % 360

        if new_cell.track == '/':
            if cart.degrees % 180 == 0:
                cart.degrees = (cart.degrees - 90) % 360
            else:
                cart.degrees = (cart.degrees + 90) % 360

        if new_cell.track == '+':
            cart.degrees = (cart.degrees + turn_strategies[cart.turn_strategy_id % 3]) % 360
            cart.turn_strategy_id += 1

        cart.occupying = new_cell
        new_cell.occupied_by = cart
