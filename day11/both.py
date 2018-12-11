import numpy as np
from scipy import signal

def calc_power_level(x,y):
    rack_id = x + 11 # rack_id's are 1-indexed, not 0-indexed
    power = rack_id * (y + 1)
    power += serial_number
    power = power * rack_id
    if len(str(power)) > 2:
        power = int(str(power)[-3]) - 5
    else:
        power = -5
    return power

serial_number = 5235 # the only input
grid = np.array([[calc_power_level(x,y) for y in range(0,300)] for x in range(0,300)],dtype=int)

def convolve_power_levels(grid,size):
    #  why does scipy have two different 2d convolution functions?
    # and why does the one this blog post says is 2x faster, perform 2x slower for me?
    # http://blog.rtwilson.com/convolution-in-python-which-function-to-use/
    sums = signal.convolve2d(grid,np.ones([size,size]),mode='valid')
    (x_max,y_max) = np.unravel_index(np.argmax(sums, axis=None), sums.shape)
    return (x_max + 1,y_max + 1, int(sums[x_max][y_max]), size)

(x,y,power,size) = convolve_power_levels (grid,3)
print ('Answer 1: Coord {x},{y} has total power {power}.').format(**locals())
print(x,y)

# while this will work for convolving using every possible size up to 300,
# observing the output it looks like the max cell at each size starts becoming
# negative somewhere between size 15-25. this makes sense since the average value
# in any given cell is -0.5, so adding more cells _in general_ should hurt the power
# This will complete in ~2 seconds, the full run will take a few minutes
(x,y,power,size) = max([convolve_power_levels(grid,s) for s in range(3,30)], key=lambda x:x[2])

print ('Answer 2: Coord {x},{y} has total power {power} using size {size}.').format(**locals())
print (x,y,size)
