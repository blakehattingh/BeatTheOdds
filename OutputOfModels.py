from AdditionalFunctions import ComputeTBProbabilities
from RunMarkovModel import RunMarkovModel
from TennisSetNetwork import TennisSetNetwork
from loopybeliefprop import beliefpropagation
import numpy as np
import matplotlib.pyplot as plt

def main():
    # This file runs each implementation, for each of the 3 scenarios and outputs each distribution as a plot.

    # Scenarios:
    P2S = 0.7
    P1S = [0.71, 0.75, 0.8]
    FirstToTBPoints = 7
    Viscosity = 0.5

    # Distributions:
    MatchDistributions3A1 = []
    MatchScoreDistributions3A1 = []
    TotalNumberOfGamesDistributions3A1 = []
    AllSetScoresDistributions3A1 = []
    MatchDistributions3A2 = []
    MatchScoreDistributions3A2 = []
    #NumSetsDistributions3A2 = []
    TotalNumberOfGamesDistributions3A2 = []
    AllSetScoresDistributions3A2 = []
    #MatchDistributions5 = []
    #NumberOfSetsDistributions5 = []
    #TotalNumberOfGamesDistributions5 = []
    #AllSetScoresDistributions5 = []

    # Possible Outcomes:
    MatchOutcomes = ['Player 1 Wins', 'Player 2 Wins']
    NumberOfSetsOutcomes = [2,3,4,5]
    MatchScoreOutcomes = ["2-0", "2-1", "0-2", "1-2"]
    TotalNumberOfGamesOutcomes = list(range(12,40))
    AllSetScoreOutcomes = ["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]

    # First Implementation:
    Approach = 1
    for P1 in P1S:
        [MatchDist3A1, MatchScoreDist3A1, TotalNumGamesDist3A1, AllSetScoresDist3A1] = RunMarkovModel(P1,P2S,3,FirstToTBPoints,Approach,Viscosity)
        #[MatchDist5, NumSetsDist5, TotalNumGamesDist5, AllSetScoresDist5] = RunMarkovModel(P1,P2S,5,FirstToTBPoints,Approach,Viscosity)

        ####[MatchDist3A2, MatchScoreDist3A2, TotalNumGamesDist3A2, AllSetScoresDist3A2] = RunMarkovModel(P1,P2S,3,FirstToTBPoints,2,Viscosity)

        #[MatchDist5A2, NumSetsDist5A2, TotalNumGamesDist5A2, AllSetScoresDist5A2] = RunMarkovModel(P1,P2S,5,FirstToTBPoints,2,Viscosity,'Complex')

        # Append distributions for each scenario:
        MatchDistributions3A1.append(MatchDist3A1)
        MatchScoreDistributions3A1.append(MatchScoreDist3A1)
        TotalNumberOfGamesDistributions3A1.append(TotalNumGamesDist3A1)
        AllSetScoresDistributions3A1.append(AllSetScoresDist3A1)

        #UNCOMMENT !!!!!
        #MatchDistributions3A2.append(MatchDist3A2)
        #MatchScoreDistributions3A2.append(MatchScoreDist3A2)
        #TotalNumberOfGamesDistributions3A2.append(TotalNumGamesDist3A2)
        #AllSetScoresDistributions3A2.append(AllSetScoresDist3A2)

        #JUST FOR TRIAL RUN
        MatchDistributions3A2.append(MatchDist3A1)
        MatchScoreDistributions3A2.append(MatchScoreDist3A1)
        TotalNumberOfGamesDistributions3A2.append(TotalNumGamesDist3A1)
        AllSetScoresDistributions3A2.append(AllSetScoresDist3A1)
        

    plotMatchOutcome(MatchDistributions3A1, MatchDistributions3A2)
    plotNumberOfGames(TotalNumberOfGamesDistributions3A1, TotalNumberOfGamesDistributions3A2)
    plotSetScore(AllSetScoresDistributions3A1, AllSetScoresDistributions3A2)
    #plotNumberOfSets(NumberOfSetsDistributions3A1, NumberOfSetsDistributions5A1, NumberOfSetsDistributions3A2, NumberOfSetsDistributions5A2)
    plotMatchScore(MatchScoreDistributions3A1,MatchScoreDistributions3A2)


def plotMatchOutcome(matchDist3A1, matchDist3A2):
    serverTitles = ['P1 v P2','P1 v P2','P1 v P2']
    labelLocation = np.arange(len(serverTitles))
    width = 0.25
    figMatch, axes = plt.subplots(1, 2, figsize = [15, 12])
    figMatch.suptitle('Probability Distributions for match outcome')

    player1WinsDists = [matchDist3A1[0][0],matchDist3A1[1][0],matchDist3A1[2][0]]
    player2WinsDists = [matchDist3A1[0][1],matchDist3A1[1][1],matchDist3A1[2][1]]

    player1WinsDists3S2A = [matchDist3A2[0][0],matchDist3A2[1][0],matchDist3A2[2][0]]
    player2WinsDists3S2A = [matchDist3A2[0][1],matchDist3A2[1][1],matchDist3A2[2][1]]

    rects1 = axes[0].bar(labelLocation,player1WinsDists, width, color='r')
    rects2 = axes[0].bar(labelLocation+width,player2WinsDists, width, color='b')

    rects13S2A = axes[1].bar(labelLocation,player1WinsDists3S2A, width, color='r')
    rects23S2A = axes[1].bar(labelLocation+width,player2WinsDists3S2A, width, color='b')


    axes[0].legend((rects1[0], rects2[0]), ('Player 1', 'Player 2'))
    axes[0].set_ylabel('Probability')
    axes[0].set_xlabel('Serve Probability Differences')
    axes[0].set_title('Algorithm 1 - first to 3 sets')
    axes[0].set_xticks(labelLocation + width / 2)
    axes[0].set_xticklabels(('0.01','0.05','0.1'))

    axes[1].legend((rects13S2A[0], rects23S2A[0]), ('Player 1', 'Player 2'))
    axes[1].set_ylabel('Probability')
    axes[1].set_xlabel('Serve Probability Differences')
    axes[1].set_title('Algorithm 2 - first to 3 sets')
    axes[1].set_xticks(labelLocation + width / 2)
    axes[1].set_xticklabels(('0.01','0.05','0.1'))

    plt.savefig('matchOutcomeDistribution.png')

def plotNumberOfGames(numGamesData3SA1,numGamesData3SA2):
    figGames3S, axesGames3S = plt.subplots(2, 3, figsize = [15, 12])
    figGames3S.suptitle('Probability Distributions for Number of Games (first to 3 sets)')

    axesGames3S[0][0].bar(range(12,40,1), numGamesData3SA1[0])
    axesGames3S[0][1].bar(range(12,40,1), numGamesData3SA1[1])
    axesGames3S[0][2].bar(range(12,40,1), numGamesData3SA1[2])

    axesGames3S[1][0].bar(range(12,40,1), numGamesData3SA2[0])
    axesGames3S[1][1].bar(range(12,40,1), numGamesData3SA2[1])
    axesGames3S[1][2].bar(range(12,40,1), numGamesData3SA2[2])

    axesGames3S[0,0].set_ylabel('Probability')
    axesGames3S[0,0].set_xlabel('Number of Games')
    axesGames3S[0,0].set_title('Alg 1 - first to 3 sets - 0.01 serve prob diff')

    axesGames3S[0,1].set_ylabel('Probability')
    axesGames3S[0,1].set_xlabel('Number of Games')
    axesGames3S[0,1].set_title('Alg 1 - first to 3 sets - 0.05 serve prob diff')

    axesGames3S[0,2].set_ylabel('Probability')
    axesGames3S[0,2].set_xlabel('Number of Games')
    axesGames3S[0,2].set_title('Alg 1 - first to 3 sets - 0.1 serve prob diff')

    axesGames3S[1,0].set_ylabel('Probability')
    axesGames3S[1,0].set_xlabel('Number of Games')
    axesGames3S[1,0].set_title('Alg 2 - first to 3 sets - 0.01 serve prob diff')

    axesGames3S[1,1].set_ylabel('Probability')
    axesGames3S[1,1].set_xlabel('Number of Games')
    axesGames3S[1,1].set_title('Alg 2 - first to 3 sets - 0.05 serve prob diff')

    axesGames3S[1,2].set_ylabel('Probability')
    axesGames3S[1,2].set_xlabel('Number of Games')
    axesGames3S[1,2].set_title('Alg 2 - first to 3 sets - 0.1 serve prob diff')

    plt.savefig('numGamesDistribution.png')

def plotSetScore(setScoreData3SA1,setScoreData3SA2):
    AllSetScoreOutcomes = ["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]
    figSetScore3S, axesSetScore3S = plt.subplots(2, 3, figsize = [15, 12])
    figSetScore3S.suptitle('Probability Distributions for Set Scores(first to 3 sets)')

    axesSetScore3S[0][0].bar(AllSetScoreOutcomes, setScoreData3SA1[0])
    axesSetScore3S[0][1].bar(AllSetScoreOutcomes, setScoreData3SA1[1])
    axesSetScore3S[0][2].bar(AllSetScoreOutcomes, setScoreData3SA1[2])

    axesSetScore3S[1][0].bar(AllSetScoreOutcomes, setScoreData3SA2[0])
    axesSetScore3S[1][1].bar(AllSetScoreOutcomes, setScoreData3SA2[1])
    axesSetScore3S[1][2].bar(AllSetScoreOutcomes, setScoreData3SA2[2])

    axesSetScore3S[0,0].set_ylabel('Probability')
    axesSetScore3S[0,0].set_xlabel('Set Scores')
    axesSetScore3S[0,0].set_title('Alg 1 - first to 3 sets - 0.01 serve prob diff')

    axesSetScore3S[0,1].set_ylabel('Probability')
    axesSetScore3S[0,1].set_xlabel('Set Scores')
    axesSetScore3S[0,1].set_title('Alg 1 - first to 3 sets - 0.05 serve prob diff')

    axesSetScore3S[0,2].set_ylabel('Probability')
    axesSetScore3S[0,2].set_xlabel('Set Scores')
    axesSetScore3S[0,2].set_title('Alg 1 - first to 3 sets - 0.1 serve prob diff')

    axesSetScore3S[1,0].set_ylabel('Probability')
    axesSetScore3S[1,0].set_xlabel('Set Scores')
    axesSetScore3S[1,0].set_title('Alg 2 - first to 3 sets - 0.01 serve prob diff')

    axesSetScore3S[1,1].set_ylabel('Probability')
    axesSetScore3S[1,1].set_xlabel('Set Scores')
    axesSetScore3S[1,1].set_title('Alg 2 - first to 3 sets - 0.05 serve prob diff')

    axesSetScore3S[1,2].set_ylabel('Probability')
    axesSetScore3S[1,2].set_xlabel('Set Scores')
    axesSetScore3S[1,2].set_title('Alg 2 - first to 3 sets - 0.1 serve prob diff')

    plt.savefig('SetScoreDistribution.png')

def plotMatchScore(MatchScoreData3S1A,MatchScoreData3S2A):
    labelLocation3Sets = np.arange(3)
    width = 0.2

    twoZeroDists3S1A = [MatchScoreData3S1A[0][0],MatchScoreData3S1A[1][0],MatchScoreData3S1A[2][0]]
    twoOneDists3S1A = [MatchScoreData3S1A[0][1],MatchScoreData3S1A[1][1],MatchScoreData3S1A[2][1]]
    zeroTwoDists3S1A = [MatchScoreData3S1A[0][2],MatchScoreData3S1A[1][2],MatchScoreData3S1A[2][2]]
    oneTwoDists3S1A = [MatchScoreData3S1A[0][3],MatchScoreData3S1A[1][3],MatchScoreData3S1A[2][3]]

    twoZeroDists3S2A = [MatchScoreData3S2A[0][0],MatchScoreData3S2A[1][0],MatchScoreData3S2A[2][0]]
    twoOneDists3S2A = [MatchScoreData3S2A[0][1],MatchScoreData3S2A[1][1],MatchScoreData3S2A[2][1]]
    zeroTwoDists3S2A = [MatchScoreData3S2A[0][2],MatchScoreData3S2A[1][2],MatchScoreData3S2A[2][2]]
    oneTwoDists3S2A = [MatchScoreData3S2A[0][3],MatchScoreData3S2A[1][3],MatchScoreData3S2A[2][3]]

    figSet, axesSet = plt.subplots(1, 2, figsize = [20, 12])
    figSet.suptitle('Probability Distributions for MatchScore', fontsize=20)

    rectsMatchScore1 = axesSet[0].bar(labelLocation3Sets-width,twoZeroDists3S1A, width, color='y')
    rectsMatchScore2 = axesSet[0].bar(labelLocation3Sets,twoOneDists3S1A, width, color='b')
    rectsMatchScore3 = axesSet[0].bar(labelLocation3Sets+width,zeroTwoDists3S1A, width, color='g')
    rectsMatchScore4 = axesSet[0].bar(labelLocation3Sets+(2*width),oneTwoDists3S1A , width, color='k')

    rects1MatchScore3S2A = axesSet[1].bar(labelLocation3Sets-width,twoZeroDists3S2A, width, color='y')
    rects2MatchScore3S2A = axesSet[1].bar(labelLocation3Sets,twoOneDists3S2A, width, color='b')
    rects3MatchScore3S2A = axesSet[1].bar(labelLocation3Sets+width,zeroTwoDists3S2A, width, color='g')
    rects3MatchScore3S2A = axesSet[1].bar(labelLocation3Sets+(2*width),oneTwoDists3S2A, width, color='k')


    axesSet[0].legend((rectsMatchScore1[0], rectsMatchScore2[0], rectsMatchScore3[0], rectsMatchScore4[0] ), ('2-0', '2-1','0-2', '1-2'), fontsize=15)
    axesSet[0].set_ylabel('Probability', fontsize=15)
    axesSet[0].set_xlabel('Serve Probability Differences', fontsize=15)
    axesSet[0].set_title('Algorithm 1 - first to 3 sets', fontsize=15)
    axesSet[0].set_xticks(labelLocation3Sets + width / 2)
    axesSet[0].set_xticklabels(('0.01','0.05','0.1'), fontsize=15)

    axesSet[1].legend((rects1MatchScore3S2A [0], rects2MatchScore3S2A[0],rects3MatchScore3S2A[0], rects3MatchScore3S2A[0]), ('2-0', '2-1','0-2', '1-2'), fontsize=15)
    axesSet[1].set_ylabel('Probability', fontsize=15)
    axesSet[1].set_xlabel('Serve Probability Differences', fontsize=15)
    axesSet[1].set_title('Algorithm 2 - first to 3 sets', fontsize=15)
    axesSet[1].set_xticks(labelLocation3Sets + width / 2)
    axesSet[1].set_xticklabels(('0.01','0.05','0.1'), fontsize=15)

    plt.savefig('matchScoreDistribution.png')


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
    Scenarios = ['0.01', '0.05', '0.10']
    Servers = [[1., 0.], [0.5, 0.5], [0., 1.]]
    SetDistributions = []
    GameDistributions = []
    for S in P1S:
        # Compute TB Probs:
        [P1TB, P2TB] = ComputeTBProbabilities(S, P2S)
        for Server in Servers:
            [nodes, dist, parents, outcomes, info] = TennisSetNetwork(S, P2S, P1TB, P2TB, Server)
            [SetDist, G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,G11,G12,TB] = beliefpropagation(nodes, dist, parents, outcomes, info, Iterations, 
            Tol, ['Set', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'TB'], Viscosity)
            SetDistributions.append(SetDist.tolist())
            Games = [G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,G11,G12,TB]
            GameDistributions.append(Games)

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
    