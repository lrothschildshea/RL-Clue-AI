import random

class ReplayMemory(object):
    def __init__(self, capacity, transition):
        self.capacity = capacity
        self.pos = 0
        self.mem = []
        self.Transition = transition

    def sample(self, num):
        return random.sample(self.mem, num)
    

    def add(self, *args):
        if len(self.mem) < self.capacity:
            self.mem.append(None)
        
        self.mem[self.pos] = self.Transition(*args)
        self.pos = (self.pos + 1) % self.capacity


    def __len__(self):
        return len(self.mem)
