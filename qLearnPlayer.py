from qTable import QTable
import sys

class Player:
    def __init__(self, characterName, hand):
        self.rooms = {
            "Ballroom": 0,
            "Billiard Room": 0,
            "Conservarory": 0,
            "Dining Room": 0,
            "Hall": 0,
            "Kitchen": 0,
            "Library": 0,
            "Lounge": 0,
            "Study": 0
        }
        self.weapons = {
            "Candlestick": 0,
            "Knife": 0,
            "Lead Pipe": 0,
            "Revolver": 0,
            "Rope": 0,
            "Wrench": 0
        }
        self.people = {
            "Mr. Green": 0,
            "Colonel Mustard": 0,
            "Mrs. Peacock": 0,
            "Professor Plum": 0,
            "Ms. Scarlet": 0,
            "Mrs. White": 0
        }

        self.character = characterName
        self.cards = hand

        if self.character == "Mr. Green":
            self.location = (24, 9)
        elif self.character == "Colonel Mustard":
            self.location = (7, 23)
        elif self.character == "Mrs. Peacock":
            self.location = (18, 0)
        elif self.character == "Professor Plum":
            self.location = (5, 0)
        elif self.character == "Ms. Scarlet":
            self.location = (0, 16)
        else:
            self.location = (24, 14)

        self.qtable = QTable(self.rooms, self.weapons, self.people, self.location)

        for i in self.cards:
            if i in self.rooms:
                self.rooms[i] = 1
            elif i in self.weapons:
                self.weapons[i] = 1
            else:
                self.people[i] = 1


    def get_valid_moves(self, board, doors, roll, loc, other_players):
        moves = []
        room = board[loc[0]][loc[1]]

        if roll == 0:
            return moves
        
        #if in room check for passages
        if room == 1:
            moves.append((18, 19))
        elif room == 9:
            moves.append((3, 6))
        elif room == 3:
            moves.append((19,4))
        elif room == 7:
            moves.append((5,17))
        
        #if in a room addd all possible moves out of doors
        if room != -1 and room != 0:
            for i in doors:
                if i[1] == room:
                    if roll == 1:
                        moves.append(i[0])
                    else:
                        moves = moves + self.get_valid_moves(board, doors, roll-1, (i[0]), other_players)

        
        #if in hallway walk around
        if room == 0:
            a, b = loc
            if a < 24 and board[a+1][b] == 0:
                if roll == 1:
                    moves.append((a+1, b))
                else:
                    moves = moves + self.get_valid_moves(board, doors, roll-1, (a+1, b), other_players)

            if a > 0 and board[a-1][b] == 0:
                if roll == 1:
                    moves.append((a-1, b))
                else:
                    moves = moves + self.get_valid_moves(board, doors, roll-1, (a-1, b), other_players)

            if b < 23 and board[a][b+1] == 0:
                if roll == 1:
                    moves.append((a, b+1))
                else:
                    moves = moves + self.get_valid_moves(board, doors, roll-1, (a, b+1), other_players)

            if b > 0 and board[a][b-1] == 0:
                if roll == 1:
                    moves.append((a, b-1))
                else:
                    moves = moves + self.get_valid_moves(board, doors, roll-1, (a, b-1), other_players)

            #if neighbor square is a door go in room
            for i in doors:
                if (a+1, b) == i[2] or (a-1, b) == i[2] or (a, b+1) == i[2] or (a, b-1) == i[2]:
                    moves.append(i[2])
                    break
            
        moves = list(set(moves))
        # do not allow players to be in same hallway tile
        for i in other_players:
            if board[i.location[0]][i.location[1]] == 0 and i.location in moves:
                moves.remove(i.location)

        return moves


    def make_move(self, board, doors, roll, loc, other_players):
        '''
            actions where you win should get a large positive reward
            actions where you lose should get a large negative reward
            actions where you learn something should get a small positive reward
            actions where nothing interesting happens should get no reward
        '''

        moves = self.get_valid_moves(board, doors, roll, loc, other_players)
        solution_guesses = self.get_solution_guesses()
        actions = self.get_valid_actions(board, moves, solution_guesses)

        #make state variable
        state = self.get_state()
        print(state)
        # state = (r, w, p, board[self.location[0]][self.location[1]])
        
        print(self.qtable.table[state][actions[1]])

        
        sys.exit()
        
        #select action
        max_r = self.qtable.table[state][actions[0]]
        a = actions[0]
        for i in actions:
            if self.qtable.table[state][i] > max_r:
                max_r = self.qtable.table[state][i]
                a = i

        #make move

        #get new state
        #get new state's best action


        learning_rate = .8
        discount_factor = .95

        #update q value
        self.qtable.table[state][a] = (1-learning_rate)*self.qtable.table[state][a] + learning_rate*(reward(state, a) + discount_factor*self.qtable.table[new_state][new_action])
    


    def get_valid_actions(self, board, moves, solution_guesses):
        actions = []
        for i in moves:
            #accusations available for that move
            accusations = self.get_valid_accusations(board, i)
            for j in accusations:
                #actions.append((i, 'a', j))
                actions.append(('a', j))
            
            #solution guesses
            for j in solution_guesses:
                #actions.append((i, 's', j))
                actions.append(('s', j))

            #can do nothing if in hallway
            if board[i[0]][i[1]] == 0:
                #actions.append((i, 'n', (0, 0, 0)))
                actions.append(('n', (0, 0, 0)))
        return actions


    def get_state(self):
        r = []
        for i in self.rooms:
            if self.rooms[i] == 1:
                r.append(i)
        r = tuple(r)

        w = 0
        for i in self.weapons:
            w += self.weapons[i]

        p = 0
        for i in self.people:
            p += self.people[i]
        
        return (r, w, p)


    def get_valid_accusations(self, board, loc):
        room = board[loc[0]][loc[1]]
        
        if room == 1:
            room = "Study"
        elif room == 2:
            room = "Hall"
        elif room == 3:
            room = "Lounge"
        elif room == 4:
            room = "Library"
        elif room == 5:
            room = "Dining Room"
        elif room == 6:
            room = "Billiard Room"
        elif room == 7:
            room = "Conservatory"
        elif room == 8:
            room = "Ballroom"
        else:
            room = "Kitchen"

        w = []
        for key in self.weapons:
            w.append(key)
        
        p = []
        for key in self.people:
            p.append(key)

        accusations = []
        
        for i in w:
            for j in p:
                accusations.append((room, i, j))
        return accusations
        

    def get_solution_guesses(self):
        r = []
        for key in self.rooms:
            r.append(key)

        w = []
        for key in self.weapons:
            w.append(key)
        
        p = []
        for key in self.people:
            p.append(key)

        solutions = []

        for i in r:
            for j in w:
                for k in p:
                    solutions.append((i, j, k))

        return solutions

    #might want to redo this to make it better - not sure how at the moment
    def acc_respond(self, accusation):
        has = []
        if accusation[0] in self.cards:
            has.append(accusation[0])
        if accusation[1] in self.cards:
            has.append(accusation[1])
        if accusation[2] in self.cards:
            has.append(accusation[2])
        
        if len(has) == 0:
            return None
        else:
            return has[random.randint(0, len(has)-1)]

    def record_cards(self, hand):
        for i in hand:
            if i in self.rooms:
                self.rooms[i] = 1
            elif i in self.weapons:
                self.weapons[i] = 1
            else:
                self.people[i] = 1

    def __repr__(self):
        return "Player(\""+self.character+"\")"

    def __str__(self):
        return self.character