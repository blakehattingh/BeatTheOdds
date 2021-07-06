from RunMarkovModel import RunMarkovModel
from TennisSetNetwork import TennisSetNetwork
from TennisMatchNetwork2 import TennisMatchNetwork2
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
# a. and and b. for 3 and 5 sets respectively.
# 3NumSets) Tests if the 'NumSets' node has the correct distributions for a given sequence of set outcomes.
# 3Match) Tests if the 'Match' node has the correct distributions for a given sequence of set outcomes.
# 3TotalNumGames) Tests if the 'TotalNumGames' node has the correct distributions for a given sequence of NumSets and Number of games.
# 3AllSetScores) Tests if the 'AllSetScores' node has the correct distributions for a given sequence of set scores.

# Testing TennisMatchNetwork2:
# a. and and b. for 3 and 5 sets respectively.
# 4NumSets) Tests if the 'NumSets' node has the correct distributions for a given sequence of set outcomes.
# 4Match) Tests if the 'Match' node has the correct distributions for a given sequence of set outcomes.
# 4TotalNumGames) Tests if the 'TotalNumGames' node has the correct distributions for a given sequence of NumSets and Number of games.
# 4AllSetScores) Tests if the 'AllSetScores' node has the correct distributions for a given sequence of set scores.

# Testing RunMarkovModel:
# 5a) Tests if the first implementation returns uniform distributions when P1S == P2S
# 5b) Tests if the Second Implementation returns uniform distributions when P1S == P2S
# 5c) Tests if the first implementation returns qualitatively conrrect distributions when P2S >> P1S
# 5d) Tests if the second implementation returns qualitatively conrrect distributions when P2S >> P1S

# 3) 

def TestSuite():
    UnitTest2Set()
    UnitTest2SetScores()
    UnitTest2NumGames()
    # UnitTest1()

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

def UnitTest2Set():
    # Set up a "Set Network":
    [nodes, dist, parents, outcomes, info] = TennisSetNetwork(0.8, 0.6, 0.85, 0.15)
    
    # Check several different scorelines get the correct set winner:
    if (dist['Set'][1,1,1,1,1,2,2,2,2,2,2,2,2] != [0., 1.]):
        print('2. et Test Failed')
    elif (dist['Set'][2,2,2,2,2,1,1,1,1,1,1,1,1] != [1., 0.]):
        print('2. Set Test Failed')
    elif (dist['Set'][1,2,1,2,1,2,1,2,1,2,1,2,2] != [0., 1.]):
        print('2. Set Test Failed')
    elif (dist['Set'][2,2,1,2,1,2,1,1,1,1,1,1,1] != [1., 0.]):
        print('2. Set Test Failed')
    elif (dist['Set'][1,1,2,2,2,2,1,1,2,1,1,2,1] != [1., 0.]):
        print('2. Set Test Failed')
    else:
        print('2. Set Test Passed')

