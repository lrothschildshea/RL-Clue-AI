
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
        self.location = (0,0)       #this will need to change based off of which character they are
        self.cards = hand

        for i in self.cards:
            if i in self.rooms:
                self.rooms[i] = 1
            elif i in self.weapons:
                self.weapons[i] = 1
            else:
                self.people[i] = 1


    #todo
    def get_valid_moves(self):
        return

    #todo
    def make_move(self):
        return
    
    #todo
    def guess_solution(self):
        return