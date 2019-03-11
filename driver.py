from game import Game

num_games = 100
num_players = 6     #between 2 and 6
results = [None]*num_games
characters = ["Mr. Green", "Colonel Mustard", "Mrs. Peacock", "Professor Plum", "Ms. Scarlet", "Mrs. White"]


for i in range(num_games):
    print("Playing Game:", i+1)
    game = Game(num_players)
    results[i] = game.run_game()
    print()

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
