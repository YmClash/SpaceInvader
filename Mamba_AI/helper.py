import matplotlib.pyplot as plt
from IPython import display
import numpy as np

plt.ion()

# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

def plot(scores, mean_scores,save_path='learning_curve.png') :
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))

    plt.show(block=False)
    plt.pause(.1)

    # Sauvegarder la courbe
    plt.savefig(save_path)

    # Sauvegarder les données brutes
    np.save('scores.npy', np.array(scores))
    np.save('mean_scores.npy', np.array(mean_scores))

    #
    # display.clear_output(wait=True)
    # display.display(plt.gcf())
    # plt.clf()
    #
    # # Create figure with two subplots
    # fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
    # ax1.clear()
    # ax2.clear()
    # fig.suptitle('Training...')
    #
    # # First subplot for scores
    # ax1.set_xlabel('Number of Games')
    # ax1.set_ylabel('Score')
    # ax1.plot(scores, 'b-', label='Score')
    # ax1.plot(mean_scores, 'r-', label='Mean Score')
    # ax1.text(len(scores) - 1, scores[-1], str(scores[-1]))
    # ax1.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    # ax1.legend()
    # ax1.set_ylim(ymin=0)
    #
    # # Second subplot for epsilon (exploration rate)
    # ax2.set_xlabel('Number of Games')
    # ax2.set_ylabel('Epsilon (Exploration Rate)')
    # epsilon_values = [max(0, 80 - i) for i in range(len(scores))]  # Calculate epsilon values
    # ax2.plot(epsilon_values, 'g-', label='Epsilon')
    # ax2.legend()
    # ax2.set_ylim(ymin=0, ymax=80)
    #
    # # plt.tight_layout()
    # plt.show(block=False)
    # plt.pause(.1)
    # if len(scores) % 100 == 0 :  # Save plot every 100 games
    #     plt.savefig('training_progress.png')

