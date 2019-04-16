import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T

class QNetwork(nn.Module):
    def __init__(self, h, w, outputs):
        super(QNetwork, self).__init__()
        self.head = nn.Linear(h*w, 1000)
        self.h = nn.Linear(1000, outputs)

    def forward(self, x):
        return self.h(F.relu(self.head(x.view(x.size(0), -1))))
