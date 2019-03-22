from itertools import combinations
from itertools import product
import pickle
import sys, time

class QTable:
    def __init__(self, rooms, weapons, people):
        self.table = {}

        try:
            print("reading file...")
            t1 = time.time()
            loadable = self.read_table()
            if loadable is not None:
                self.table = loadable
                #self.states = list(loadable.keys())
                #self.actions = list(loadable[self.states[0]].keys())
            t2 = time.time()
            print("time: %.4f" % (t2 - t1))

        except FileNotFoundError as e:
            # Generate all combinations of rooms
            all_rooms = []
            for i in range(len(rooms)):
                cmb = combinations(rooms, i)
                all_rooms += cmb

            all_weapons = []
            for i in range(len(weapons)):
                cmb = combinations(weapons, i)
                all_weapons += cmb

            all_people = []
            for i in range(len(people)):
                cmb = combinations(people, i)
                all_people += cmb

            # Take cartesian product of guessable values for guesses
            guesses = product(rooms, weapons, people)

            # Pair cartesian product of guesses with action type
            print('making actions...')
            noguess = [('n', ('0', '0', '0'))]

            solves  = list(product(['a', 's'], guesses))
            self.actions = noguess + solves

            # Create state space value of rooms, weapon count, and people count
            # location omitted at this time for smaller space
            print('making states...')
            self.states = list(product(all_rooms, all_weapons, list(range(len(people)))))

            print(len(self.actions))

            # Create the keys to be used in the QTable dictionary
            # q_states = product(self.states, self.actions)
            #for s in product(self.states, self.actions):
                #self.table[s] = 0
            for s in self.states:
                self.table[s] = {}
                for a in self.actions:
                    self.table[s][a] = 0

            print('writing to file...')
            self.write_table()
        # sys.exit()

    def write_table(self, filename="qtable_init"):
        pickle_out = open(filename+".pickle","wb")
        pickle.dump(self.table, pickle_out)
        pickle_out.close()

    def read_table(self, filename="qtable_init"):
        pickle_in = open(filename+".pickle","rb")
        table = pickle.load(pickle_in)
        return table
