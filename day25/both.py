import networkx as nx
import matplotlib.pyplot as plt

class Star:
    def __init__(self, row):
        (self.t, self.x, self.y, self.z)= map(int,row.split(','))

    def __str__(self):
        return '''t: {self.t} x: {self.x} y: {self.y} z: {self.z}'''.format(**locals())

class Constellation:
    def __init__(self, star):
        self.stars = [star]

    def __str__(self):
        return 'Stars in constellation:' + str([str(star) for star in self.stars])

stars = [Star(l) for l in open('input.txt','r').readlines()]

def manhattan_distance_4d(s1,s2):
    t_dist = abs(s1.t-s2.t)
    x_dist = abs(s1.x-s2.x)
    y_dist = abs(s1.y-s2.y)
    z_dist = abs(s1.z-s2.z)
    return t_dist + x_dist + y_dist + z_dist

star_map = nx.Graph()

for star in stars:
    star_map.add_node(star)

for star_a in stars:
    for star_b in stars:
        if manhattan_distance_4d(star_a,star_b) < 4:
            star_map.add_edge(star_a, star_b)

# nx.draw(star_map, with_labels=True)
# plt.savefig('star_map.jpg')
# plt.close()

constellations = list(nx.connected_component_subgraphs(star_map))

# for i, constellation in enumerate(constellations):
#     nx.draw(constellation, with_labels=True)
#     plt.savefig('star_map_' + str(i) + '.jpg')
#     plt.close()

print ('Answer 1:')
print (len(constellations))
