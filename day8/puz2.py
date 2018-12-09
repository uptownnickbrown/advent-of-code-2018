entries = [int(i) for i in list(open('input.txt').read().split(' ')) if i != ' ']

def evaluate_node(entries):
    child_nodes = entries.pop(0)
    meta_entries = entries.pop(0)
    value = 0
    if child_nodes == 0:
        value += sum([entries.pop(0) for i in range(meta_entries)])
    else:
        children = []
        while (child_nodes > 0):
            children.append(evaluate_node(entries))
            child_nodes -= 1
        value += sum([children[i - 1] for i in [entries.pop(0) for i in range(meta_entries)] if i <= len(children)])
    return value

print ('Answer 2:')
print (evaluate_node(entries))
