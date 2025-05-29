import torch
import numpy as np
import random
from collections import deque
from game import SnakeGame, Direction, Point
from model import QNET_Neuronal, Qtrainer
from helper import plot

MAX_MEMORY = 1_000_000  # default : 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = QNET_Neuronal(11, 1024, 3)
        self.trainer = Qtrainer(self.model, lr=LR, gamma=self.gamma)

        self.model = self.model.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))


    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x - 20, head.y)
        point_u = Point(head.x - 20, head.y -20)
        point_d = Point(head.x - 20, head.y +20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        snake_length = len(game.snake)

        state = [
            # danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # food location
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y,  # food down

            # snake_length


            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: exploration/exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            if torch.cuda.is_available():
                state0 = state0.cuda()

            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def train(self):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        agent = Agent()
        game = SnakeGame()
        agent.print_model_info()
        while True:
            # get old state
            old_state = agent.get_state(game)

            # get move
            final_move = agent.get_action(old_state)

            # perform move and get new state
            reward, done, score = game.play_step(final_move)
            new_state = agent.get_state(game)

            # train short memory
            # self.train_short_memory(old_state, final_move, reward, new_state, done)
            agent.train_short_memory(old_state, final_move, reward, new_state, done)

            # remember
            # self.remember(old_state, final_move, reward, new_state, done)
            agent.remember(old_state, final_move, reward, new_state, done)

            if done:
                # train long memory, plot result
                game.reset()
                agent.n_games += 1
                agent.train_long_memory()

                if score > record:
                    record = score
                    agent.model.save()

                print('Game', agent.n_games, 'Score', score, 'Record', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)


    def count_network_parameters(self) :
        # On utilise self.model au lieu de model
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        return total_params, trainable_params

    def print_model_info(self):
        total_params, trainable_params = self.count_network_parameters()
        print(f"Total parameters: {total_params}, Trainable parameters: {trainable_params}")
        print(self.model)

        # Récupérer la structure du modèle
        input_size = self.model.qnet1.in_features
        hidden_size = self.model.qnet1.out_features
        output_size = self.model.qnet2.out_features

        # Total le nombre de Neurones
        total_neurons = input_size + hidden_size + output_size

        # Calculer les combre de connexion
        connections_layer1 = input_size * hidden_size
        connections_layer2 = hidden_size * output_size
        total_connections = connections_layer1 + connections_layer2

        print("\n=== Architecture du Réseau ===")
        print(f"Input Layer: {input_size} Neurons")
        print(f"Hidden Layer: {hidden_size} Neurons")
        print(f"Output Layer: {output_size} Neurons")
        print(f"Total Neurons: {total_neurons}")

        print("\n=== Connexions ===")
        print(f"Connexions input->hidden1: {connections_layer1:,}")
        print(f"Connexions hidden1->output: {connections_layer2:,}")
        print(f"Total Connections: {total_connections:,}")

        print("\n=== Configuration du Modèle ===")
        print(f'Architecture: {input_size} -> {hidden_size} -> {output_size}')
        print(f"Paramètres totaux: {total_params:,}")
        print(f"Paramètres entrainables: {trainable_params:,}")

        print("\n=== Hyperparamètres ===")
        print(f"Learning Rate: {self.trainer.lr}")
        print(f"Gamma (discount): {self.gamma}")
        print(f"Batch Size: {BATCH_SIZE}")
        print(f"Memory Size: {MAX_MEMORY}")
        print(f"Epsilon initial: {self.epsilon}")

        print("\n=== Détails de la Mémoire ===")
        print(f"Taille actuelle de la mémoire: {len(self.memory)}")
        print(f"Taille maximale de la mémoire: {self.memory.maxlen}")
        if torch.cuda.is_available():
            print("Le modèle est exécuté sur GPU.")
        else:
            print("Le modèle est exécuté sur CPU.")
















if __name__ == '__main__':
    if torch.cuda.is_available():
        print("CUDA is available. Training on GPU.")
    else:
        print("CUDA is not available. Training on CPU.")


    agent = Agent()
    agent.train()

