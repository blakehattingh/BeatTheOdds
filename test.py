from itertools import islice
from AdditionalFunctions import TieBreakerProbability
import numpy as np
import matplotlib.pyplot as plt
import csv

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
    Probs = [[0.5313235283602543, 0.46867647163974563], [0.5194087467354603, 0.4805912532645397], 
                [0.531323528360258, 0.4686764716397421], [0.6492655842104569, 0.3507344157895431], 
                [0.5854693402339729, 0.4145306597660272], [0.649265584210461, 0.35073441578953896], 
                [0.7708113978657046, 0.22918860213429537], [0.6440181063601971, 0.35598189363980287], 
                [0.770811397865709, 0.22918860213429107]]
    Scenarios = ['0.01', '0.05', '0.10']

    FS1 = [Probs[0][0], Probs[3][0], Probs[6][0]]
    FSE = [Probs[1][0], Probs[4][0], Probs[7][0]]
    FS2 = [Probs[2][0], Probs[5][0], Probs[8][0]]

    # Label Locations:
    x = np.arange(len(Scenarios))
    width = 0.25

    fig, ax = plt.subplots()
    ax.bar(x-width, FS1, width, label = 'Player 1 Serving First')
    ax.bar(x, FSE, width, label = '50-50 Initial Distribution')
    ax.bar(x+width, FS2, width, label = 'Player 2 Serving First')

    # Add labels:
    ax.set_xlabel('Difference in Serving Abilities')
    ax.set_ylabel('Probability of Player 1 Winning a Set')
    ax.set_title('Probability of Winning a Set dependent on the First Server')
    ax.set_xticks(x)
    ax.set_xticklabels(Scenarios)
    ax.legend()

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
