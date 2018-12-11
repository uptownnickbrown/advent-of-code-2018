serial_number = 5235
# can't remove why I switched to this from a simple array of arrays...
grid = defaultdict(lambda: defaultdict(int))

for x in range(1,301):
    for y in range(1,301):
        #print(x,y)
        rack_id = x + 10
        power_level = rack_id * y
        power_level += serial_number
        power_level = power_level * rack_id
        string_power_level = str(power_level)
        if len(string_power_level) > 2:
            power_level = int(string_power_level[-3]) - 5
        else:
            power_level = -5
        grid[x][y] = power_level
        #print(power_level)

max_power = 0
max_coord = (0,0)
max_size = 0
for x in range(1,301):
    print(x) # so you can track the agonizingly slow progress
    for y in range(1,301):
        for s in range(1,min([301-x,301-y])):
            rows = [grid[x + i] for i in range(0,s)]
            subgrid = [row[y + j] for j in range(0,s) for row in rows]
            total = sum(subgrid)
            if total > max_power:
                max_power = total
                max_coord = (x,y)
                max_size = s
print (max_power)
print (max_coord,max_size)
