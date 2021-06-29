import numpy as np
import matplotlib.pyplot as plt


def plotMatchOutcome(matchData3S1A,matchData5S1A,matchData3S2A,matchData5S2A):
    serverTitles = ['P1 v P2','P1 v P2','P1 v P2']
    labelLocation = np.arange(len(serverTitles))
    width = 0.25

    player1WinsDists = [matchData3S1A[0][0],matchData3S1A[1][0],matchData3S1A[2][0]]
    player2WinsDists = [matchData3S1A[0][1],matchData3S1A[1][1],matchData3S1A[2][1]]

    '''player1WinsDists5S1A = [matchData5S1A[0][0],matchData5S1A[1][0],matchData5S1A[2][0]]
    player2WinsDists5S1A = [matchData5S1A[0][1],matchData5S1A[1][1],matchData5S1A[2][1]]

    player1WinsDists3S2A = [matchData3S2A[0][0],matchData3S2A[1][0],matchData3S2A[2][0]]
    player2WinsDists3S2A = [matchData3S2A[0][1],matchData3S2A[1][1],matchData3S2A[2][1]]

    player1WinsDists5S2A = [matchData5S2A[0][0],matchData5S2A[1][0],matchData5S2A[2][0]]
    player2WinsDists5S2A = [matchData5S2A[0][1],matchData5S2A[1][1],matchData5S2A[2][1]]'''

    fig, axes = plt.subplots(2, 2, figsize = [15, 12])
    fig.suptitle('Probability Distributions for match outcome')

    rects1 = axes[0,0].bar(labelLocation,player1WinsDists, width, color='r')
    rects2 = axes[0,0].bar(labelLocation+width,player2WinsDists, width, color='b')

    '''rects15S1A = axes[0,1].bar(labelLocation,player1WinsDists5S1A, width, color='r')
    rects25S1A = axes[0,1].bar(labelLocation+width,player2WinsDists5S1A, width, color='b')

    rects13S2A = axes[1,0].bar(labelLocation,player1WinsDists3S2A, width, color='r')
    rects23S2A = axes[1,0].bar(labelLocation+width,player2WinsDists3S2A, width, color='b')

    rects15S2A = axes[1,1].bar(labelLocation,player1WinsDists5S2A, width, color='r')
    rects25S2A = axes[1,1].bar(labelLocation+width,player2WinsDists5S2A, width, color='b')'''

    axes[0,0].legend((rects1[0], rects2[0]), ('Player 1', 'Player 2'))
    axes[0,0].set_ylabel('Probability')
    axes[0,0].set_xlabel('Serve Probability Differences')
    axes[0,0].set_title('Algorithm 1 - first to 3 sets')
    axes[0,0].set_xticks(labelLocation + width / 2)
    axes[0,0].set_xticklabels(('0.01','0.05','0.1'))

    '''axes[0,1].legend((rects15S1A[0], rects25S1A[0]), ('Player 1', 'Player 2'))
    axes[0,1].set_ylabel('Probability')
    axes[0,1].set_xlabel('Serve Probability Differences')
    axes[0,1].set_title('Algorithm 1 - first to 5 sets')
    axes[0,1].set_xticks(labelLocation + width / 2)
    axes[0,1].set_xticklabels(('0.01','0.05','0.1'))

    axes[1,0].legend((rects13S2A[0], rects23S2A[0]), ('Player 1', 'Player 2'))
    axes[1,0].set_ylabel('Probability')
    axes[1,0].set_xlabel('Serve Probability Differences')
    axes[1,0].set_title('Algorithm 2 - first to 3 sets')
    axes[1,0].set_xticks(labelLocation + width / 2)
    axes[1,0].set_xticklabels(('0.01','0.05','0.1'))

    axes[1,1].legend((rects15S2A[0], rects25S2A[0]), ('Player 1', 'Player 2'))
    axes[1,1].set_ylabel('Probability')
    axes[1,1].set_xlabel('Serve Probability Differences')
    axes[1,1].set_title('Algorithm 2 - first to 5 sets')
    axes[1,1].set_xticks(labelLocation + width / 2)
    axes[1,1].set_xticklabels(('0.01','0.05','0.1'))'''

    plt.show()


