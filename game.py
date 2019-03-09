from cards import Cards
from player import Player

class Game:

    board = []
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

        # need to design board
        self.board = []

    
    def is_game_over(self):
        return self.solution_guessed

    #todo
    def run_game(self):
        return