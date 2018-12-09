import re
from blist import *

# haven't used blist before - pretty sweet perf upgrade
# https://pypi.org/project/blist/

# Use Case                                  blist             list
# Insertion into or removal from a list     O(log n)          O(n) <--- this is what we needed
# Taking slices of lists                    O(log n)          O(n)
# Making shallow copies of lists            O(1)              O(n)
# Changing slices of lists                  O(log n + log k)  O(n+k)
# Multiplying a list to make a sparse list  O(log k)          O(kn)

regex = '(.*) players; last marble is worth (.*) points'
(num_players, num_marbles) = map(int,re.findall(regex,open('input.txt','r').read())[0])

def find_winner(num_players,num_marbles):
    players = [0 for i in range(num_players)]
    circle = blist([])
    current_index = 0

    for i in range(num_marbles + 1):
        current_player = i % num_players
        if i == 0:
            circle.append(i)
            current_index = i
        elif i % 23 == 0:
            current_index = (current_index - 8) % len(circle) + 1
            removed = circle.pop(current_index)
            players[current_player] += (removed + i)
        else:
            current_index = (current_index + 1) % len(circle) + 1
            circle.insert(current_index,i)
    return max(players)

print('Answer 1:')
print(find_winner(num_players,num_marbles))

print('Answer 2:')
print(find_winner(num_players,num_marbles * 100))
