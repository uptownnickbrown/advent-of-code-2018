import re

class StepNode:
    def __init__(self, name, dependency = None):
        self.name = name
        self.complete = False
        self.assigned = False
        self.time_to_complete = ord(name) - 4 # ord('A') = 65, we want it to be 61. use -64 instead on test data / example
        self.time_worked = 0
        self.dependencies = []
        if dependency != None:
            self.dependencies.append(dependency)

    def add_dependency(self, dependency = None):
        self.dependencies.append(dependency)

class Worker:
    def __init__(self):
        self.working_on = None

class StepGraph:
    def __init__(self):
        self.nodes = {}
        self.complete = False
        self.time_elapsed = 0
        self.available_nodes = []
        self.workers = [Worker() for i in range(5)] # number of workers, use 2 for test data / example

    def add_node(self,node):
        self.nodes[node.name] = node

    def complete_node(self,node):
        node.complete = True

    def assign_node_to_worker(self,node,worker):
        worker.working_on = node
        node.assigned = True

    def find_available_nodes(self):
        self.available_nodes = []
        # (number of unmet dependencies, node_name) for each uncompleted node
        dep_counts = [(len([d for d in self.nodes[node].dependencies if d.complete == False]),node) for node in self.nodes if self.nodes[node].complete == False]
        if (len(dep_counts) == 0):
            self.complete = True
        else:
            # sort by # of unmet dependencies, then by alphabetic on name
            sorted_dep_counts = sorted(sorted(dep_counts, key=lambda x: x[1]), key=lambda x: x[0])
            for (dep_count,node_name) in sorted_dep_counts:
                if dep_count == 0 and self.nodes[node_name].assigned == False:
                    self.available_nodes.append(self.nodes[node_name])

    def tick(self):
        self.find_available_nodes()
        for available_node in self.available_nodes:
            available_workers = [worker for worker in self.workers if worker.working_on == None]
            if len(available_workers) > 0:
                self.assign_node_to_worker(available_node,available_workers[0])
        for worker in self.workers:
            if worker.working_on != None:
                worker.working_on.time_worked += 1
                if worker.working_on.time_worked == worker.working_on.time_to_complete:
                    worker.working_on.complete = True
                    worker.working_on = None
        if self.complete == False:
            self.time_elapsed += 1

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

while graph.complete == False:
    graph.tick()

print ('Answer 2:')
print (graph.time_elapsed)