def UnitTest2SetScores():
    # Set up a "Set Network":
    [nodes, dist, parents, outcomes, info] = TennisSetNetwork(0.8, 0.6, 0.85, 0.15)
    SetScores = ["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]

    # Check several different scorelines get the correct set score:
    if (dist['SetScore'][1,1,1,1,1,2,2,2,2,2,2,2,2] != [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,0.]): # Set Score = 5-7
        print('2. Set Scores Test Failed')
    elif (dist['SetScore'][2,2,2,2,2,1,1,1,1,1,1,1,1] != [0.,0.,0.,0.,0.,1.,0.,0.,0.,0.,0.,0.,0.,0.]): # Set Score = 7-5
        print('2. Set Scores Test Failed')
    elif (dist['SetScore'][1,2,1,2,1,2,1,2,1,2,1,2,2] != [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.]): # Set Score = 6-7
        print('2. Set Scores Test Failed')
    elif (dist['SetScore'][2,2,1,2,1,2,1,1,1,1,1,1,1] != [0.,0.,0.,0.,1.,0.,0.,0.,0.,0.,0.,0.,0.,0.]): # Set Score = 6-4
        print('2. Set Scores Test Failed')
    elif (dist['SetScore'][1,1,2,2,2,2,1,1,2,1,1,2,1] != [0.,0.,0.,0.,0.,0.,1.,0.,0.,0.,0.,0.,0.,0.]): # Set Score = 7-6
        print('2. Set Scores Test Failed')
    else:
        print('2. Set Scores Test Passed')

def UnitTest2NumGames():
    # Set up a "Set Network":
    [nodes, dist, parents, outcomes, info] = TennisSetNetwork(0.8, 0.6, 0.85, 0.15)
    NumGames = [6, 7, 8, 9, 10, 12, 13]

    # Check several different scorelines get the correct set score:
    if (dist['NumGames'][1,1,1,1,1,2,2,2,2,2,2,2,2] != [0.,0.,0.,0.,0.,1.,0.]): # Number of games = 12
        print('2. Number of Games Test Failed')
    elif (dist['NumGames'][2,2,2,2,2,1,1,1,1,1,1,1,1] != [0.,0.,0.,0.,0.,1.,0.]): #  Number of games = 12
        print('2. Number of Games Failed')
    elif (dist['NumGames'][1,2,1,2,1,2,1,2,1,2,1,2,2] != [0.,0.,0.,0.,0.,0.,1.]): #  Number of games = 13
        print('2. Number of Games Test Failed')
    elif (dist['NumGames'][2,2,1,2,1,2,1,1,1,1,1,1,1] != [0.,0.,0.,0.,1.,0.,0.]): #  Number of games = 10
        print('2. Number of Games Test Failed')
    elif (dist['NumGames'][1,1,1,2,2,1,1,1,1,1,1,1,1] != [0.,0.,1.,0.,0.,0.,0.]): #  Number of games = 8
        print('2. Number of Games Test Failed')
    else:
        print('2. Number of Games Test Passed')    

def UnitTest4Set():
    # Set up a "Match Network" using the second approach:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.9, 0.7, 0.85, 0.15, 3, 'Complex')
    
    # Check several different scorelines get the correct set winner when 3 sets are played:
    if (dist['NumSets'][1,1,1] != [1.,0.,0.,0.]): # 2 sets
        print('4a. Number of Sets Test Failed')
    elif (dist['NumSets'][1,1,2] != [1.,0.,0.,0.]): # 2 sets
        print('4a. Number of Sets Test Failed')
    elif (dist['NumSets'][2,2,2] != [1.,0.,0.,0.]): # 2 sets
        print('4a. Number of Sets Test Failed')
    elif (dist['NumSets'][2,2,1] != [1.,0.,0.,0.]): # 2 sets
        print('4a. Number of Sets Test Failed')
    elif (dist['NumSets'][2,1,2] != [0.,1.,0.,0.]): # 3 sets
        print('4a. Number of Sets Test Failed')
    else:
        print('4a. Number of Sets Test Passed')

    # Check scoreline for 5 set matches:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.5, 0.7, 0.3, 0.7, 5, 'Complex')
    if (dist['NumSets'][1,1,1,1,1] != [0.,1.,0.,0.]): # 3 sets
        print('4b. Number of Sets Test Failed')
    elif (dist['NumSets'][2,1,1,1,1] != [0.,1.,0.,0.]): # 4 sets
        print('4b. Number of Sets Test Failed')
    elif (dist['NumSets'][1,1,2,2,1] != [0.,0.,0.,1.]): # 5 sets
        print('4b. Number of Sets Test Failed')
    elif (dist['NumSets'][2,1,2,1,2] != [0.,0.,0.,1.]): # 5 sets
        print('4b. Number of Sets Test Failed')
    elif (dist['NumSets'][2,2,1,2,1] != [0.,0.,1.,0.]): # 4 sets
        print('4b. Number of Sets Test Failed')
    else:
        print('4b. Number of Sets Test Passed')

def UnitTest4Match():
    # Set up a "Match Network" using the second approach:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.9, 0.7, 0.85, 0.15, 3, 'Complex')
    
    # Check several different scorelines get the correct set winner when 3 sets are played:
    if (dist['Match'][1,1,1] != [1.,0.]): 
        print('4a. Match Test Failed')
    elif (dist['Match'][1,1,2] != [1.,0.]):
        print('4a. Match Test Failed')
    elif (dist['Match'][2,2,2] != [0.,1.]): 
        print('4a. Match Test Failed')
    elif (dist['Match'][2,2,1] != [0.,1.]):
        print('4a. Match Test Failed')
    elif (dist['Match'][2,1,2] != [0.,1.]): 
        print('4a. Match Test Failed')
    else:
        print('4a. Match Test Passed')

    # Check scoreline for 5 set matches:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.5, 0.7, 0.3, 0.7, 5, 'Complex')
    if (dist['Match'][1,1,1,1,1] != [1.,0.]): 
        print('4b. Match Test Failed')
    elif (dist['Match'][2,1,1,1,1] != [1.,0.]): 
        print('4b. Match Test Failed')
    elif (dist['Match'][1,1,2,2,1] != [1.,0.]): 
        print('4b. Match Test Failed')
    elif (dist['Match'][2,1,2,1,2] != [0.,1.]):
        print('4b. Match Test Failed')
    elif (dist['Match'][2,2,1,2,1] != [0.,1.]):
        print('4b. Match Test Failed')
    else:
        print('4b. Match Test Passed')

def UnitTest4TotalNumGames():
    # Set up a "Match Network" using the second approach:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.9, 0.7, 0.85, 0.15, 3, 'Complex')
    
    # Check several different scorelines get the correct set winner when 3 sets are played:
    if (dist['TotalNumGames'][2,7,8,9][3] != 1. or dist['TotalNumGames'][2,7,8,9][12] != 0.): # Total games = 15 
        print('4a. Total Number of Games Test Failed')
    elif (dist['TotalNumGames'][3,7,8,9][3] != 0. or dist['TotalNumGames'][3,7,8,9][12] != 1.): # Total games = 24
        print('4a. Total Number of Games Test Failed')
    elif (dist['TotalNumGames'][2,6,13,8][7] != 1. or dist['TotalNumGames'][2,6,13,8][15] != 0.): # Total games = 19
        print('4a. Total Number of Games Test Failed')
    elif (dist['TotalNumGames'][3,6,13,8][7] != 0. or dist['TotalNumGames'][3,6,13,8][15] != 0.): # Total games = 27
        print('4a. Total Number of Games Test Failed')
    elif (dist['TotalNumGames'][3,13,13,13][27] != 1. or dist['TotalNumGames'][3,13,13,13][14] != 0.): # Total games = 39
        print('4a. Total Number of Games Test Failed')
    elif (dist['TotalNumGames'][2,6,6,6][0] != 1. or dist['TotalNumGames'][2,6,6,6][6] != 0.): # Total games = 12
        print('4a. Total Number of Games Test Failed')
    else:
        print('4a. Total Number of Games Test Passed')

    # Check scoreline for 5 set TotalNumGameses:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.5, 0.7, 0.3, 0.7, 5, 'Complex')
    if (dist['TotalNumGames'][3,7,8,9,10,11][12] != 1. or dist['TotalNumGames'][3,7,8,9,10,11][22] != 0.): # Total games = 24 
        print('4a. Total Number of Games Test Failed')
    elif (dist['TotalNumGames'][4,9,9,9,6,12][21] != 1. or dist['TotalNumGames'][4,9,9,9,6,12][33] != 0.): # Total games = 33
        print('4a. Total Number of Games Test Failed')
    elif (dist['TotalNumGames'][5,13,13,13,13,13][53] != 1.):  # Total games = 65
        print('4a. Total Number of Games Test Failed')
    elif (dist['TotalNumGames'][3,7,6,13,7,8][14] != 1.): # Total games = 26
        print('4a. Total Number of Games Test Failed')
    elif (dist['TotalNumGames'][5,6,6,6,6,6][18] != 1.): # Total games = 30
        print('4a. Total Number of Games Test Failed')
    elif (dist['TotalNumGames'][4,12,10,9,13,6][32] != 1.): # Total games = 44
        print('4a. Total Number of Games Test Failed')
    else:
        print('4a. Total Number of Games Test Passed')

if __name__ == "__main__":
    TestSuite()
    