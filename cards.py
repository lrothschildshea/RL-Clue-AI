import random

class Cards:

    numPlayers = 2
    rooms = ["Ballroom", "Billiard Room", "Conservatory", "Dining Room", "Hall", "Kitchen", "Library", "Lounge", "Study"]
    weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
    people = ["Mr. Green", "Colonel Mustard", "Mrs. Peacock", "Professor Plum", "Ms. Scarlet", "Mrs. White"]

    def __init__(self, numberOfPlayers):
        self.numPlayers = numberOfPlayers

    def deal_cards(self):
        room = self.rooms[random.randint(0, len(self.rooms) - 1)]
        rooms_cp = self.rooms[:]
        rooms_cp.remove(room)

        weapon = self.weapons[random.randint(0, len(self.weapons) - 1)]
        weapons_cp = self.weapons[:]
        weapons_cp.remove(weapon)

        person = self.people[random.randint(0, len(self.people) - 1)]
        people_cp = self.people[:]
        people_cp.remove(person)

        deck = rooms_cp + weapons_cp + people_cp

        random.shuffle(deck)

        hands = []
        for i in range(self.numPlayers):
            hands.append([])
        
        idx = 0
        while len(deck) > 0:
            hands[idx].append(deck[0])
            deck.remove(deck[0])
            idx = (idx + 1) % self.numPlayers
        
        return hands, (room, weapon, person)