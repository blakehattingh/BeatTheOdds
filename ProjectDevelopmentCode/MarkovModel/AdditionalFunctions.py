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
    #Find which row and column these Pserve probabilities correspond to in the TBProbs matrix:
    Row = round((P1S - 0.50) / 0.01)
    Col = round((P2S - 0.50) / 0.01)

    # Compute the tie-breaker probabilities using pre-calculated values from a simulation:
    THIS_FOLDER = os.path.abspath(os.getcwd())
    with open(os.path.join(THIS_FOLDER, 'CSVFiles\\TBProbabilities.csv')) as csv_file:
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

def OddsComputer(FirstOdds, Margin = 0.08):
    SecondOdds = FirstOdds / (FirstOdds * (1. + 0.5 * Margin) - 1)
    return SecondOdds

def RemainingOdds(Odds, Margin = 0.08):
    Probs = 0.
    for i in Odds:
        Probs += (1. / i)
    
    # Check if odds are too low:
    if (1. + Margin <= Probs):
        print("Increase Odds, current implied probability is {}".format(100*Probs))
    else:
        RemainP = (1. + Margin - Probs)
        return (1. / RemainP)
        
def BuildingTheTBDataBase():
    # Calculating the TB values for each possible combination of P1S and P2S values:
    # Store each probability for player 1 winning for each combination of P1S and P2S values:
    # Each row corresponds to a new P1S value:
    # e.g. Row 1 = P1S = 0.5, Row 2 = 0.55, Row = 0.6

    # Generate all possible P1S and P2S values:
    P1S = np.arange(0.5, 0.95, 0.01).tolist()
    P2S = np.arange(0.5, 0.95, 0.01).tolist()

    # Set up Tie-breaker:
    FirstToTBPoints = 7
    Iterations = 100000
    TBProbabilities = []
    P1WinProbs = []

    # Run simulation for all possible P1S and P2S values:
    for P1 in P1S:
        for P2 in P2S:
            [P1Winning, P2Winning] = TieBreakerProbability(P1, P2, Iterations, FirstToTBPoints)
            P1WinProbs.append(P1Winning)
            print(P2)
        # Store the probabilities for that P1S value:
        TBProbabilities.append(P1WinProbs)
        P1WinProbs = []
        print(P1)

    with open('TBProbabilities.csv', mode = 'w', newline = "") as TB_file:
        TB_writer = csv.writer(TB_file)
        TB_writer.writerows(TBProbabilities)    