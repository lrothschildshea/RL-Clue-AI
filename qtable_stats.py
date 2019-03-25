from qTable import QTable
from itertools import combinations
from itertools import product
import pickle

rooms = ["Study", "Hall", "Lounge", "Library", "Dining Room", "Billiard Room", "Conservatory", "Ballroom", "Kitchen"]
weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
characters = ["Mr. Green", "Colonel Mustard", "Mrs. Peacock", "Professor Plum", "Ms. Scarlet", "Mrs. White"]

all_rooms = []
for i in range(len(rooms)):
    cmb = combinations(rooms, i)
    all_rooms += cmb

    all_weapons = []
    for i in range(len(weapons)):
        cmb = combinations(weapons, i)
        all_weapons += cmb

    all_people = []
    for i in range(len(characters)):
        cmb = combinations(characters, i)
        all_people += cmb

states = list(product(all_rooms, all_weapons, all_people))

for i in states:
    if (len(i[0]) + len(i[1]) + len(i[2])) < 3:
        states.remove(i)

pickle_in = open("qtable_init.pickle","rb")
table = pickle.load(pickle_in)


total = 0
zero = 0
nonzero = 0
count = 0

for i in states:
    for j in table[i]:
        total += table[i][j]
        count += 1
        if table[i][j] != 0:
            zero += 1
        else:
            nonzero += 1


print(total)
print(zero)
print(nonzero)
print(count)
