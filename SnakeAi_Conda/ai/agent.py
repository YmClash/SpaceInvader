import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
from .model import DQN
from .memory import ReplayMemory
from game.constants import *


class Agent:
    def __init__(self, device):
        self.device = device
        self.policy_net = DQN().to(device)
        self.target_net = DQN().to(device)
        self.target_net.load_state_dict(self.policy_net.state_dict())

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=LEARNING_RATE)
        self.memory = ReplayMemory(MEMORY_SIZE)

        self.epsilon = EPSILON_START
        self.steps_done = 0

    def select_action(self, state):
        """Sélectionne une action selon la politique epsilon-greedy"""
        if random.random() > self.epsilon:
            with torch.no_grad():
                state = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                q_values = self.policy_net(state)
                return q_values.max(1)[1].item()
        else:
            return random.randrange(OUTPUT_SIZE)

    def optimize(self):
        """Optimise le réseau de neurones"""
        if len(self.memory) < BATCH_SIZE:
            return

        # Échantillonner un batch de transitions
        states, actions, next_states, rewards, dones = self.memory.sample(BATCH_SIZE)

        # Convertir en tenseurs PyTorch
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.LongTensor(actions).to(self.device)
        next_states = torch.FloatTensor(next_states).to(self.device)
        rewards = torch.FloatTensor(rewards).to(self.device)
        dones = torch.FloatTensor(dones).to(self.device)

        # Calculer les Q-values courantes
        current_q_values = self.policy_net(states).gather(1, actions.unsqueeze(1))

        # Calculer les Q-values cibles
        with torch.no_grad():
            next_q_values = self.target_net(next_states).max(1)[0]
            target_q_values = rewards + (1 - dones) * GAMMA * next_q_values

        # Calculer la perte
        loss = nn.MSELoss()(current_q_values, target_q_values.unsqueeze(1))

        # Optimiser le modèle
        self.optimizer.zero_grad()
        loss.backward()
        # Gradient clipping pour éviter l'explosion des gradients
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

        # Mettre à jour epsilon pour l'exploration
        self.epsilon = max(EPSILON_END, EPSILON_DECAY * self.epsilon)

        return loss.item()

    def update_target_network(self):
        """Met à jour le réseau cible"""
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def save(self, file_path):
        """Sauvegarde le modèle"""
        self.policy_net.save(file_path)

    def load(self, file_path):
        """Charge le modèle"""
        self.policy_net.load(file_path)
        self.target_net.load_state_dict(self.policy_net.state_dict())
