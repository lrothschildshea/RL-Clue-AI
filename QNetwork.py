import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

class QNetwork(nn.Module):
    def __init__(self, h, w, outputs):
        super(QNetwork, self).__init__()
        self.l1 = nn.Linear(h*w, 750)
        self.l2 = nn.Linear(750, 1000)
        self.l3 = nn.Linear(1000, 1500)
        self.l4 = nn.Linear(1500, outputs)

    def forward(self, x):
        return self.l4(F.relu(self.l3(torch.tanh(self.l2(F.relu(self.l1(x.view(x.size(0), -1))))))))
