from AdditionalFunctions import ComputeTBProbabilities
from RunMarkovModel import RunMarkovModel
from TennisSetNetwork import TennisSetNetwork
from loopybeliefprop import beliefpropagation
from resultPlotter import plotMatchOutcome
from resultPlotter import plotMatchOutcome
from resultPlotter import plotNumberOfGames
from resultPlotter import plotNumberOfSets
from resultPlotter import plotSetScore
import numpy as np
import matplotlib.pyplot as plt

def main():
    # This file runs each implementation, for each of the 3 scenarios and outputs each distribution as a plot.

    # Scenarios:
    P2S = 0.7
    P1S = [0.71] #, 0.75, 0.8]
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
        #[MatchDist5, NumSetsDist5, TotalNumGamesDist5, AllSetScoresDist5] = RunMarkovModel(P1,P2S,5,FirstToTBPoints,Approach,Viscosity)

        #[MatchDist3A2, NumSetsDist3A2, TotalNumGamesDist3A2, AllSetScoresDist3A2] = RunMarkovModel(P1,P2S,3,FirstToTBPoints,2,Viscosity, True)
        #[MatchDist5A2, NumSetsDist5A2, TotalNumGamesDist5A2, AllSetScoresDist5A2] = RunMarkovModel(P1,P2S,5,FirstToTBPoints,2,Viscosity, True)

        # Append distributions for each scenario:
        MatchDistributions3A1.append(MatchDist3)
        NumberOfSetsDistributions3A1.append(NumSetsDist3)
        TotalNumberOfGamesDistributions3A1.append(TotalNumGamesDist3)
        AllSetScoresDistributions3A1.append(AllSetScoresDist3)
        '''MatchDistributions5A1.append(MatchDist5)
        NumberOfSetsDistributions5A1.append(NumSetsDist5)
        TotalNumberOfGamesDistributions5A1.append(TotalNumGamesDist5)
        AllSetScoresDistributions5A1.append(AllSetScoresDist5)

        MatchDistributions3A1.append(MatchDist3A2)
        NumberOfSetsDistributions3A1.append(NumSetsDist3A2)
        TotalNumberOfGamesDistributions3A1.append(TotalNumGamesDist3A2)
        AllSetScoresDistributions3A1.append(AllSetScoresDist3A2)
        MatchDistributions5A1.append(MatchDist5A2)
        NumberOfSetsDistributions5A1.append(NumSetsDist5A2)
        TotalNumberOfGamesDistributions5A1.append(TotalNumGamesDist5A2)
        AllSetScoresDistributions5A1.append(AllSetScoresDist5A2)'''

        #plotMatchOutcome(MatchDistributions3A1, MatchDistributions5A1, MatchDistributions3A2, MatchDistributions5A2)
        #plotNumberOfSets(NumberOfSetsDistributions3A1, NumberOfSetsDistributions5A1, NumberOfSetsDistributions3A2, NumberOfSetsDistributions5A2)
        plotNumberOfGames(TotalNumberOfGamesDistributions3A1, TotalNumberOfGamesDistributions3A2, TotalNumberOfGamesDistributions5A1, TotalNumberOfGamesDistributions5A2)
        plotSetScore(AllSetScoresDistributions3A1, AllSetScoresDistributions3A2, AllSetScoresDistributions5A1, AllSetScoresDistributions5A2)

def FirstServerEffects():
    # This function visualises the effect of knowing the first server of a match.
    # It shows how the probability of a player winning a set changes if they serve first versus if they recieve first.
    # It also shows the affect that the value of P1S has on this relationship.

    # Parameters:
    Iterations = 100
    Tol = 0.0001
    Viscosity = 0.5

    # Plot 1:
    # - PServe difference vs Probability of Player 1 winning a set (grouped bargraph)
    P2S = 0.7 # Average probability of winning a point on serve
    P1S = [0.71, 0.75, 0.80]
    Scenarios = [[1., 0.], [0.5, 0.5], [0., 1.]]
    SetDistributions = []
    GameDistributions = []
    for S in P1S:
        # Compute TB Probs:
        [P1TB, P2TB] = ComputeTBProbabilities(S, P2S)
        for Scen in Scenarios:
            [nodes, dist, parents, outcomes, info] = TennisSetNetwork(S, P2S, P1TB, P2TB, Scen)
            [SetDist, G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,G11,G12,TB] = beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, 
            Tol, ['Set', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'TB'], Viscosity)
            SetDistributions.append(SetDist.tolist())
            Games = [G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,G11,G12,TB]
            GameDistributions.append(Games)
    
    print(SetDistributions)
    print(GameDistributions)

    # Split Game distributions up:
    FS1 = [SetDistributions[0][0], SetDistributions[3][0], SetDistributions[6][0]]
    FSE = [SetDistributions[1][0], SetDistributions[4][0], SetDistributions[7][0]]
    FS2 = [SetDistributions[2][0], SetDistributions[5][0], SetDistributions[8][0]]

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
    
    # Plot 2:
    # - Player 1 serving ability vs Difference in probability between serving first and receiving first (line graph)
    # - Each line on the graph corresponds to a different difference in serving abilities
    # A = PServe difference of 0.01
    # B = PServe difference of 0.05
    # C = PServe differnece of 0.1

    if False:
        P1S = np.arange(0.5, 0.95, 0.05).tolist()
        SetDistributions2 = []
        Differences = [0.01, 0.05, 0.10]
        for S in P1S:
            for D in Differences:
                # Compute TB Probs:
                [P1TB, P2TB] = ComputeTBProbabilities(S, S - D)

                for Scen in Scenarios:
                    # Set up network:
                    [nodes, dist, parents, outcomes, info] = TennisSetNetwork(S, S - D, P1TB, P2TB, Scen)
                    SetDist = beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, Tol, ['Set'], Viscosity)
                    SetDistributions2.append(SetDist.to_list())
        
        print(SetDistributions2)

if __name__ == "__main__":
    main()
    