entries = [int(i) for i in list(open('input.txt').read().split(' ')) if i != ' ']

def sum_metadata(entries):
    child_nodes = entries.pop(0)
    meta_entries = entries.pop(0)
    total = 0
    while (child_nodes > 0):
        total += sum_metadata(entries)
        child_nodes -= 1
    total += sum([entries.pop(0) for i in range(meta_entries)])
    return total

print ('Answer 1:')
print (sum_metadata(entries))
