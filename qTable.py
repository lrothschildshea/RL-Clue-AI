from itertools import combinations
from itertools import product
from ast import literal_eval as make_tuple
import sys, time

class QTable:
    def __init__(self, rooms, weapons, people, location):
        self.table = {}

        try:
            print("reading file...")
            t1 = time.time()
            loadable = self.read_table()
            if loadable is not None:
                self.table = loadable
                self.states = list(loadable.keys())
                self.actions = list(loadable[self.states[0]].keys())
            t2 = time.time()
            print("time: %.4f" % (t2 - t1))

        except FileNotFoundError as e:
            # Generate all combinations of rooms
            all_rooms = []
            for i in range(len(rooms)):
                cmb = combinations(rooms, i)
                all_rooms += cmb

            # Take cartesian product of guessable values for guesses
            guesses = product(rooms.keys(), weapons.keys(), people.keys())

            # Pair cartesian product of guesses with action type
            print('making actions...')
            self.actions = [(i, 'n', ('0', '0', '0')) for i in range(10)] + list(product(range(10), ['a', 's'], guesses))

            # Create state space value of rooms, weapon count, and people count
            # location omitted at this time for smaller space
            print('making states...')
            self.states = list(product(all_rooms, list(range(len(weapons))), list(range(len(people)))))

            # Create the keys to be used in the QTable dictionary
            print('making q_states...')
            q_states = product(self.states, self.actions)
            for s in self.states:
                self.table[s] = {}
                for a in self.actions:
                    self.table[s][a] = 0

            print('writing to file...')
            self.write_table()
        # sys.exit()

    def write_table(self, filename="qtable_init.tsv"):
        first_line = True
        head = ["-"]

        with open(filename, 'w') as file:
            for (state, actions) in self.table.items():
                line = [str(state)]
                for (action, value) in actions.items():
                    if first_line:
                        head.append(str(action))
                    line.append(str(value))

                if first_line:
                    file.write("%s\n" % ("\t".join(head)))
                    first_line = False
                file.write("%s\n" % ("\t".join(line)))

    def read_table(self, filename="qtable_init.tsv"):
        tstart = time.time()
        tcur = tstart
        first_line = True
        table = {}
        actions = []
        count = 0
        with open(filename, 'r') as file:
            for line in file:
                if first_line:
                    actions = line.split("\t")[1:]
                    first_line = False
                else:
                    line_data = line.split("\t")
                    state = make_tuple(line_data[0])
                    values = line_data[1:]
                    if state not in table.keys():
                        table[state] = {}

                    for (i, a) in enumerate(actions):
                        action = make_tuple(a)
                        table[state][action] = float(values[i])

                count += 1
                t = time.time()
                if (t - tcur) > 15:
                    print("%d lines (%.4fs)" % (count , t - tstart))
                    tcur = t

        return table
