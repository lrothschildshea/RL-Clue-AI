import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
import numpy as np
import random
import math
from collections import namedtuple

class Player():
    def __init__(self, characterName, hand, board, actionSet, qNetworks):
        self.rooms = {
            "Study": 0,
            "Hall": 0,
            "Lounge": 0,
            "Library": 0,
            "Dining Room": 0,
            "Billiard Room": 0,
            "Conservatory": 0,
            "Ballroom": 0,
            "Kitchen": 0
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
        self.actions = actionSet

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
        
        self.stepsDone = 0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.nActions = 67220
        self.policy_net = qNetworks[0]
        self.Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))
        self.target_net = qNetworks[1]
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()
        self.optimizer = optim.RMSprop(self.policy_net.parameters())
        self.memory = qNetworks[2]


    def record_cards(self, hand):
        for i in hand:
            if i in self.rooms:
                self.rooms[i] = 1
            elif i in self.weapons:
                self.weapons[i] = 1
            else:
                self.people[i] = 1

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

    def get_state(self, other_players, board):
        m = np.zeros((6,6))
        #encode player locations
        for i in range(len(other_players)):
            m[i][0] = other_players[i].location[0]
            m[i][1] = other_players[i].location[1]

        #encode self location
        m[5][0] = self.location[0]
        m[5][1] = self.location[1]
        
        #encode known characters
        idx = 0
        for i in self.people:
            m[idx][2] = self.people[i]
            idx += 1
        
        #encode known weapons
        idx = 0
        for i in self.weapons:
            m[idx][3] = self.weapons[i]
            idx += 1
        
        idx = 0
        for i in self.rooms:
            if idx < 6:
                m[idx][4] = self.rooms[i]
            else:
                m[idx - 6][5] = self.rooms[i]
            idx += 1
        
        m[3][5] = self.stepsDone
        m[4][5] = board[self.location[0]][self.location[1]]
        return torch.from_numpy(np.asarray([np.asarray([m])])).float().to(self.device)

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
            if (board[i.location[0]][i.location[1]] == 0) and (i.location in moves):
                moves.remove(i.location)

        return moves

    def get_action(self, board, doors, roll, loc, other_players, state):
        threshold = .05 + .9/(math.exp(-1*self.stepsDone/10))
        moves = self.get_valid_moves(board, doors, roll, loc, other_players)
        
        best_mv = None
        best_mv_val = -1000000

        if random.random() > threshold:
            out = self.policy_net(state)

            if self.stepsDone == 0 and len(self.memory) == 0:   #guarantee first move into memory isn't a solution guess
                for i in range(self.nActions):
                    if self.actions[i][0] in moves and self.actions[i][1] != 's' and out[0][i].item() > best_mv_val:
                        best_mv_val = out[0][i].item()
                        best_mv = torch.tensor([[i]], device=self.device, dtype=torch.long)

            else:
                for i in range(self.nActions):
                    if self.actions[i][0] in moves and out[0][i].item() > best_mv_val:
                        best_mv_val = out[0][i].item()
                        best_mv = torch.tensor([[i]], device=self.device, dtype=torch.long)
        else:

            if self.stepsDone == 0 and len(self.memory) == 0:
                a = list(range(self.nActions))
                while len(a) > 0:
                    choice = random.choice(a)
                    best_mv = torch.tensor([[choice]], device=self.device, dtype=torch.long)
                    
                    if self.actions[best_mv[0][0].item()][0] not in moves or self.actions[best_mv[0][0].item()][1] == 's':
                        a.remove(choice)
                    else:
                        break

            else:
                a = list(range(self.nActions))
                while len(a) > 0:
                    choice = random.choice(a)
                    best_mv = torch.tensor([[choice]], device=self.device, dtype=torch.long)
                    
                    if self.actions[best_mv[0][0].item()][0] not in moves:
                        a.remove(choice)
                    else:
                        break

        return self.actions[best_mv[0][0].item()], best_mv
        

    def optimize(self):
        batch_sz = 32
        if len(self.memory) < batch_sz:
            return
        
        transitions = self.memory.sample(batch_sz)
        batch = self.Transition(*zip(*transitions))
        while(len([s for s in batch.next_state if s is not None]) < 1):
            transitions = self.memory.sample(batch_sz)
            batch = self.Transition(*zip(*transitions))
        
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), device=self.device, dtype=torch.uint8)
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        next_state_values = torch.zeros(batch_sz, device=self.device)
        next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0].detach()
        expected_state_action_values = (next_state_values * .999) + reward_batch.float().to(self.device)

        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))
        self.optimizer.zero_grad()
        loss.backward()
        print(loss)
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()


    def make_move(self, board, doors, roll, loc, other_players, sol):
        # i think this will call optimize and whatnot
        currState = self.get_state(other_players, board)
        action, action_tensor = self.get_action(board, doors, roll, loc, other_players, currState)
        self.stepsDone += 1

        reward = 0
        ret_val = None
        gameOver = False

        if action[1] == 'n':
            #in hall
            self.location = action[0]
            reward = -5
        elif action[1] == 's':
            #guess solution
            self.location = action[0]
            if sol == action[2]:
                reward = 1000
            else:
                reward = -1000
            ret_val = action[2]
            gameOver = True
        else:
            #accusation
            self.location = action[0]
            acc = action[2]

            #move accused player to room
            for i in other_players:
                if i.character == acc[2]:
                    i.location = self.location
                    break
            
            learn = False
            #ask other players for a card
            for i in other_players:
                response = i.acc_respond(acc)
                if response != None and ((response in self.rooms and self.rooms[response] == 0) or (response in self.weapons and self.weapons[response] == 0) or (response in self.people and self.people[response] == 0)):
                    learn = True
                    self.record_cards([response])
                    reward = 20
                    break
            if not learn:
                reward = -20

        reward = torch.tensor([reward], device=self.device)
        newState = self.get_state(other_players, board)
        if gameOver:
            newState = None

        self.memory.add(currState, action_tensor, newState, reward)
        self.optimize()

        return ret_val