def plotNumberOfSets(setData3S1A,setData5S1A,setData3S2A,setData5S2A):
    n=3
    labelLocation3Sets = np.arange(n)
    labelLocation5Sets = np.arange(n)
    width = 0.25

    twoSetsDists3S1A = [setData3S1A[0][0],setData3S1A[1][0],setData3S1A[2][0]]
    threeSetsDists3S1A = [setData3S1A[0][1],setData3S1A[1][1],setData3S1A[2][1]]

    threeSetsDists5S1A = [setData5S1A[0][0],setData5S1A[1][0],setData5S1A[2][0]]
    fourSetsDists5S1A = [setData5S1A[0][1],setData5S1A[1][1],setData5S1A[2][1]]
    fiveSetsDists5S1A = [setData5S1A[0][2],setData5S1A[1][2],setData5S1A[2][2]]

    twoSetsDists3S2A = [setData3S2A[0][0],setData3S2A[1][0],setData3S2A[2][0]]
    threeSetsDists3S2A = [setData3S2A[0][1],setData3S2A[1][1],setData3S2A[2][1]]

    threeSetsDists5S2A = [setData5S2A[0][0],setData5S2A[1][0],setData5S2A[2][0]]
    fourSetsDists5S2A = [setData5S2A[0][1],setData5S2A[1][1],setData5S2A[2][1]]
    fiveSetsDists5S2A = [setData5S2A[0][2],setData5S2A[1][2],setData5S2A[2][2]]

    figSet, axesSet = plt.subplots(2, 2, figsize = [15, 12])
    figSet.suptitle('Probability Distributions for Number of Sets')

    rectsSets1 = axesSet[0,0].bar(labelLocation3Sets,twoSetsDists3S1A, width, color='r')
    rectsSets2 = axesSet[0,0].bar(labelLocation3Sets+width,threeSetsDists3S1A, width, color='b')

    rects1Sets5S1A = axesSet[0,1].bar(labelLocation5Sets-width,threeSetsDists5S1A, width, color='b')
    rects2Sets5S1A = axesSet[0,1].bar(labelLocation5Sets,fourSetsDists5S1A, width, color='y')
    rects3Sets5S1A = axesSet[0,1].bar(labelLocation5Sets+width,fiveSetsDists5S1A, width, color='g')

    rects1Sets3S2A = axesSet[1,0].bar(labelLocation3Sets,twoSetsDists3S2A, width, color='r')
    rects2Sets3S2A = axesSet[1,0].bar(labelLocation3Sets+width,threeSetsDists3S2A, width, color='b')

    rects1Sets5S2A = axesSet[1,1].bar(labelLocation5Sets-width,threeSetsDists5S2A, width, color='b')
    rects2Sets5S2A = axesSet[1,1].bar(labelLocation5Sets,fourSetsDists5S2A, width, color='y')
    rects3Sets5S2A = axesSet[1,1].bar(labelLocation5Sets+width,fiveSetsDists5S2A, width, color='g')

    axesSet[0,0].legend((rectsSets1[0], rectsSets2[0]), ('2 sets', '3 sets'))
    axesSet[0,0].set_ylabel('Probability')
    axesSet[0,0].set_xlabel('Serve Probability Differences')
    axesSet[0,0].set_title('Algorithm 1 - first to 3 sets')
    axesSet[0,0].set_xticks(labelLocation3Sets + width / 2)
    axesSet[0,0].set_xticklabels(('0.01','0.05','0.1'))

    axesSet[0,1].legend((rects1Sets5S1A[0], rects2Sets5S1A[0],rects3Sets5S1A[0]), ('3 sets', '4 sets', '5 sets'))
    axesSet[0,1].set_ylabel('Probability')
    axesSet[0,1].set_xlabel('Serve Probability Differences')
    axesSet[0,1].set_title('Algorithm 1 - first to 5 sets')
    axesSet[0,1].set_xticks(labelLocation5Sets + width / 2)
    axesSet[0,1].set_xticklabels(('0.01','0.05','0.1'))

    axesSet[1,0].legend((rects1Sets3S2A[0], rects2Sets3S2A[0]), ('2 sets', '3 sets'))
    axesSet[1,0].set_ylabel('Probability')
    axesSet[1,0].set_xlabel('Serve Probability Differences')
    axesSet[1,0].set_title('Algorithm 2 - first to 3 sets')
    axesSet[1,0].set_xticks(labelLocation3Sets + width / 2)
    axesSet[1,0].set_xticklabels(('0.01','0.05','0.1'))

    axesSet[1,1].legend((rects1Sets5S2A[0], rects2Sets5S2A[0], rects3Sets5S2A[0]), ('3 sets', '4 sets', '5 sets'))
    axesSet[1,1].set_ylabel('Probability')
    axesSet[1,1].set_xlabel('Serve Probability Differences')
    axesSet[1,1].set_title('Algorithm 2 - first to 5 sets')
    axesSet[1,1].set_xticks(labelLocation5Sets + width / 2)
    axesSet[1,1].set_xticklabels(('0.01','0.05','0.1'))

    plt.show()

    



