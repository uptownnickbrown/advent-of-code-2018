from blist import *

def new_recipes(recipe_list,elf_one,elf_two):
    return map(int,list(str(recipe_list[elf_one] + recipe_list[elf_two])))

def cook_next(recipe_list,elf_one,elf_two):
    elf_one_steps = recipe_list[elf_one] + 1
    elf_one = (elf_one + elf_one_steps) % len(recipe_list)
    elf_two_steps = recipe_list[elf_two] + 1
    elf_two = (elf_two + elf_two_steps) % len(recipe_list)
    return (elf_one,elf_two)

def tick(recipe_list,elf_one,elf_two):
    to_add = new_recipes(recipe_list,elf_one,elf_two)
    recipe_list.extend(to_add)
    (elf_one,elf_two) = cook_next(recipe_list,elf_one,elf_two)
    return (recipe_list,elf_one,elf_two)

def next_ten_after(i):
    recipe_list = [3,7]
    elf_one = 0
    elf_two = 1
    while (len(recipe_list) < i + 10):
        (recipe_list,elf_one,elf_two) = tick(recipe_list,elf_one,elf_two)
    return ''.join(map(str,recipe_list[-10:]))

def how_many_until(search):
    recipe_list = blist([3,7])
    elf_one = 0
    elf_two = 1

    while (len(recipe_list) > len(search)):
        (recipe_list,elf_one,elf_two) = tick(recipe_list,elf_one,elf_two)

    while (''.join(map(str,recipe_list[-1 * len(search):])) != search):
        if (len(recipe_list) % 1000000 == 0):
            print (len(recipe_list),'checked')
        (recipe_list,elf_one,elf_two) = tick(recipe_list,elf_one,elf_two)

    return len(recipe_list) - len(search)

print('Answer 1:')
print(next_ten_after(84601))

print('Answer 2:')
print(how_many_until('084601'))
