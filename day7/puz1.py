import re

class StepNode:
    def __init__(self, name, dependency = None):
        self.name = name
        self.complete = False
        self.dependencies = []
        if dependency != None:
            self.dependencies.append(dependency)

    def add_dependency(self,dependency = None):
        self.dependencies.append(dependency)

class StepGraph:
    def __init__(self):
        self.nodes = {}
        self.complete = False
        self.next_node = None

    def add_node(self,node):
        self.nodes[node.name] = node

    def complete_node(self,node):
        node.complete = True

    def find_next_node(self):
        # (number of unmet dependencies, node_name) for each uncompleted node
        dep_counts = [(len([d for d in self.nodes[node].dependencies if d.complete == False]),node) for node in self.nodes if self.nodes[node].complete == False]
        if (len(dep_counts) == 0):
            self.complete = True
            self.next_node = None
        else:
            # sort by # of unmet dependencies, then by alphabetic on name
            sorted_dep_counts = sorted(sorted(dep_counts, key=lambda x: x[1]), key=lambda x: x[0])
            next_node_name = sorted_dep_counts[0][1]
            self.next_node = self.nodes[next_node_name]

graph = StepGraph()

for step in open('input.txt','r').readlines():
    # Example: 'Step A must be finished before step D can begin.'
    regex = 'Step (.) must be finished before step (.) can begin.'
    (dependency_name,downstream_name) = re.findall(regex,step)[0]

    if dependency_name not in graph.nodes:
        graph.add_node(StepNode(dependency_name))
    dependency_node = graph.nodes[dependency_name]

    if downstream_name not in graph.nodes:
        graph.add_node(StepNode(downstream_name, dependency = dependency_node))
    else:
        graph.nodes[downstream_name].add_dependency(dependency_node)

# the graph is complete, find our first node
graph.find_next_node()

result = []
while graph.complete == False:
    result.append(graph.next_node.name)
    graph.complete_node(graph.next_node)
    graph.find_next_node()

print ('Answer 1:')
print (''.join(result))
