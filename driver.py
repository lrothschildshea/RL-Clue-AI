from game import Game
from qTable import QTable
import time
import matplotlib.pyplot as plt
from QNetwork import QNetwork
from replayMemory import ReplayMemory
import torch
import pickle
from collections import namedtuple
import os

num_games = 1000
save_every = 1000
isTraining = True
#newNetworks = True
newNetworks = False

num_players = 6     #between 2 and 6
numQlearnPlayers = 0
numDeepQLearnPlayers = 1
results = [None]*num_games

rooms = ["Study", "Hall", "Lounge", "Library", "Dining Room", "Billiard Room", "Conservatory", "Ballroom", "Kitchen"]
weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
characters = ["Mr. Green", "Colonel Mustard", "Mrs. Peacock", "Professor Plum", "Ms. Scarlet", "Mrs. White"]

#qtbl = QTable(rooms, weapons, characters)

if not newNetworks:
        nets = pickle.load(open("QNetworks.pickle","rb"))
        rm = ReplayMemory(100000, namedtuple('Transition', ('state', 'action', 'next_state', 'reward')))
        qNetworks = (nets[0], nets[1], rm)
else:
        n1 = QNetwork(6, 6, 67220).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        n2 = QNetwork(6, 6, 67220).to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        rm = ReplayMemory(100000, namedtuple('Transition', ('state', 'action', 'next_state', 'reward')))
        qNetworks = (n1, n2, rm)

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
#i believe there are ~3000 duiplicate actions (some rooms have multiple allowable locations) in self.actions but that is a problem for a different day

#play games
tic = time.time()

for i in range(num_games):
    print("Playing Game:", i+1)
    if numQlearnPlayers > 0:
        game = Game(num_players, isTraining, deepQActionSet, qNetworks, qtbl=qtbl, numQlearn=numQlearnPlayers)
    else:
            game = Game(num_players, isTraining, deepQActionSet, qNetworks, numDeepQ=numDeepQLearnPlayers)
    results[i] = game.run_game()
    print()
    '''
    if (i % save_every) == save_every-1:
        print("writing Q-table to file\n")
        qtbl.write_table()
        '''
    if (i % 10) == 0:
        qNetworks[1].load_state_dict(qNetworks[0].state_dict())

    if (i % save_every) == save_every-1:
        print("writing Networks\n")
        pickle.dump((qNetworks[0], qNetworks[1]), open("QNetworks.pickle","wb"))

toc = time.time()

num_players_left = {}
character_wins = {}
game_length = []

for i in range(1, num_players + 1):
    num_players_left[i] = 0

for i in characters:
    character_wins[i] = 0

for i in results:
    num_players_left[i[0]] += 1
    character_wins[i[1]] += 1
    game_length.append(i[2])

print("\nStats on how the game ended")
for i in num_players_left:
    print(i, num_players_left[i])

print("\nStats on which character won")
for i in character_wins:
    print(i, character_wins[i])

print("\nPlayed", num_games, "games with", num_players, "players in", toc-tic, "seconds.")

qsum = 0
dqsum = 0
rsum = 0
for i in range(numQlearnPlayers):
        qsum += character_wins[characters[i]]

for i in range(numQlearnPlayers, numDeepQLearnPlayers):
        dqsum += character_wins[characters[i]]

for i in range(numQlearnPlayers + numDeepQLearnPlayers, num_players):
        rsum += character_wins[characters[i]]

plt.figure(1)
plt.title("Number of Wins out of %d Games" % num_games)
plt.bar(["Q-learn Player", "Deep Q-learn Player","Random Player"], [qsum, dqsum, rsum])
plt.ylabel("Number of Wins")
plt.xlabel("Player Type")

plt.figure(2)
plt.scatter(range(0, num_games), game_length)
plt.ylabel("Length of Game")
plt.xlabel("Iteration")
plt.title("Length of games during learning")

plt.figure(3)
plt.title("Player's Win Records")
plt.bar(characters, character_wins.values())
plt.ylabel("Number of Wins")
plt.xlabel("Character")

if not os.path.exists("figures"):
        os.mkdir("figures")

plt.figure(1).savefig("figures/gamesWonByPlayerType.png")
plt.figure(2).savefig("figures/gameLength.png")
plt.figure(3).savefig("figures/gamesWonByCharacter.png")
