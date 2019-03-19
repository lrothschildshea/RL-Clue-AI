from itertools import combinations
from itertools import product
import sys

class QTable:
    def __init__(self, rooms, weapons, people, location):
        self.table = {}

        # Generate all combinations of rooms
        all_rooms = []
        for i in range(len(rooms) + 1):
            cmb = combinations(rooms, i)
            all_rooms += cmb

        guesses = product(rooms.keys(), weapons.keys(), people.keys())
        self.actions = list(product(['a', 's'], guesses))
        self.states = list(product(all_rooms, list(range(len(weapons) + 1)), list(range(len(people) + 1))))
        q_states = product(self.states, self.actions)
        i = 0
        for (s, a) in q_states:
            self.table[(s, a)] = 0

        print(len(self.table))