from RunMarkovModel import RunMarkovModel
from TennisSetNetwork import TennisSetNetwork
import sys

# This script is a test suite for all the unit tests for functions contributing to our Markov Model.

# Functions to test:
# 1) ComputeTBProbabilities (Additional Functions)
# 2) TennisSetNetwork
# 3) TennisMatchNetwork1
# 4) TennisMatchNetwork2
# 5) RunMarkovModel

# Testing ComputeTBProbabilities:
# 1) Tests if the correct TB probabilities (approximately) are returned for a given P1S and P2S

# Testing TennisSetNetwork:
# 2Set) Tests if the 'Set' node has the correct distributions for a given sequence of game outcomes.
# 2SetScore) Tests if the 'SetScore' node has the correct distributions for a given sequence of game outcomes.
# 2NumGames) Tests if the 'NumGames' node has the correct distributions for a given sequence of game outcomes.

# Testing TennisMatchNetwork1:

# Testing TennisMatchNetwork2:

# Testing RunMarkovModel:
# 5a) Tests if the first implementation returns uniform distributions when P1S == P2S
# 5b) Tests if the Second Implementation returns uniform distributions when P1S == P2S
# 5c) Tests if the first implementation returns qualitatively conrrect distributions when P2S >> P1S
# 5d) Tests if the second implementation returns qualitatively conrrect distributions when P2S >> P1S

# 3) 

def TestSuite():
    UnitTestSet()
    UnitTestSetScores()
    UnitTest1()

def UnitTest1():
    # Run our model using the first implementation:
    Sets = [3,5]
    Ps = [0.6, 0.9]
    counta = 0
    countb = 0
    for s in Sets:
        for P in Ps:
            [MatchDista, NumSetsDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P, P, s, 7, 1, 0.)
            [MatchDistb, NumSetsDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P, P, s, 7, 2, 0.5)

            # Check for a uniform match distriubtion:
            if (abs(MatchDista[0] - MatchDista[1]) < 0.001):
                counta = counta + 1
            if (abs(MatchDistb[0] - MatchDistb[1]) < 0.001):
                countb = countb + 1

    if (counta == 4):
        print('Test 1a Passed')
    else:
        print('Test 1a Failed')
    if (countb == 4):
        print('Test 1b Passed')

def UnitTestSet():
    # Set up a "Set Network":
    [nodes, dist, parents, outcomes, info] = TennisSetNetwork(0.8, 0.6, 0.85, 0.15)
    
    # Check several different scorelines get the correct set winner:
    if (dist['Set'][1,1,1,1,1,2,2,2,2,2,2,2,2] != [0., 1.]):
        print('Set Test Failed')
    elif (dist['Set'][2,2,2,2,2,1,1,1,1,1,1,1,1] != [1., 0.]):
        print('Set Test Failed')
    elif (dist['Set'][1,2,1,2,1,2,1,2,1,2,1,2,2] != [0., 1.]):
        print('Set Test Failed')
    elif (dist['Set'][2,2,1,2,1,2,1,1,1,1,1,1,1] != [1., 0.]):
        print('Set Test Failed')
    elif (dist['Set'][1,1,2,2,2,2,1,1,2,1,1,2,1] != [1., 0.]):
        print('Set Test Failed')
    else:
        print('Set Test Passed')

def UnitTestSetScores():
    # Set up a "Set Network":
    [nodes, dist, parents, outcomes, info] = TennisSetNetwork(0.8, 0.6, 0.85, 0.15)
    SetScores = ["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]

    # Check several different scorelines get the correct set score:
    if (dist['SetScore'][1,1,1,1,1,2,2,2,2,2,2,2,2] != [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,0.]): # Set Score = 5-7
        print('Set Scores Test Failed')
    elif (dist['SetScore'][2,2,2,2,2,1,1,1,1,1,1,1,1] != [0.,0.,0.,0.,0.,1.,0.,0.,0.,0.,0.,0.,0.,0.]): # Set Score = 7-5
        print('Set Scores Test Failed')
    elif (dist['SetScore'][1,2,1,2,1,2,1,2,1,2,1,2,2] != [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.]): # Set Score = 6-7
        print('Set Scores Test Failed')
    elif (dist['SetScore'][2,2,1,2,1,2,1,1,1,1,1,1,1] != [0.,0.,0.,0.,1.,0.,0.,0.,0.,0.,0.,0.,0.,0.]): # Set Score = 6-4
        print('Set Scores Test Failed')
    elif (dist['SetScore'][1,1,2,2,2,2,1,1,2,1,1,2,1] != [0.,0.,0.,0.,0.,0.,1.,0.,0.,0.,0.,0.,0.,0.]): # Set Score = 7-6
        print('Set Scores Test Failed')
    else:
        print('Set Scores Test Passed')


if __name__ == "__main__":
    TestSuite()
    