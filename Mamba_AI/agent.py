#
import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot
import os

# MAX_MEMORY = 100000
# BATCH_SIZE = 1000
# LR = 0.0005


# Augmenter la taille de la mémoire et du batch
MAX_MEMORY = 500000  # 5x plus grand
BATCH_SIZE = 4096    # 4x plus grand pour un meilleur apprentissage

# Ajuster aussi le learning rate pour la stabilité
LR = 0.0001  # Réduire pour éviter les explosions de gradient




class Agent :

    def __init__(self) :
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.95  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        # self.model = Linear_QNet(12, 512, 3)
        self.model = Linear_QNet(
            input_size=12,
            hidden_size1=1024,
            hidden_size2=2048,
            hidden_size3=1024,
            output_size=3
        )
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game) :
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        # Calculer la distance Manhattan à la nourriture
        food_distance = abs(game.food.x - game.head.x) + abs(game.food.y - game.head.y)
        normalized_distance = food_distance / (game.w * 2)  # Normaliser entre 0 et 1


        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Food location
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y, # food down

            # food distance
            normalized_distance

            # normalized_distance

            # food penalty

            # position la queue

            # poisition  global

        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done) :
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self) :
        if len(self.memory) > BATCH_SIZE :
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else :
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done) :
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state) :
        # random moves: tradeoff exploration / exploitation
        # self.epsilon = 80 - self.n_games
        # final_move = [0, 0, 0]
        # if random.randint(0, 200) < self.epsilon :
        #     move = random.randint(0, 2)
        #     final_move[move] = 1
        # else :
        #     state0 = torch.tensor(state, dtype=torch.float)
        #     prediction = self.model(state0)
        #     move = torch.argmax(prediction).item()
        #     final_move[move] = 1
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon :
            move = random.randint(0, 2)
            final_move[move] = 1
        else :
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            # Ajouter du bruit pour l'exploration
            if random.random() < 0.1 :
                prediction += torch.randn_like(prediction) * 0.1
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def count_network_parameters(self) :
        # On utilise self.model au lieu de model
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        return total_params, trainable_params

    def print_model_info(self) :
        # Calculer la taille du réseau
        total_params, trainable_params = self.count_network_parameters()

        # Récupérer la structure du modèle
        input_size = self.model.linear1.in_features
        hidden_size1 = self.model.linear1.out_features
        hidden_size2 = self.model.linear2.out_features
        hidden_size3 = self.model.linear3.out_features
        output_size = self.model.linear4.out_features

        # Calculer le nombre total de neurones
        total_neurons = input_size + hidden_size1 + hidden_size2 + hidden_size3 + output_size

        # Calculer le nombre de connexions
        connections_layer1 = input_size * hidden_size1
        connections_layer2 = hidden_size1 * hidden_size2
        connections_layer3 = hidden_size2 * hidden_size3
        connections_layer4 = hidden_size3 * output_size
        total_connections = connections_layer1 + connections_layer2 + connections_layer3 + connections_layer4

        print("\n=== Architecture du Réseau ===")
        print(f"Couche d'entrée: {input_size:,} neurones")
        print(f"Couche cachée 1: {hidden_size1:,} neurones")
        print(f"Couche cachée 2: {hidden_size2:,} neurones")
        print(f"Couche cachée 3: {hidden_size3:,} neurones")
        print(f"Couche de sortie: {output_size:,} neurones")
        print(f"Nombre total de neurones: {total_neurons:,}")

        print("\n=== Connexions ===")
        print(f"Connexions input->hidden1: {connections_layer1:,}")
        print(f"Connexions hidden1->hidden2: {connections_layer2:,}")
        print(f"Connexions hidden2->hidden3: {connections_layer3:,}")
        print(f"Connexions hidden3->output: {connections_layer4:,}")
        print(f"Total connexions: {total_connections:,}")

        print("\n=== Configuration du Modèle ===")
        print(f"Architecture: {input_size} -> {hidden_size1} -> {hidden_size2} -> {hidden_size3}-> {output_size}")
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


def train(max_games,checkpoint_interval,save_dir) :
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()

    # Afficher les informations du modèle au début de l'entraînement
    agent.print_model_info()

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

        # Sauvegarder la configuration dans un fichier
        config_path = os.path.join(save_dir, 'model_config.txt')
        with open(config_path, 'w') as f :
            f.write("=== Configuration de l'Entraînement ===\n")
            f.write(f"Nombre maximum de parties: {max_games}\n")
            f.write(f"Intervalle de sauvegarde: {checkpoint_interval}\n")

            f.write("\n=== Architecture du Réseau ===\n")
            input_size = agent.model.linear1.in_features
            hidden_size = agent.model.linear1.out_features
            output_size = agent.model.linear2.out_features
            f.write(f"Structure: {input_size} -> {hidden_size} -> {output_size}\n")

            f.write("\n=== Hyperparamètres ===\n")
            f.write(f"Learning Rate: {agent.trainer.lr}\n")
            f.write(f"Gamma: {agent.gamma}\n")
            f.write(f"Batch Size: {BATCH_SIZE}\n")
            f.write(f"Memory Size: {MAX_MEMORY}\n")





    try:
        while True :
            # get old state
            state_old = agent.get_state(game)

            # get move
            final_move = agent.get_action(state_old)

            # perform move and get new state
            reward, done, score = game.play_step(final_move)
            state_new = agent.get_state(game)

            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            agent.remember(state_old, final_move, reward, state_new, done)

            if done :
                # train long memory, plot result
                game.reset()
                agent.n_games += 1
                agent.train_long_memory()

                if score > record :
                    record = score
                    # agent.model.save()
                    agent.trainer.save_model(f'model_best_score_{record}.pth')

                print('Game', agent.n_games, 'Score', score, 'Record:', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)
                print("Score Moyenne:",mean_score)


                # # Sauvegarder les courbes d'apprentissage
                # plot(plot_scores, plot_mean_scores,
                #      os.path.join(save_dir, f'learning_curve_game_{agent.n_games}.png'))
                # print(f"Score Moyen: {mean_score:.2f}")

                # Checkpoint périodique
                if agent.n_games % checkpoint_interval == 0:
                    checkpoint_path = os.path.join(save_dir, f'model_checkpoint_game_{agent.n_games}.pth')
                    agent.trainer.save_model(checkpoint_path)
                    print(f"Checkpoint sauvegardé: {checkpoint_path}")

        # Sauvegarde finale une fois l'entrainement terminé
        final_model_path = os.path.join(save_dir, 'model_final.pth')
        agent.trainer.save_model(final_model_path)
        final_plot_path = os.path.join(save_dir, 'learning_curve_final.png')
        plot(plot_scores, plot_mean_scores, final_plot_path)
        print(f"\nEntrainement terminé. Modèle final sauvegardé: {final_model_path}")

    except KeyboardInterrupt:
        print("\nEntrainement interrompu. Sauvegarde finale...")
        interrupt_model_path = os.path.join(save_dir, 'model_interrupted.pth')
        agent.trainer.save_model(interrupt_model_path)
        interrupt_plot_path = os.path.join(save_dir, 'learning_curve_interrupted.png')
        plot(plot_scores, plot_mean_scores, interrupt_plot_path)
        print(f"Sauvegarde effectuée: {interrupt_model_path}")


if __name__ == '__main__' :
    train(max_games=50,
          checkpoint_interval=20,
          save_dir='checkpoints')