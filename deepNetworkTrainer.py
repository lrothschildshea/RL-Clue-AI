import pickle
from QNetwork import QNetwork
import torch
from replayMemory import ReplayMemory
from collections import namedtuple
from cards import Cards
from deepQPlayer import Player as DeepQPlayer
from player import Player
import random
import time

def get_random_loc():
    room = random.randint(0, 9)
    if room == 0:
        l1 = random.randint(0,24)
        l2 = random.randint(0,23)
        while board[l1][l2] != 0:
            l1 = random.randint(0,24)
            l2 = random.randint(0,23)
        loc = (l1, l2)

    elif room == 1:
        loc = (3, 6)

    elif room == 2:
        rand = random.random()
        if rand < .34:
            loc = (4, 9)
        elif rand < .67:
            loc = (6, 11)
        else:
            loc = (6, 12)

    elif room == 3:
        loc = (5,17)

    elif room == 4:
        if random.random() > .5:
            loc = (8, 6)
        else:
            loc = (10, 3)

    elif room == 5:
        if random.random() > .5:
            loc = (9, 17)
        else:
            loc = (12, 16)

    elif room == 6:
        if random.random() > .5:
            loc = (12, 1)
        else:
            loc = (15, 5)

    elif room == 7:
        loc = (19, 4)

    elif room == 8:
        rand = random.random()
        if rand < .25:
            loc = (19, 8)
        elif rand < .5:
            loc = (17, 9)
        elif rand < .75:
            loc = (17,14)
        else:
            loc = (19,15)

    elif room == 9:
        loc = (18,19)

    return loc

num_games = 100
save_every = 100

newNetworks = True
#newNetworks = False

rooms = ["Ballroom", "Billiard Room", "Conservatory", "Dining Room", "Hall", "Kitchen", "Library", "Lounge", "Study"]
weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
characters = ["Mr. Green", "Colonel Mustard", "Mrs. Peacock", "Professor Plum", "Ms. Scarlet", "Mrs. White"]

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

doors = [((4, 6), 1, (3, 6)), ((4, 8), 2, (4, 9)), ((7, 11), 2, (6, 11)), ((7, 12), 2, (6, 12)), ((6, 17), 3, (5, 17)), ((8, 7), 4, (8, 6)), ((11, 3), 4, (10, 3)), ((8, 17), 5, (9, 17)), ((12, 15), 5, (12, 16)), ((11, 1), 6, (12, 1)), ((15, 6), 6, (15, 5)), ((19, 5), 7, (19, 4)), ((19, 7), 8, (19, 8)), ((16, 9), 8, (17, 9)), ((16, 14), 8, (17, 14)), ((19, 16), 8, (19, 15)), ((17, 19), 9, (18, 19))]

room_map = {
        1: "Study",
        2: "Hall",
        3: "Lounge",
        4: "Library",
        5: "Dining Room",
        6: "Billiard Room",
        7: "Conservatory",
        8: "Ballroom",
        9: "Kitchen"
}

deepQActionSet = {}
room_squares = [(3, 6), (4, 9), (6, 11), (6, 12), (5, 17), (8, 6), (10, 3), (9, 17), (12, 16), (12, 1), (15, 5), (19, 4), (19, 8), (17, 9), (17, 14), (19, 15), (18, 19)]
count = 0
#make set of actions for deepQNetwork
#for every board space
for i in range(len(board)):
        for j in range(len(board[i])):
                #for every combo of card guesses
                add_nothing = True
                for k in rooms:
                        for l in weapons:
                                for m in characters:
                                        #solution guesses in every square
                                        if board[i][j] != -1:
                                                if board[i][j] > 0 and (i, j) in room_squares:
                                                        deepQActionSet[count] = ((i,j), 's', (k, l, m))
                                                        count += 1
                                                elif board[i][j] == 0:
                                                        deepQActionSet[count] = ((i,j), 's', (k, l, m))
                                                        count += 1
                                                
                                        #accusations in every room
                                        if board[i][j] > 0 and (i,j) in room_squares and room_map[board[i][j]] == k:
                                                deepQActionSet[count] = ((i,j), 'a', (k, l, m))
                                                count += 1
                                        
                                        #do nothing if in hallway
                                        if board[i][j] == 0 and add_nothing:
                                                deepQActionSet[count] = ((i,j), 'n', ('0', '0', '0'))
                                                count += 1
                                                add_nothing = False


if not newNetworks:
        nets = pickle.load(open("QNetworks.pickle","rb"))
        rm = ReplayMemory(100000, namedtuple('Transition', ('state', 'action', 'next_state', 'reward')))
        qNetworks = (nets[0], nets[1], rm)
else:
        n1 = QNetwork(6, 6, 67220).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        n2 = QNetwork(6, 6, 67220).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        rm = ReplayMemory(100000, namedtuple('Transition', ('state', 'action', 'next_state', 'reward')))
        qNetworks = (n1, n2, rm)

tic = time.time()
#training loop
for i in range(num_games):

    cards, solution = Cards(6).deal_cards()
    players = []
    players.append(DeepQPlayer(characters[0], cards[0], board, deepQActionSet, qNetworks))
    players[0].location = get_random_loc()

    other_cards = []
    for j in range(1,6):
        players.append(Player(characters[j], cards[j]))
        other_cards += cards[j]
        #move to random spot on board
        players[j].location = get_random_loc()
    
    learned_cards = []
    #give random cards
    for j in other_cards:
        if random.random() > .5:
            learned_cards.append(j)
    
    players[0].record_cards(learned_cards)

    players[0].make_move(board, doors, random.randint(1, 6), players[0].location, players[1:], solution)

    if (i % 32) == 0:
        qNetworks[1].load_state_dict(qNetworks[0].state_dict())

    if (i % save_every) == (save_every - 1):
        toc = time.time()
        print("Writing Networks    Iteration:", i+1, "    Time:", toc - tic, "Seconds")
        pickle.dump((qNetworks[0], qNetworks[1]), open("QNetworks.pickle","wb"))
        tic = time.time()
