import re

class Army:
    def __init__(self, input_group_lines, team, boost):
        self.groups = [Group(i, l, team, boost) for i,l in enumerate(input_group_lines) if l != '']
        self.team = team
        self.alive = True

class Group:
    def __init__(self, i, input_row, team, boost):
        # Example: '2321 units each with 10326 hit points (immune to slashing) with an attack that does 42 fire damage at initiative 4'
        regex = '^(\d+) units each with (\d+) hit points(.*?)with an attack that does (\d+) (.*?) damage at initiative (\d+)$'
        (units, hp, abilities, attack, self.type, initiative) = re.findall(regex,input_row)[0]

        self.id = i
        self.team = team
        self.hp = int(hp)
        self.alive = True
        self.under_attack = False

        self.units = int(units)
        self.attack = int(attack) + boost
        self.power = self.units * self.attack

        self.initiative = int(initiative)

        self.weaknesses = []
        self.immunities = []

        # this is pretty yucky string mangling, but :shrug: it's christmas eve
        # split immunities and weaknesses (either can come first)
        abilities = abilities.replace('(','').replace(')','').split(';')
        for ability in abilities:
            if 'immune' in ability.split(' '):
                self.immunities.extend([c.strip() for c in ability.replace('immune to ', '').split(', ')])
            elif 'weak' in ability.split(' '):
                self.weaknesses.extend([c.strip() for c in ability.replace('weak to ', '').split(', ')])

    def attacked(self,damage):
        self.units = max(self.units - damage // self.hp,0)
        if self.units == 0:
            self.alive = False
        else:
            self.power = self.units * self.attack

def order_groups(groups):
    # order by power, use intitative to break ties
    return sorted(sorted(groups, key=lambda group:group.initiative, reverse=True), key=lambda group:group.power, reverse=True)

def calculate_damage(attacker, defender):
    if attacker.type in defender.immunities:
        return 0
    if attacker.type in defender.weaknesses:
        return attacker.power * 2
    else:
        return attacker.power

def target_selection(attacking_army, defending_army):
    attacks = []
    for attacker in [g for g in order_groups(attacking_army.groups) if g.alive == True]:
        max_attack = 0
        to_attack = None
        for defender in [g for g in order_groups(defending_army.groups) if g.under_attack == False and g.alive == True]:
            damage = calculate_damage(attacker,defender)
            if damage > max_attack:
                max_attack = damage
                to_attack = defender
        if to_attack != None:
            to_attack.under_attack = True
            # put initiative first for easy sorting later
            attacks.append((attacker.initiative, attacker, to_attack))
    return attacks

def post_fight(army):
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
        damage = calculate_damage(attacker,defender)
        kills = min(damage // defender.hp, defender.units)
        total_kills += kills
        defender.attacked(damage)

    post_fight(army_one)
    post_fight(army_two)

    return total_kills

def battle(immune_system_lines, infection_lines, boost):
    immune_system = Army(immune_system_lines,'Immune System', boost)
    infection = Army(infection_lines,'Infection', 0)

    while (immune_system.alive and infection.alive):
        kills = fight(immune_system,infection)
        # if there are no kills in either direction, we're stuck forever (yes this can happen)
        if (kills == 0):
            return ('No winner',-1)

    winner = [army.team for army in [immune_system,infection] if army.alive == True][0]
    score = max([sum([group.units for group in army.groups]) for army in [immune_system,infection] if army.alive == True])
    return (winner,score)


input = ''.join([l.replace('Immune System','').replace('Infection','') for l in open('input.txt','r').readlines()]).split(':')
immune_system_lines = input[1].split('\n')
infection_lines = input[2].split('\n')

# Part 1
(winner, score) = battle(immune_system_lines,infection_lines,0)

print ('Answer 1:')
print ('{winner} wins with this many units left: {score}').format(**locals())

# Part 2

print ('Answer 2:')
boost = 0
while (winner != 'Immune System'):
    boost += 1
    (winner, score) = battle(immune_system_lines,infection_lines,boost)
print ('Using a boost of {boost}, {winner} wins with this many units left: {score}').format(**locals())
