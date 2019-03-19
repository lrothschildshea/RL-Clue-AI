import random

#this is a bad AI that makes randomish moves but can at least play the game

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

    # makes random move at the moment
    def make_move(self, board, doors, roll, loc, other_players):
        if self.should_guess_solution():
            return self.get_soln_guess()

        moves = self.get_valid_moves(board, doors, roll, loc, other_players)

        #if no moves then the player has been boxed in by other players. Game does not seem to be defined for this behavior so do not move.
        if len(moves) != 0:
            self.location = moves[random.randint(0, len(moves)-1)]

        if board[self.location[0]][self.location[1]] > 0:
            acc = self.make_accusation(board)
            
            #move accused player to room
            for i in other_players:
                if i.character == acc[2]:
                    i.location = self.location
                    break

            #ask other players for a card
            for i in other_players:
                response = i.acc_respond(acc)
                if response != None:
                    self.record_cards([response])
                    break
        return None

        
    
    #makes random accusation from room asking for things it doesnt know
    def make_accusation(self, board):
        room = board[self.location[0]][self.location[1]]
        
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
            if self.weapons[key] == 0:
                w.append(key)
        
        p = []
        for key in self.people:
            if self.people[key] == 0:
                p.append(key)
        
        return (room, w[random.randint(0, len(w)-1)], p[random.randint(0, len(p)-1)])
        

    #show random card from accusation if you have one
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

    def should_guess_solution(self):
        count = 3
        for i in self.rooms:
            count += self.rooms[i]
        for i in self.weapons:
            count += self.weapons[i]
        for i in self.people:
            count += self.people[i]

        if count < 12:
            return False
        return random.random()**100 > ((21-count)**.2)/(21**.2)
    
    def get_soln_guess(self):
        r = []
        for key in self.rooms:
            if self.rooms[key] == 0:
                r.append(key)

        w = []
        for key in self.weapons:
            if self.weapons[key] == 0:
                w.append(key)
        
        p = []
        for key in self.people:
            if self.people[key] == 0:
                p.append(key)
        
        return (r[random.randint(0, len(r)-1)], w[random.randint(0, len(w)-1)], p[random.randint(0, len(p)-1)])

    def record_cards(self, hand):
        for i in hand:
            if i in self.rooms:
                self.rooms[i] = 1
            elif i in self.weapons:
                self.weapons[i] = 1
            else:
                self.people[i] = 1

    def __repr__(self):
        return "Player("+self.character+")"

    def __str__(self):
        return self.character