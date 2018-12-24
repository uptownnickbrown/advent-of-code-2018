import re

class Army:
    def __init__(self, input_group_lines, team, boost):
        self.groups = [Group(l,i,team,boost) for i,l in enumerate(input_group_lines) if l != '']
        self.team = team
        self.alive = True

    def status(self):
        print (self.team)
        for group in self.groups:
            if group.units > 0:
                print ('Group {group.id} contains {group.units} units').format(**locals())
        print ('\n')

class Group:
    def __init__(self, input_row, i, team, boost):
        # Example: '2321 units each with 10326 hit points (immune to slashing) with an attack that does 42 fire damage at initiative 4'
        regex = '^(\d+) units each with (\d+) hit points(.*?)with an attack that does (\d+) (.*?) damage at initiative (\d+)$'
        (units, hp, characteristics, attack, self.type, initiative) = re.findall(regex,input_row)[0]

        self.id = i
        self.team = team
        self.hp = int(hp)
        self.alive = True

        self.units = int(units)
        self.attack = int(attack) + boost
        self.power = self.units * self.attack

        self.initiative = int(initiative)

        self.weaknesses = []
        self.immunities = []

        # this is pretty yucky string mangling, but :shrug: it's christmas eve
        characteristics = characteristics.replace('(','').replace(')','').split(';')
        for characteristic in characteristics:
            if 'immune' in characteristic.split(' '):
                self.immunities.extend([c.strip() for c in characteristic.replace('immune to ', '').split(', ')])
            elif 'weak' in characteristic.split(' '):
                self.weaknesses.extend([c.strip() for c in characteristic.replace('weak to ', '').split(', ')])

        self.under_attack = False

    def attacked(self,damage):
        self.units = max(self.units - damage // self.hp,0)
        if self.units == 0:
            self.alive = False
        else:
            self.power = self.units * self.attack

    def __str__(self):
        return ('''
{self.team} Group {self.id} stats:
Units: {self.units}
HP: {self.hp}

Initiative: {self.initiative}
Type: {self.type}
Attack: {self.attack}
Power: {self.power}

Weaknesses: {self.weaknesses}
Immunities: {self.immunities}

''').format(**locals())

def actual_attack_power(attacking_group, defending_group):
    if attacking_group.type in defending_group.immunities:
        return 0
    if attacking_group.type in defending_group.weaknesses:
        return attacking_group.power * 2
    else:
        return attacking_group.power

def order_groups(groups):
    return sorted(sorted(groups, key=lambda group:group.initiative, reverse=True), key=lambda group:group.power, reverse=True)

def target_selection(attacking_army, defending_army):
    attacks = []
    for attacker in [group for group in order_groups(attacking_army.groups) if group.alive == True]:
        max_attack = 0
        to_attack = None
        for defender in [group for group in order_groups(defending_army.groups) if group.under_attack == False and group.alive == True]:
            damage = actual_attack_power(attacker,defender)
            # To log exactly like the sample:
            print ('{attacker.team} group {attacker.id} would deal defending group {defender.id} {damage} damage').format(**locals())
            if damage > max_attack:
                max_attack = damage
                to_attack = defender
        if to_attack != None:
            to_attack.under_attack = True
            attacks.append((attacker.initiative, attacker, to_attack))
    return attacks

def post_fight_status(army):
    if all([group.alive == False for group in army.groups]):
        army.alive = False

    for group in army.groups:
        group.under_attack = False

def fight(army_one, army_two):
    attacks = []
    attacks.extend(target_selection(army_two,army_one))
    attacks.extend(target_selection(army_one,army_two))

    total_kills = 0
    for attack in sorted(attacks, reverse=True):
        (_, attacker, defender) = attack
        damage = actual_attack_power(attacker,defender)
        kills = min(damage // defender.hp,defender.units)
        total_kills += kills
        # To log exactly like the sample:
        print ('{attacker.team} group {attacker.id} attacks defending group {defender.id}, killing {kills} units').format(**locals())
        defender.attacked(damage)

    post_fight_status(army_one)
    post_fight_status(army_two)

    return total_kills

def battle(immune_system_lines, infection_lines, boost):
    immune_system = Army(immune_system_lines,'Immune System', boost)
    infection = Army(infection_lines,'Infection', 0)

    while (immune_system.alive and infection.alive):
        # To log exactly like the sample:
        immune_system.status()
        infection.status()
        kills = fight(immune_system,infection)
        immune_system_left = sum([group.units for group in immune_system.groups])
        infection_left = sum([group.units for group in infection.groups])
        print('Immune system: {immune_system_left} vs. Infection: {infection_left}').format(**locals())

        if (kills == 0):
            return ('No winner',-1)

    return ([army.team for army in [immune_system,infection] if army.alive == True][0],max([sum([group.units for group in army.groups]) for army in [immune_system,infection] if army.alive == True]))

input = ''.join([l.replace('Immune System','').replace('Infection','') for l in open('input.txt','r').readlines()]).split(':')

immune_system_lines = input[1].split('\n')
infection_lines = input[2].split('\n')

(winner, score) = battle(immune_system_lines,infection_lines,0)

print ('Answer 1:')
print ('{winner} wins with this many units left: {score}').format(**locals())

print ('Answer 2:')
boost = 0
while (winner != 'Immune System'):
    boost += 1
    (winner, score) = battle(immune_system_lines,infection_lines,boost)
    print ('Using boost: {boost}, {winner} wins with this many units left: {score}').format(**locals())
print ('Using boost: {boost}, {winner} wins with this many units left: {score}').format(**locals())
