from qTable import QTable
import sys
import random

class Player:
    def __init__(self, characterName, hand, qtbl):
        self.rooms = {
            "Ballroom": 0,
            "Billiard Room": 0,
            "Conservatory": 0,
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

        self.qtable = qtbl

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
            if (board[i.location[0]][i.location[1]] == 0) and (i.location in moves):
                moves.remove(i.location)

        return moves


    def make_move(self, board, doors, roll, loc, other_players, sol):

        moves = self.get_valid_moves(board, doors, roll, loc, other_players)

        if len(moves) == 0:
            return None

        actions = self.get_valid_actions(board, moves)

        state = self.get_state()
        
        #select action
        max_r = -10000
        a = []
        for i in actions:
            ia = (board[i[0][0]][i[0][1]], i[1], i[2])
            if self.qtable.table[state][ia] > max_r:
                max_r = self.qtable.table[state][ia]
                a = [i]
            elif self.qtable.table[state][ia] == max_r:
                a.append(i)
        #if tie select random move
        a = a[random.randint(0, len(a) - 1)]

        #explore vs exploit
        if random.random() > .98:
            a = actions[random.randint(0, len(actions) - 1)]

        #make move and get reward
        reward = 0
        ret_val = None
        if a[1] == 'n':
            #in hall
            self.location = a[0]
            reward = -5
        elif a[1] == 's':
            #guess solution
            self.location = a[0]
            if sol == a[2]:
                reward = 1000
            else:
                reward = -1000
            ret_val = a[2]
        else:
            #accusation
            self.location = a[0]
            acc = a[2]

            #move accused player to room
            for i in other_players:
                if i.character == acc[2]:
                    i.location = self.location
                    break
            
            learn = False
            #ask other players for a card
            for i in other_players:
                response = i.acc_respond(acc)
                if response != None:
                    learn = True
                    self.record_cards([response])
                    reward = 20
                    break
            if not learn:
                reward = -20
                

        #get new state
        new_state = self.get_state()

        #get all possible next moves
        new_moves = []
        for i in range(1,7):
            new_moves += self.get_valid_moves(board, doors, i, loc, other_players)
        
        new_actions = self.get_valid_actions(board, new_moves)

        #select best possible next action
        new_max_r = -10000
        new_a = []
        for i in new_actions:
            ia = (board[i[0][0]][i[0][1]], i[1], i[2])
            if self.qtable.table[new_state][ia] > new_max_r:
                new_max_r = self.qtable.table[new_state][ia]
                new_a = [i]
            elif self.qtable.table[new_state][ia] == new_max_r:
                new_a.append(i)
        new_action = new_a[random.randint(0, len(new_a) - 1)]

        #generalize actions
        a = (board[a[0][0]][a[0][1]], a[1], a[2])
        new_action = (board[new_action[0][0]][new_action[0][1]], new_action[1], new_action[2])

        learning_rate = .8
        discount_factor = .95

        #update q value
        self.qtable.table[state][a] = (1-learning_rate)*self.qtable.table[state][a] + learning_rate*(reward + discount_factor*self.qtable.table[new_state][new_action])

        return ret_val
    

    def get_valid_actions(self, board, moves):
        #returns using specific location which is later generalized
        solution_guesses = self.get_solution_guesses()
        actions = []
        #an action is = (loc_tup, 'type', guess_tup)
        for i in moves:
            #accusations available for that move
            accusations = self.get_valid_accusations(board, i)
            for j in accusations:
                if board[i[0]][i[1]] > 0:
                    actions.append((i, 'a', j))
                    #actions.append(('a', j))
            
            #solution guesses
            for j in solution_guesses:
                actions.append((i, 's', j))
                #actions.append(('s', j))

            #can do nothing if in hallway
            if board[i[0]][i[1]] == 0:
                actions.append((i, 'n', ('0', '0', '0')))
                #actions.append(('n', (0, 0, 0)))
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
        solutions = []
        for i in self.rooms:
            for j in self.weapons:
                for k in self.people:
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