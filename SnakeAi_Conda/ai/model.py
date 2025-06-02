import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
# from game.constants import *
from SnakeAi_Conda.game import constants

class SnakeBrain(nn.Module):
    def __init__(self):
        super(SnakeBrain, self).__init__()
        # Architecture du réseau
        self.fc1 = nn.Linear(INPUT_SIZE, HIDDEN_SIZE)
        self.fc2 = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)
        self.fc3 = nn.Linear(HIDDEN_SIZE, OUTPUT_SIZE)

        # Initialisation des poids
        self._init_weights()

    def _init_weights(self):
        """Initialise les poids avec la méthode de He pour de meilleures performances"""
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
                nn.init.zeros_(m.bias)

    def forward(self, x):
        """Propagation avant du réseau"""
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return F.softmax(self.fc3(x), dim=-1)  # Utiliser softmax pour obtenir des probabilités

    def get_action(self, state):
        """Obtient l'action à partir de l'état du jeu"""
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            action_probs = self.forward(state_tensor)
            return torch.argmax(action_probs).item()

    def mutate(self, mutation_rate=MUTATION_RATE):
        """Applique une mutation aux poids du réseau"""
        with torch.no_grad():
            for param in self.parameters():
                mutation_mask = torch.rand_like(param) < mutation_rate
                mutation = torch.randn_like(param) * 0.1
                param.data += mutation * mutation_mask

    def crossover(self, other_brain):
        """Effectue un croisement avec un autre cerveau"""
        child = SnakeBrain()

        # Copier les paramètres du parent avec une probabilité de 50/50
        with torch.no_grad():
            for child_param, self_param, other_param in zip(
                    child.parameters(), self.parameters(), other_brain.parameters()
            ):
                mask = torch.rand_like(child_param) < 0.5
                child_param.data = (
                        mask * self_param.data +
                        ~mask * other_param.data
                )

        return child

    def save(self, file_path):
        """Sauvegarde le modèle"""
        torch.save(self.state_dict(), file_path)

    def load(self, file_path):
        """Charge le modèle"""
        self.load_state_dict(torch.load(file_path))
        self.eval()

    def clone(self):
        """Crée une copie exacte du cerveau"""
        clone = SnakeBrain()
        clone.load_state_dict(self.state_dict())
        return clone

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# from game.constants import INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE
#
#
# class DQN(nn.Module):
#     def __init__(self):
#         super(DQN, self).__init__()
#         # Couches du réseau neuronal
#         self.fc1 = nn.Linear(INPUT_SIZE, HIDDEN_SIZE)
#         self.fc2 = nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)
#         self.fc3 = nn.Linear(HIDDEN_SIZE, OUTPUT_SIZE)
#
#         # Initialisation des poids
#         self._init_weights()
#
#     def _init_weights(self):
#         """Initialise les poids du réseau avec la méthode de He"""
#         for m in self.modules():
#             if isinstance(m, nn.Linear):
#                 nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
#                 nn.init.constant_(m.bias, 0)
#
#     def forward(self, x):
#         """Propagation avant du réseau"""
#         x = F.relu(self.fc1(x))
#         x = F.relu(self.fc2(x))
#         return self.fc3(x)
#
#     def save(self, file_path):
#         """Sauvegarde le modèle"""
#         torch.save(self.state_dict(), file_path)
#
#     def load(self, file_path):
#         """Charge le modèle"""
#         self.load_state_dict(torch.load(file_path))
#         self.eval()
