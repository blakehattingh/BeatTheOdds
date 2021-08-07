from FirstImplementation import MarkovModelFirstImplementation
import numpy as np
import csv

def BuildingDB(PStart, PEnd, Increment):
    # This function runs our Markov Model for ALL possible P1 and P2 combinations
    # Inputs:
    # - PStart: The lowest P values we want to consider
    # - PEnd: The highest P values we want to consider
    # - Increment: The increase in P values
    #   e.g. P1 = [0.6, 0.61, 0.62....0.90] has PStart = 0.6, PEnd = 0.9 and Increment = 0.01

    # Compute the number of p values to consider:
    N = int(((PEnd - PStart) / Increment) + 1)

    # Create a dictionary to store all distributions from each run of the model:
    # Dictionary Format:
    # - Key = (P1, P2)
    # - Values = Another Dictionary
    #   - Key = Distribution Name e.g. "Match Score"
    #   - Values = Distribution as an array
    DataBase = {}

    # Create an array of P values:
    PValues = np.linspace(PStart/100., PEnd/100., N)

    for P1 in PValues:
        for P2 in PValues:
            print('P-values: ', [P1],[P2])
            # Run the model:
            [MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = MarkovModelFirstImplementation(P1, P2, 3, 7)

            # Create the dictionary of distributions for this run:
            Distributions = {'Match Outcome': MatchDist, 'Match Score': MatchScoreDist, 'Number of Games': TotalNumGamesDist, 
            'Set Score': AllSetScoresDist}

            # Store the distributions:
            DataBase[(P1, P2)] = Distributions

    # Export the dictionary of distributions to a csv file:
    with open('ModelDistributions.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in DataBase.items():
            writer.writerow([key, value])

def main():
    # Run function:
    BuildingDB(50, 60, 5)

if __name__ == "__main__":
    main()