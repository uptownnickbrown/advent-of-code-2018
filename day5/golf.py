units = list(open('input.txt').read().strip())
alpha = 'abcdefghijklmnopqrstuvwxyz'
def react(units):
    poly = []
    for u in units:
        if len(poly) == 0:
            poly.append(u)
        elif poly[-1].isupper() != u.isupper() and poly[-1].lower() == u.lower():
            poly.pop()
        else:
            poly.append(u)
    return poly
print (len(react(units)))
print (min([len(react([u for u in units if u.lower() != char.lower()])) for char in alpha]))
