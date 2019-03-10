from cards import Cards
from player import Player
import random

class Game:

    numPlayers = 2
    currentPlayer = 0
    solution_guessed = False

    rooms = ["Ballroom", "Billiard Room", "Conservatory", "Dining Room", "Hall", "Kitchen", "Library", "Lounge", "Study"]
    weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
    characters = ["Mr. Green", "Colonel Mustard", "Mrs. Peacock", "Professor Plum", "Ms. Scarlet", "Mrs. White"]

    def __init__(self, numberOfPlayers):
        if numberOfPlayers > 1 and numberOfPlayers < 7:
            self.numPlayers = numberOfPlayers
        
        self.cards, self.solution = Cards(self.numPlayers).deal_cards()
        self.players = []
        for i in range(self.numPlayers):
            self.players.append(Player(self.characters[i], self.cards[i]))

        self.board = self.init_board()
        
        #door = (hall_loc, room_num, room_loc)
        self.doors = [((4, 6), 1, (3, 6)), ((4, 8), 2, (4, 9)), ((7, 11), 2, (6, 11)), ((7, 12), 2, (6, 12)), ((6, 17), 3, (5, 17)), ((8, 7), 4, (8, 6)), ((11, 3), 4, (10, 3)), ((8, 17), 5, (9, 17)), ((12, 15), 5, (12, 16)), ((11, 1), 6, (12, 1)), ((15, 6), 6, (15, 5)), ((19, 5), 7, (19, 4)), ((19, 7), 8, (19, 8)), ((16, 9), 8, (17, 9)), ((16, 14), 8, (17, 14)), ((19, 16), 8, (19, 15)), ((17, 19), 9, (18, 19))]

        




    #todo
    def run_game(self):
        return
            



    def roll_dice(self):
        return random.randint(1, 6)



    def init_board(self):
        #-1 = no space  0 = hallway     num=room
        board = [None]*25
        board[0] = [1,1,1,1,1,1,-1,0,-1,-1,-1,-1,-1,-1,-1,-1,0,-1,3,3,3,3,3,3]
        board[1] = [1,1,1,1,1,1,1,0,0,2,2,2,2,2,2,0,0,3,3,3,3,3,3,3]
        board[2] = [1,1,1,1,1,1,1,0,0,2,2,2,2,2,2,0,0,3,3,3,3,3,3,3]
        board[3] = [1,1,1,1,1,1,1,0,0,2,2,2,2,2,2,0,0,3,3,3,3,3,3,3]
        board[4] = [-1,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,3,3,3,3,3,3,3]
        board[5] = [0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,3,3,3,3,3,3,3]
        board[6] = [-1,4,4,4,4,4,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,-1]
        board[7] = [4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        board[8] = [4,4,4,4,4,4,4,0,0,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,-1]
        board[9] = [4,4,4,4,4,4,4,0,0,-1,-1,-1,-1,-1,0,0,5,5,5,5,5,5,5,5]
        board[10] = [-1,4,4,4,4,4,0,0,0,-1,-1,-1,-1,-1,0,0,5,5,5,5,5,5,5,5]
        board[11] = [-1,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,0,0,5,5,5,5,5,5,5,5]
        board[12] = [6,6,6,6,6,6,0,0,0,-1,-1,-1,-1,-1,0,0,5,5,5,5,5,5,5,5]
        board[13] = [6,6,6,6,6,6,0,0,0,-1,-1,-1,-1,-1,0,0,5,5,5,5,5,5,5,5]
        board[14] = [6,6,6,6,6,6,0,0,0,-1,-1,-1,-1,-1,0,0,5,5,5,5,5,5,5,5]
        board[15] = [6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,5,5]
        board[16] = [6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1]
        board[17] = [-1,0,0,0,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0]
        board[18] = [0,0,0,0,0,0,0,0,8,8,8,8,8,8,8,8,0,0,9,9,9,9,9,-1]
        board[19] = [-1,7,7,7,7,0,0,0,8,8,8,8,8,8,8,8,0,0,9,9,9,9,9,9]
        board[20] = [7,7,7,7,7,7,0,0,8,8,8,8,8,8,8,8,0,0,9,9,9,9,9,9]
        board[21] = [7,7,7,7,7,7,0,0,8,8,8,8,8,8,8,8,0,0,9,9,9,9,9,9]
        board[22] = [7,7,7,7,7,7,0,0,8,8,8,8,8,8,8,8,0,0,9,9,9,9,9,9]
        board[23] = [7,7,7,7,7,7,-1,0,0,0,8,8,8,8,0,0,0,-1,9,9,9,9,9,9]
        board[24] = [-1,-1,-1,-1,-1,-1,-1,-1,-1,0,-1,-1,-1,-1,0,-1,-1,-1,-1,-1,-1,-1,-1,-1]
        return board