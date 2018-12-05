units = list(''.join(open('input.txt','r').readlines()).strip())

def compare_chars(c1,c2):
    return c1.isupper() != c2.isupper() and c1.lower() == c2.lower()

def react_polymer(units):
    polymer = []
    for unit in units:
        if len(polymer) == 0:
            polymer.append(unit)
        elif compare_chars(polymer[-1],unit):
            polymer.pop()
        else:
            polymer.append(unit)
    return polymer

print ('Answer 1:')
print (len(react_polymer(units)))

import string
alphabet = list(string.ascii_lowercase)

def clean_polymer(units,to_remove):
    return [c for c in units if c.lower() != to_remove.lower()]

print ('Answer 2:')
print (min([len(react_polymer(clean_polymer(units,c))) for c in alphabet]))
