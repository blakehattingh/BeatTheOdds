from itertools import islice
from AdditionalFunctions import TieBreakerProbability
import numpy as np
import csv

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
    # Calculating the TB values for each possible combination of P1S and P2S values:
    # Store each probability for player 1 winning for each combination of P1S and P2S values:
    # Each row corresponds to a new P1S value:
    # e.g. Row 1 = P1S = 0.5, Row 2 = 0.55, Row = 0.6
    x = list(range(18,66))
    print(x)
    # Generate all possible P1S and P2S values:
    P1S = np.arange(0.5, 0.9, 0.1).tolist()
    P2S = np.arange(0.5, 0.9, 0.1).tolist()

    # Set up Tie-breaker:
    FirstToTBPoints = 7
    Iterations = 1000
    TBProbabilities = []
    P1WinProbs = []

    # Run simulation for all possible P1S and P2S values:
    for P1 in P1S:
        for P2 in P2S:
            [P1Winning, P2Winning] = TieBreakerProbability(P1, P2, Iterations, FirstToTBPoints)
            P1WinProbs.append(P1Winning)
        # Store the probabilities for that P1S value:
        TBProbabilities.append(P1WinProbs)
        P1WinProbs = []
        print(P1)
    

    with open('TBProbabilities.csv', mode = 'w', newline = "") as TB_file:
        TB_writer = csv.writer(TB_file)
        TB_writer.writerows(TBProbabilities)    

if __name__ == "__main__":
    main()
