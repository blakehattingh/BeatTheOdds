import numpy as np
import matplotlib.pyplot as plt
from RunMarkovModel import RunMarkovModel

def plotResults():
    P1S = [0.61, 0.65, 0.7]
    P2S = 0.6

    firstToSets = 3
    firstToTB = 7

    matchWinnerDistImp1 = []
    numGamesDistImp1 = []
    setScoreDistImp1 = []
    numSetsDistImp1 = []

    matchWinnerDistImp2 = []
    numGamesDistImp2 = []
    setScoreDistImp2 = []
    numSetsDistImp2 = []

    #[matchWinnerDistImp1, numGamesDistImp1,setScoreDistImp1, numSetsDistImp1] = RunMarkovModel(P1S[0], P2S, firstToSets, firstToTB,1, 1)



    for p1 in P1S:
        index = P1S.index(p1)

        matchWinnerDist, numGamesDist,\
            setScoreDist, numSetsDist = RunMarkovModel(p1, P2S, firstToSets, firstToTB, 1,1)
        matchWinnerDistImp1.append(matchWinnerDist)
        numGamesDistImp1.append(numGamesDist)
        setScoreDistImp1.append(setScoreDist)
        numSetsDistImp1.append(numSetsDist)
        
        #matchWinnerDistImp2[index], numGamesDistImp2[index],\
         #   setScoreDistImp2[index], numSetsDistImp2[index] = RunMarkovModel(p1, P2S, firstToSets, firstToTB, 1)

    serverTitles = ['P1','P2','P1','P2','P1','P2']
    labelLocation = np.arange(len(serverTitles))
    width = 0.25

    player1WinsDists = [matchWinnerDistImp1[0][0],matchWinnerDistImp1[1][0],matchWinnerDistImp1[2][0]]
    player2WinsDists = [matchWinnerDistImp1[0][1],matchWinnerDistImp1[1][1],matchWinnerDistImp1[2][1]]
    
    fig, axes = plt.subplots(2, 3, figsize = [15, 4.8])
    fig.suptitle('Probability Distributions')

    #Distribution for match winner
    #axes[0,0].bar(['Player 1', 'Player 2'], matchWinnerDistImp1)
    rects1 = axes[0,0].bar(labelLocation,player1WinsDists, width, color='r')
    rects2 = axes[0,0].bar(labelLocation+width,player2WinsDists, width, color='y')

    axes[0,0].set_ylabel('Probability')
    axes[0,0].set_title('Prob of player winning match')
    axes[0,0].set_xticks(labelLocation + width / 2)
    axes[0,0].set_xticklabels(('P1','P2','P1','P2','P1','P2'))


    #plt.savefig('probDists.png')
    plt.show()

def main():
    plotResults()

if __name__ == "__main__":
    main()