def plotNumberOfGames(numGamesData3SA1, numGamesData3SA2, numGamesData5SA1, numGamesData5SA2):
    figGames3S, axesGames3S = plt.subplots(2, 3, figsize = [15, 12])
    figGames3S.suptitle('Probability Distributions for Number of Games (first to 3 sets)')

    axesGames3S[0][0].bar(list(range(12,66)), numGamesData3SA1[0])
    axesGames3S[0][1].bar(list(range(12,66)), numGamesData3SA1[1])
    axesGames3S[0][2].bar(list(range(12,66)), numGamesData3SA1[2])

    axesGames3S[1][0].bar(list(range(12,66)), numGamesData3SA2[0])
    axesGames3S[1][1].bar(list(range(12,66)), numGamesData3SA2[1])
    axesGames3S[1][2].bar(list(range(12,66)), numGamesData3SA2[2])

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

    #Number of games for first to 5 sets

    figGames5S, axesGames5S = plt.subplots(2, 3, figsize = [15, 12])
    figGames5S.suptitle('Probability Distributions for Number of Games (first to 5 sets)')

    axesGames5S[0][0].bar(range(18,66,1), numGamesData5SA1[0])
    axesGames5S[0][1].bar(range(18,66,1), numGamesData5SA1[1])
    axesGames5S[0][2].bar(range(18,66,1), numGamesData5SA1[2])

    axesGames5S[1][0].bar(range(18,66,1), numGamesData5SA2[0])
    axesGames5S[1][1].bar(range(18,66,1), numGamesData5SA2[1])
    axesGames5S[1][2].bar(range(18,66,1), numGamesData5SA2[2])

    axesGames5S[0,0].set_ylabel('Probability')
    axesGames5S[0,0].set_xlabel('Number of Games')
    axesGames5S[0,0].set_title('Alg 1 - first to 5 sets - 0.01 serve prob diff')

    axesGames5S[0,1].set_ylabel('Probability')
    axesGames5S[0,1].set_xlabel('Number of Games')
    axesGames5S[0,1].set_title('Alg 1 - first to 5 sets - 0.05 serve prob diff')

    axesGames5S[0,2].set_ylabel('Probability')
    axesGames5S[0,2].set_xlabel('Number of Games')
    axesGames5S[0,2].set_title('Alg 1 - first to 5 sets - 0.1 serve prob diff')

    axesGames5S[1,0].set_ylabel('Probability')
    axesGames5S[1,0].set_xlabel('Number of Games')
    axesGames5S[1,0].set_title('Alg 2 - first to 5 sets - 0.01 serve prob diff')

    axesGames5S[1,1].set_ylabel('Probability')
    axesGames5S[1,1].set_xlabel('Number of Games')
    axesGames5S[1,1].set_title('Alg 2 - first to 5 sets - 0.05 serve prob diff')

    axesGames5S[1,2].set_ylabel('Probability')
    axesGames5S[1,2].set_xlabel('Number of Games')
    axesGames5S[1,2].set_title('Alg 2 - first to 5 sets - 0.1 serve prob diff')

    plt.show()



def plotSetScore(setScoreData3SA1,setScoreData3SA2,setScoreData5SA1,setScoreData5SA2):
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

    #Set Score Probabilities for first to 5 sets

    figSetScore5S, axesSetScore5S = plt.subplots(2, 3, figsize = [15, 12])
    figSetScore5S.suptitle('Probability Distributions for Set Scores(first to 5 sets)')

    axesSetScore5S[0][0].bar(AllSetScoreOutcomes, setScoreData5SA1[0])
    axesSetScore5S[0][1].bar(AllSetScoreOutcomes, setScoreData5SA1[1])
    axesSetScore5S[0][2].bar(AllSetScoreOutcomes, setScoreData5SA1[2])

    axesSetScore5S[1][0].bar(AllSetScoreOutcomes, setScoreData5SA2[0])
    axesSetScore5S[1][1].bar(AllSetScoreOutcomes, setScoreData5SA2[1])
    axesSetScore5S[1][2].bar(AllSetScoreOutcomes, setScoreData5SA2[2])

    axesSetScore5S[0,0].set_ylabel('Probability')
    axesSetScore5S[0,0].set_xlabel('Set Scores')
    axesSetScore5S[0,0].set_title('Alg 1 - first to 5 sets - 0.01 serve prob diff')

    axesSetScore5S[0,1].set_ylabel('Probability')
    axesSetScore5S[0,1].set_xlabel('Set Scores')
    axesSetScore5S[0,1].set_title('Alg 1 - first to 5 sets - 0.05 serve prob diff')

    axesSetScore5S[0,2].set_ylabel('Probability')
    axesSetScore5S[0,2].set_xlabel('Set Scores')
    axesSetScore5S[0,2].set_title('Alg 1 - first to 5 sets - 0.1 serve prob diff')

    axesSetScore5S[1,0].set_ylabel('Probability')
    axesSetScore5S[1,0].set_xlabel('Set Scores')
    axesSetScore5S[1,0].set_title('Alg 2 - first to 5 sets - 0.01 serve prob diff')

    axesSetScore5S[1,1].set_ylabel('Probability')
    axesSetScore5S[1,1].set_xlabel('Set Scores')
    axesSetScore5S[1,1].set_title('Alg 2 - first to 5 sets - 0.05 serve prob diff')

    axesSetScore5S[1,2].set_ylabel('Probability')
    axesSetScore5S[1,2].set_xlabel('Set Scores')
    axesSetScore5S[1,2].set_title('Alg 2 - first to 5 sets - 0.1 serve prob diff')

    plt.show()
