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

counter = 0
print("Starting")
for i in states:
    counter += 1
    if (counter % 1000) == 0:
        print("State #:", counter)

    for j in table[i]:
        total += table[i][j]
        count += 1
        if table[i][j] == 0:
            zero += 1
        else:
            nonzero += 1


print("Total Q:", total)
print("Num Zeros:", zero)
print("Num Non-zeros:", nonzero)
print("Number of entries:", count)

