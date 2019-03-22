from game import Game
from qTable import QTable
import time

num_games = 30
save_every = 5000

num_players = 6     #between 2 and 6
results = [None]*num_games

rooms = ["Study", "Hall", "Lounge", "Library", "Dining Room", "Billiard Room", "Conservatory", "Ballroom", "Kitchen"]
weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
characters = ["Mr. Green", "Colonel Mustard", "Mrs. Peacock", "Professor Plum", "Ms. Scarlet", "Mrs. White"]

qtbl = QTable(rooms, weapons, characters)

tic = time.time()

for i in range(num_games):
    print("Playing Game:", i+1)
    game = Game(num_players, qtbl, numQlearn=6)
    results[i] = game.run_game()
    print()
    if (i % save_every) == save_every-1:
        print("writing Q-table to file\n")
        qtbl.write_table()

toc = time.time()

num_players_left = {}
character_wins = {}

for i in range(1, num_players + 1):
    num_players_left[i] = 0

for i in characters:
    character_wins[i] = 0

for i in results:
    num_players_left[i[0]] += 1
    character_wins[i[1]] += 1

print("\nStats on how the game ended")
for i in num_players_left:
    print(i, num_players_left[i])

print("\nStats on which character won")
for i in character_wins:
    print(i, character_wins[i])

print("\nPlayed", num_games, "games with", num_players, "players in", toc-tic, "seconds.")
