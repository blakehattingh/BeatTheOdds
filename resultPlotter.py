import numpy as np
import matplotlib.pyplot as plt

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

    for p1 in P1S:
        index = P1S.index(p1)

        matchWinnerDistImp1[index], numGamesDistImp1[index],\
            setScoreDistImp1[index], numSetsDistImp1[index] = runMatch(p1,P2S, firstToSets, firstToTB,1)
        
        matchWinnerDistImp2[index], numGamesDistImp2[index],\
            setScoreDistImp2[index], numSetsDistImp2[index] = runMatch(p1,P2S, firstToSets, firstToTB,2)
    
    fig, axes = plt.subplots(2, 3, figsize = [15, 4.8])
    fig.subtitle('Probability Distributions')

    #Distribution for match winner
    axes[0].bar()


