from game import Game
from qTable import QTable
import time
import matplotlib.pyplot as plt

num_games = 10
save_every = 500

num_players = 6     #between 2 and 6
numQlearnPlayers = 0
results = [None]*num_games

rooms = ["Study", "Hall", "Lounge", "Library", "Dining Room", "Billiard Room", "Conservatory", "Ballroom", "Kitchen"]
weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
characters = ["Mr. Green", "Colonel Mustard", "Mrs. Peacock", "Professor Plum", "Ms. Scarlet", "Mrs. White"]

#qtbl = QTable(rooms, weapons, characters)
qtbl = {}

tic = time.time()

for i in range(num_games):
    print("Playing Game:", i+1)
    game = Game(num_players, qtbl, numQlearn=numQlearnPlayers)
    results[i] = game.run_game()
    print()
    if (i % save_every) == save_every-1:
        print("writing Q-table to file\n")
        qtbl.write_table()

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
rsum = 0
for i in range(numQlearnPlayers):
        qsum += character_wins[characters[i]]

for i in range(numQlearnPlayers, num_players):
        rsum += character_wins[characters[i]]

plt.figure(1)
plt.title("Number of Wins out of %d Games" % num_games)
plt.bar(["Q-learn player","Random player"], [qsum, rsum])
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

plt.show()
