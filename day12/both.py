import re

class Pot:
    def __init__(self, position, state):
        self.position = position
        self.state = state

class RowOfPots:
    def __init__(self, initial_state_string, rules):
        initial_state = initial_state_string.replace('initial state: ','')
        self.pots = {i:Pot(i,c) for i,c in enumerate(initial_state)}
        self.rules = rules
        self.total = 0
        self.update_pot_range()
        self.update_pot_id_total()

    def update_pot_range(self):
        self.leftmost_pot = min([self.pots[i].position for i in self.pots.keys() if self.pots[i].state == '#'])
        self.rightmost_pot = max([self.pots[i].position for i in self.pots.keys() if self.pots[i].state == '#'])

    def update_pot_id_total(self):
        self.total = sum([self.pots[i].position for i in self.pots.keys() if self.pots[i].state == '#'])

    def print_pots(self):
        print (''.join([state for (pot_id,state) in sorted([(pot_id,self.pots[pot_id].state) for pot_id in self.pots])]))

    def tick(self):
        # Make sure we have "empty" pots to the left and right of the pots we want to check
        for i in range(self.leftmost_pot - 4, self.rightmost_pot + 5):
            if i not in self.pots:
                self.pots[i] = Pot(i,'.')

        # store changes to be applied after analyzing every pot
        changes = {}

        # look 2 to the left / right of our edge pots to see if they grow this generation
        for i in range(self.leftmost_pot - 2, self.rightmost_pot + 3):
            input = ''.join(map(str,[self.pots[j].state for j in range(i - 2, i + 3)]))
            outcome = [rule.outcome for rule in self.rules if rule.input == input]
            if len(outcome) == 0:
                changes[i] = '.'
            else:
                changes[i] = outcome[0]

        for i in changes:
            self.pots[i].state = changes[i]

        self.update_pot_range()
        self.update_pot_id_total()
        #self.print_pots()

class Rule:
    def __init__(self, rule_string):
        # Example: ##.## => #
        regex = '(.*) => (.*)'
        (self.input,self.outcome) = re.findall(regex,rule_string)[0]

lines = [l.strip() for l in open('input.txt','r').readlines()]
pots = RowOfPots(lines[0], [Rule(l) for l in lines[2:]])

# keep track of the change from one generation to the next, wait for it to stabilize
last_total = pots.total
deltas = []
for i in range(1,101):
    pots.tick()

    if (i == 20):
        print('Answer 1:')
        print(pots.total)

    delta = pots.total - last_total
    last_total = pots.total
    deltas.append(delta)

    if (i > 20 and all([d == delta for d in deltas[-3:]])):
        break

print('Constant rate of increase found:',deltas[-1],'plants per generation')
print('After',i,'generations, we have',last_total,'plants.')
print('So after',i + 1,'generations, we have',last_total + 1 * deltas[-1],'plants.')
print('And after',50000000000,'generations, we have',last_total + (50000000000-i) * deltas[-1],'plants.')

print('Answer 2:')
print(last_total + (50000000000-i) * deltas[-1])
