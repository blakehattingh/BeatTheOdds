from RunMarkovModel import RunMarkovModel
from TennisSetNetwork import TennisSetNetwork
import numpy as np

def main():
    # This file runs each implementation, for each of the 3 scenarios and outputs each distribution as a plot.

    # Scenarios:
    P2S = 0.7
    P1S = [0.71, 0.75, 0.8]
    FirstToTBPoints = 7
    Viscosity = 0.5

    # Distributions:
    MatchDistributions3A1 = []
    NumberOfSetsDistributions3A1 = []
    TotalNumberOfGamesDistributions3A1 = []
    AllSetScoresDistributions3A1 = []
    MatchDistributions5A1 = []
    NumberOfSetsDistributions5A1 = []
    TotalNumberOfGamesDistributions5A1 = []
    AllSetScoresDistributions5A1 = []

    MatchDistributions3A2 = []
    NumberOfSetsDistributions3A2 = []
    TotalNumberOfGamesDistributions3A2 = []
    AllSetScoresDistributions3A2 = []
    MatchDistributions5A2 = []
    NumberOfSetsDistributions5A2 = []
    TotalNumberOfGamesDistributions5A2 = []
    AllSetScoresDistributions5A2 = []

    # Possible Outcomes:
    MatchOutcomes = ['Player 1 Wins', 'Player 2 Wins']
    NumberOfSetsOutcomes = [2,3,4,5]
    TotalNumberOfGamesOutcomes = list(range(18,66))
    AllSetScoreOutcomes = ["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]

    # First Implementation:
    Approach = 1
    for P1 in P1S:
        [MatchDist3, NumSetsDist3, TotalNumGamesDist3, AllSetScoresDist3] = RunMarkovModel(P1,P2S,3,FirstToTBPoints,Approach,Viscosity)
        [MatchDist5, NumSetsDist5, TotalNumGamesDist5, AllSetScoresDist5] = RunMarkovModel(P1,P2S,5,FirstToTBPoints,Approach,Viscosity)

        [MatchDist3A2, NumSetsDist3A2, TotalNumGamesDist3A2, AllSetScoresDist3A2] = RunMarkovModel(P1,P2S,3,FirstToTBPoints,2,Viscosity, True)
        [MatchDist5A2, NumSetsDist5A2, TotalNumGamesDist5A2, AllSetScoresDist5A2] = RunMarkovModel(P1,P2S,5,FirstToTBPoints,2,Viscosity, True)

        # Append distributions for each scenario:
        MatchDistributions3A1.append(MatchDist3)
        NumberOfSetsDistributions3A1.append(NumSetsDist3)
        TotalNumberOfGamesDistributions3A1.append(TotalNumGamesDist3)
        AllSetScoresDistributions3A1.append(AllSetScoresDist3)
        MatchDistributions5A1.append(MatchDist5)
        NumberOfSetsDistributions5A1.append(NumSetsDist5)
        TotalNumberOfGamesDistributions5A1.append(TotalNumGamesDist5)
        AllSetScoresDistributions5A1.append(AllSetScoresDist5)

def FirstServerEffects():
    # Affect of the first server:
    P2S = 0.7 # Average probability of winning a point on serve
    P1S = np.arange(0.3, 0.9, 0.01).tolist()
    for S in P1S:
        [nodes, dist, parents, outcomes, info] = TennisSetNetwork(P1S, P2S, P1TB, P2TB)

        [MatchDist3]


if __name__ == "__main__":
    main()
    