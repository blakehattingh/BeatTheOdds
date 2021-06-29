from itertools import islice
from MarkovSimulations import MarkovChainTieBreaker
import csv
import os

# Find the nth position of a value in an array:
def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)

# Combinatoric Generator:
def combine_recursion(n, k):
    result = []
    combine_dfs(n, k, 1, [], result)
    return result

def combine_dfs(n, k, start, path, result):
    if k == len(path):
        result.append(path)
        return
    for i in range(start, n + 1):
        combine_dfs(n, k, i + 1, path + [i], result)

def TieBreakerProbability(P1S, P2S, Iter, FirstTo):
    # Compute the probability of winning a TB using the MarkovTB Simulation:

    Count1 = 0
    Count2 = 0
    for i in range(Iter):
        # Player 1 Serving first:
        Winner1 = MarkovChainTieBreaker(P1S, P2S, 'i', FirstTo)
        # Player 2 Serving first:
        Winner2 = MarkovChainTieBreaker(P1S, P2S, 'j', FirstTo)
        if (Winner1 == 'i'):
            Count1 = Count1 + 1
        if (Winner2 == 'j'):
            Count2 = Count2 + 1
    
    # Compute their probability of winning when they start the TB serving:
    return [Count1/Iter, Count2/Iter] # Prob Player 1 winning if he serves first, Prob Player 2 winning if he serves first

def ComputeTBProbabilities(P1S, P2S):
    # Find which row and column these Pserve probabilities correspond to in the TBProbs matrix:
    Row = round((P1S - 0.50) / 0.01)
    Col = round((P2S - 0.50) / 0.01)

    # Compute the tie-breaker probabilities using pre-calculated values from a simulation:
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(THIS_FOLDER,'TBProbabilities.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == Row:
                P1TB = float(row[Col])
                # Compute P2TB:
                P2TB = 1. - P1TB
                return P1TB, P2TB
            else:
                line_count += 1