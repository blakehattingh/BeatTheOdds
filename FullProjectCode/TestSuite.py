import numpy as np
from RunningTheMarkovModel import RunMarkovModel
from MarkovModelNetwork import TennisSetNetworkEfficient
from BeliefPropogationAlgorithm import beliefpropagation
from OtherMarkovModelNetworks import TennisMatchNetwork1, TennisMatchNetwork2

# This script is a test suite for all the unit tests for functions contributing to our Markov Model.

# Functions to test:
# 1) TennisSetNetwork
# 2) TennisMatchNetwork1 
# 3) TennisMatchNetwork2

# Testing TennisSetNetwork:
# 1Set) Tests if the 'Set' node has the correct distributions for a given sequence of game outcomes.
# 1SetScore) Tests if the 'SetScore' node has the correct distributions for a given sequence of game outcomes.
# 1NumGames) Tests if the 'NumGames' node has the correct distributions for a given sequence of game outcomes.
# 1SetUp) Tests the general set up of the network.
# 1Network) Checks the network gives qualitatively correct distributions for specific p values.
# 1SetScoreAdv) Allows the user to input their own sequence of games and expected set score distribution to test.
# 1SetEvents) Tests if the network responds qualitatively accurately when events are set fixed.
            
# Testing TennisMatchNetwork1:
# a. and and b. for 3 and 5 sets respectively.
# 2SetUp) Tests the general Network set up.
# 2Match) Tests if the 'Match' node has the correct distributions for a given sequence of set outcomes.
# 2MatchScore) Tests if the 'MatchScore' node has the correct distributions for a given sequence of set outcomes.
# 2TotalNumGames) Tests if the 'TotalNumGames' node has the correct distributions for a given sequence of NumSets and Number of games.
# 2AllSetScores) Tests if the 'AllSetScores' node has the correct distributions for a given sequence of set scores.

# Testing TennisMatchNetwork2:
# a. and and b. for 3 and 5 sets respectively.
# 3Network) Tests the general network set up.
# 3Sets) Tests the 'Set' nodes have the correct distributions for a given sequence of game outcomes.
# 3Match) Tests if the 'Match' node has the correct distributions for a given sequence of set outcomes.
# 3NumSets) Tests if the 'NumSets' node has the correct distributions for a given sequence of set outcomes.
# 3TotalNumGames) Tests if the 'TotalNumGames' node has the correct distributions for a given sequence of NumSets and Number of games.
# 3AllSetScores) Tests if the 'AllSetScores' node has the correct distributions for a given sequence of set scores.

def TestSuite():
    Test1 = False
    Test2 = False
    Test3 = True

    if Test1:
        # UnitTest1Set() - Not relevant anymore with efficiencies added
        # UnitTest1NumGames() - Not relevant with efficiencies added
        UnitTest1SetScores()
        UnitTest1SetUp()
        UnitTest1Network()
        UnitTest1SetScoreAdv()
        UnitTest1SetEvents()
    if Test2:
        UnitTest2Network()
        UnitTest2Match()
        UnitTest2NumSets()
        UnitTest2TotalNumGames()
        UnitTest2AllSetScores()
    if Test3:
        UnitTest3Network()
        UnitTest3Sets()
        UnitTest3Match()
        UnitTest3MatchScore()
        UnitTest3TotalNumGames()

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
    else:
        print('Test 1b Failed')

def UnitTest1Set():
    # Set up a "Set Network":
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(0.8, 0.6, InitServerDist = [0.85, 0.15])
    
    # Check several different scorelines get the correct set winner:
    if (dist['Set'][1,1,1,1,1,2,2,2,2,2,2,2,2] != [0., 1.]):
        print('2. et Test Failed a')
    elif (dist['Set'][2,2,2,2,2,1,1,1,1,1,1,1,1] != [1., 0.]):
        print('2. Set Test Failed b')
    elif (dist['Set'][1,2,1,2,1,2,1,2,1,2,1,2,2] != [0., 1.]):
        print('2. Set Test Failed c')
    elif (dist['Set'][2,2,1,2,1,2,1,1,1,1,1,1,1] != [1., 0.]):
        print('2. Set Test Failed d')
    elif (dist['Set'][1,1,2,2,2,2,1,1,2,1,1,2,1] != [1., 0.]):
        print('2. Set Test Failed e')
    elif (dist['Set'][1,2,2,2,1,1,1,1,1,2,2,2,2] != [1., 0.]):
        print('2. Set Test Failed f')
    else:
        print('2. Set Test Passed')

def UnitTest1SetScores():
    # Set up a "Set Network":
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(0.8, 0.6)
    SetScores = ["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]

    # Check several different scorelines get the correct set score:
    if (dist['SetScore'][1,1,1,1,1,2,2,2,2,2,2,2,2] != [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,0.]): # Set Score = 5-7
        print('1. Set Scores Test Failed')
    elif (dist['SetScore'][2,2,2,2,2,1,1,1,1,1,1,1,1] != [0.,0.,0.,0.,0.,1.,0.,0.,0.,0.,0.,0.,0.,0.]): # Set Score = 7-5
        print('1. Set Scores Test Failed')
    elif (dist['SetScore'][1,2,1,2,1,2,1,2,1,2,1,2,2] != [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.]): # Set Score = 6-7
        print('1. Set Scores Test Failed')
    elif (dist['SetScore'][2,2,1,2,1,2,1,1,1,1,1,1,1] != [0.,0.,0.,0.,1.,0.,0.,0.,0.,0.,0.,0.,0.,0.]): # Set Score = 6-4
        print('1. Set Scores Test Failed')
    elif (dist['SetScore'][1,1,2,2,2,2,1,1,2,1,1,2,1] != [0.,0.,0.,0.,0.,0.,1.,0.,0.,0.,0.,0.,0.,0.]): # Set Score = 7-6
        print('1. Set Scores Test Failed')
    else:
        print('1. Set Scores Test Passed')

def UnitTest1NumGames():
    # Set up a "Set Network":
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(0.8, 0.6)
    NumGames = [6, 7, 8, 9, 10, 12, 13]

    # Check several different scorelines get the correct set score:
    if (dist['NumGames'][1,1,1,1,1,2,2,2,2,2,2,2,2] != [0.,0.,0.,0.,0.,1.,0.]): # Number of games = 12
        print('1. Number of Games Test Failed')
    elif (dist['NumGames'][2,2,2,2,2,1,1,1,1,1,1,1,1] != [0.,0.,0.,0.,0.,1.,0.]): #  Number of games = 12
        print('1. Number of Games Failed')
    elif (dist['NumGames'][1,2,1,2,1,2,1,2,1,2,1,2,2] != [0.,0.,0.,0.,0.,0.,1.]): #  Number of games = 13
        print('1. Number of Games Test Failed')
    elif (dist['NumGames'][2,2,1,2,1,2,1,1,1,1,1,1,1] != [0.,0.,0.,0.,1.,0.,0.]): #  Number of games = 10
        print('1. Number of Games Test Failed')
    elif (dist['NumGames'][1,1,1,2,2,1,1,1,1,1,1,1,1] != [0.,0.,1.,0.,0.,0.,0.]): #  Number of games = 8
        print('1. Number of Games Test Failed')
    else:
        print('1. Number of Games Test Passed')    

def UnitTest1SetUp():
    # Set up a "Set Network":
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(0.8, 0.6)

    # Check parents of game nodes:
    if (parents['G4'] != ['ServerEven']):
        print('1. Parents of Game Nodes Failed a')
    elif (parents['TB'] != ['ServerOdd']):
        print('1. Parents of Game Nodes Failed b')
    elif (len(parents['SetScore']) != 13):
        print('1. Parents of Game Nodes Failed c')
    else:
        print('1. Parents of Game Nodes Passed')

def UnitTest1Network():
    # Check the network gives suitable winners based off the p values inputted:

    # Scenario 1: Player 1 > Player 2
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(0.8, 0.6)
    [SetScoreDist] = beliefpropagation(nodes,dist,parents,outcomes,info,100,0.001,['SetScore'])
    if (sum(SetScoreDist[0:7]) <= sum(SetScoreDist[7:14])):
        print('1. Output Distributions Test Failed a')
    elif (SetScoreDist[6] > SetScoreDist[5]):
        print('1. Output Distributions Test Failed b')
    else:
        print('1. Output Distributions Test Scenario 1 Passed')
    
    # Scenario 2: Player 1 = Player 2
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(0.65, 0.65)
    [SetScoreDist] = beliefpropagation(nodes,dist,parents,outcomes,info,100,0.0001,['SetScore'])
    if (abs(sum(SetScoreDist[0:7]) - sum(SetScoreDist[7:14])) > 0.001):
        print('1. Output Distributions Test Failed a')
    elif (SetScoreDist[1] > SetScoreDist[6]):
        print('1. Output Distributions Test Failed b')
    elif (abs(SetScoreDist[2] - SetScoreDist[9]) > 0.001):
        print('1. Output Distributions Test Failed c')
    else:
        print('1. Output Distributions Test Scenario 2 Passed')

def UnitTest1SetScoreAdv():
    Game = 0
    Wins1 = 0
    Wins2 = 0
    Sequence = [1,1,1,1,1,1,1,1,1,1,1,1,1]
    GameOver = [[6,0],[6,1],[6,2],[6,3],[6,4],[7,5],[7,6],[0,6],[1,6],[2,6],[3,6],[4,6],[5,7],[6,7]]
    Distribution = np.zeros(14, dtype = float)
    while ([Wins1,Wins2] not in GameOver):
        Game += 1
        GameWinner = int(input('Please enter the winner of game {}: '.format(Game)))
        if (GameWinner == 1):
            Wins1 += 1
        elif (GameWinner == 2):
            Wins2 += 1
        else:
            while (GameWinner == 1 or GameWinner == 2):
                GameWinner = int(input('Enter 1 or 2 you idiot: '))
        Sequence[Game-1] = GameWinner
        print('Current Score is: {}-{}'.format(Wins1, Wins2))
    print('Checking network assigns the correct Set Score')

    # Update Set Score distribution:
    Distribution[GameOver.index([Wins1,Wins2])] = 1.

    # Set up a "Set Network":
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(0.7, 0.7)

    Sequence = tuple(Sequence)
    if ((dist['SetScore'][Sequence] == Distribution).all()):
        print('1. Set Score Advanced Test Passed')
    else:
        print('1. Set Score Advanced Test Failed')
        print(dist['SetScore'][Sequence])

def UnitTest1SetEvents():
    # Need to modify the network to allow events to be fixed
    x = 69

def UnitTest2Network():
    SetDists = [np.array([0.51471958, 0.48528042]), np.array([0.51495612, 0.48504388]), np.array([0.51473445, 0.48526555]),
    np.array([0.54, 0.46]), np.array([0.58, 0.42])]
    SetScoreDists = [np.array([0.01576853, 0.04723345, 0.08253247, 0.10987546, 0.12342136,
        0.06171053, 0.06842541, 0.01548256, 0.04651851, 0.08153156,
        0.10887454, 0.12267068, 0.0613352 , 0.05461975]), np.array([0.01500446, 0.05239947, 0.07579284, 0.12454442, 0.10996195,
        0.0612606 , 0.0702565 , 0.01472783, 0.03985681, 0.08661524,
        0.09532216, 0.1373999 , 0.06088177, 0.05597605]), np.array([0.01575673, 0.04796772, 0.08177476, 0.11161937, 0.12169578,
        0.06170372, 0.06845911, 0.0154709 , 0.04576982, 0.08225674,
        0.10715684, 0.12440623, 0.06132832, 0.05463398]), np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.]),
        np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.])]
    NumGamesDists = [np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516]), np.array([0.02973229, 0.09225628, 0.16240807, 0.21986659, 0.24736185,
        0.12214237, 0.12623255]), np.array([0.03122763, 0.09373754, 0.1640315 , 0.21877621, 0.24610201,
        0.12303204, 0.12309308]), np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516]), np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516])]

    # Set up a "Match Network" using first approach:
    [nodes3, dist3, parents3, outcomes3, info3] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 3)
    [nodes5, dist5, parents5, outcomes5, info5] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 5)

    # Check number of nodes and parent nodes: (3 sets)
    if (len(nodes3) != 3 * 3 + 4):
        print('3a. Network Test Failed')
    elif (len(parents3['Match']) != 3):
        print('3a. Network Test Failed')    
    elif (len(parents3['TotalNumGames']) != 3 + 1):
        print('3a. Network Test Failed')
    else:
        print('3a. Network Test Passed')

    # 5 sets:
    if (len(nodes5) != 5 * 3 + 4):
        print('3b. Network Test Failed')
    elif (len(parents5['Match']) != 5):
        print('3b. Network Test Failed')    
    elif (len(parents5['TotalNumGames']) != 5 + 1):
        print('3b. Network Test Failed')
    else:
        print('3b. Network Test Passed')

def UnitTest2Match():
    SetDists = [np.array([0.51471958, 0.48528042]), np.array([0.51495612, 0.48504388]), np.array([0.51473445, 0.48526555]),
    np.array([0.54, 0.46]), np.array([0.58, 0.42])]
    SetScoreDists = [np.array([0.01576853, 0.04723345, 0.08253247, 0.10987546, 0.12342136,
        0.06171053, 0.06842541, 0.01548256, 0.04651851, 0.08153156,
        0.10887454, 0.12267068, 0.0613352 , 0.05461975]), np.array([0.01500446, 0.05239947, 0.07579284, 0.12454442, 0.10996195,
        0.0612606 , 0.0702565 , 0.01472783, 0.03985681, 0.08661524,
        0.09532216, 0.1373999 , 0.06088177, 0.05597605]), np.array([0.01575673, 0.04796772, 0.08177476, 0.11161937, 0.12169578,
        0.06170372, 0.06845911, 0.0154709 , 0.04576982, 0.08225674,
        0.10715684, 0.12440623, 0.06132832, 0.05463398]), np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.]),
        np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.])]
    NumGamesDists = [np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516]), np.array([0.02973229, 0.09225628, 0.16240807, 0.21986659, 0.24736185,
        0.12214237, 0.12623255]), np.array([0.03122763, 0.09373754, 0.1640315 , 0.21877621, 0.24610201,
        0.12303204, 0.12309308]), np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516]), np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516])]

    # Set up a 'Match Network' using approach 1:
    [nodes3, dist3, parents3, outcomes3, info3] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 3)
    [nodes5, dist5, parents5, outcomes5, info5] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 5)

    # Test the Match outcome distribution (3 sets):
    if (dist3['Match'][2, 2, 2] != [0., 1.]):
        print('3a. Match Test Failed')
    elif (dist3['Match'][1, 1, 2] != [1., 0.]):
        print('3a. Match Test Failed')
    elif(dist3['Match'][1, 2, 1] != [1., 0.]):
        print('3a. Match Test Failed')
    else:
        print('3a. Match Test Passed')

    # Test the Match outcome distribution (5 sets):
    if (dist5['Match'][2, 2, 2, 2, 2] != [0., 1.]):
        print('3b. Match Test Failed')
    elif (dist5['Match'][1, 1, 2, 2, 2] != [0., 1.]):
        print('3b. Match Test Failed')
    elif(dist5['Match'][1, 2, 1, 2, 1] != [1., 0.]):
        print('3b. Match Test Failed')
    else:
        print('3b. Match Test Passed')

def UnitTest2MatchScore():
    SetScoreDists = [np.array([0.01576853, 0.04723345, 0.08253247, 0.10987546, 0.12342136,
        0.06171053, 0.06842541, 0.01548256, 0.04651851, 0.08153156,
        0.10887454, 0.12267068, 0.0613352 , 0.05461975]), np.array([0.01500446, 0.05239947, 0.07579284, 0.12454442, 0.10996195,
        0.0612606 , 0.0702565 , 0.01472783, 0.03985681, 0.08661524,
        0.09532216, 0.1373999 , 0.06088177, 0.05597605]), np.array([0.01575673, 0.04796772, 0.08177476, 0.11161937, 0.12169578,
        0.06170372, 0.06845911, 0.0154709 , 0.04576982, 0.08225674,
        0.10715684, 0.12440623, 0.06132832, 0.05463398]), np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.]),
        np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.])]

    # Set up a 'Match Network' using approach 1:
    [nodes5, dist5, parents5, outcomes5, info5] = TennisMatchNetwork1(SetScoreDists, 5)
    [nodes3, dist3, parents3, outcomes3, info3] = TennisMatchNetwork1(SetScoreDists, 3)

    # Test the Match Score distribution: (3 sets)
    if (dist3['MatchScore'][2, 2, 2] != [0., 0., 1., 0.]):
        print('3a. Match Score Test Failed')
    elif (dist3['MatchScore'][1, 1, 2] != [1., 0., 0., 0.]):
        print('3a. Match Score Test Failed')
    elif(dist3['MatchScore'][1, 2, 1] != [0., 1., 0., 0.]):
        print('3a. Match Score Test Failed')
    elif(dist3['MatchScore'][2, 1, 2] != [0., 0., 0., 1.]):
        print('3a. Match Score Test Failed')
    else:
        print('3a. Match Score Test Passed')

    # Test the Match Score distribution: (5 sets)
    if (dist5['MatchScore'][2, 2, 2, 2, 2] != [0., 0., 0., 1., 0., 0.]):
        print(dist5['MatchScore'][2,2,2,2,2])
    elif (dist5['MatchScore'][1, 1, 2, 2, 2] != [0., 0., 0., 0., 0., 1.]):
        print('3b. Match Score Test Failed')
    elif(dist5['MatchScore'][1, 2, 1, 2, 1] != [0., 0., 1., 0., 0., 0.]):
        print('3b. Match Score Test Failed')
    elif(dist5['MatchScore'][2, 2, 1, 2, 1] != [0., 0., 0., 0., 1., 0.]):
        print('3b. Match Score Test Failed')
    elif(dist5['MatchScore'][1, 1, 1, 2, 2] != [1., 0., 0., 0., 0., 0.]):
        print('3b. Match Score Test Failed')
    elif(dist5['MatchScore'][2, 1, 1, 1, 2] != [0., 1., 0., 0., 0., 0.]):
        print('3b. Match Score Test Failed')
    else:
        print('3b. Match Score Test Passed')

def UnitTest2NumSets():
    SetDists = [np.array([0.51471958, 0.48528042]), np.array([0.51495612, 0.48504388]), np.array([0.51473445, 0.48526555]),
    np.array([0.54, 0.46]), np.array([0.58, 0.42])]
    SetScoreDists = [np.array([0.01576853, 0.04723345, 0.08253247, 0.10987546, 0.12342136,
        0.06171053, 0.06842541, 0.01548256, 0.04651851, 0.08153156,
        0.10887454, 0.12267068, 0.0613352 , 0.05461975]), np.array([0.01500446, 0.05239947, 0.07579284, 0.12454442, 0.10996195,
        0.0612606 , 0.0702565 , 0.01472783, 0.03985681, 0.08661524,
        0.09532216, 0.1373999 , 0.06088177, 0.05597605]), np.array([0.01575673, 0.04796772, 0.08177476, 0.11161937, 0.12169578,
        0.06170372, 0.06845911, 0.0154709 , 0.04576982, 0.08225674,
        0.10715684, 0.12440623, 0.06132832, 0.05463398]), np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.]),
        np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.])]
    NumGamesDists = [np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516]), np.array([0.02973229, 0.09225628, 0.16240807, 0.21986659, 0.24736185,
        0.12214237, 0.12623255]), np.array([0.03122763, 0.09373754, 0.1640315 , 0.21877621, 0.24610201,
        0.12303204, 0.12309308]), np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516]), np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516])]

    # Set up a 'Match Network' using approach 1:
    [nodes5, dist5, parents5, outcomes5, info5] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 5)
    [nodes3, dist3, parents3, outcomes3, info3] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 3)

    # Test the Number of Sets distribution: (3 sets)
    if (dist3['NumSets'][2, 2, 2] != [1., 0.]):
        print('3a. Number of Sets Test Failed')
    elif (dist3['NumSets'][1, 1, 2] != [1., 0.]):
        print('3a. Number of Sets Test Failed')
    elif(dist3['NumSets'][1, 2, 1] != [0., 1.]):
        print('3a. Number of Sets Test Failed')
    elif(dist3['NumSets'][2, 1, 2] != [0., 1.]):
        print('3a. Number of Sets Test Failed')
    else:
        print('3a. Number of Sets Test Passed')

    # Test the Number of Sets distribution: (5 sets)
    if (dist5['NumSets'][2, 2, 2, 2, 2] != [1., 0., 0.]):
        print(dist5['NumSets'][2,2,2,2,2])
    elif (dist5['NumSets'][1, 1, 2, 2, 2] != [0., 0., 1.]):
        print('3b. Number of Sets Test Failed')
    elif(dist5['NumSets'][1, 2, 1, 2, 1] != [0., 0., 1.]):
        print('3b. Number of Sets Test Failed')
    elif(dist5['NumSets'][2, 2, 1, 2, 1] != [0., 1., 0.]):
        print('3b. Number of Sets Test Failed')
    elif(dist5['NumSets'][1, 1, 1, 2, 2] != [1., 0., 0.]):
        print('3b. Number of Sets Test Failed')
    elif(dist5['NumSets'][2, 1, 1, 1, 2] != [0., 1., 0.]):
        print('3b. Number of Sets Test Failed')
    else:
        print('3b. Number of Sets Test Passed')

def UnitTest2TotalNumGames():
    SetDists = [np.array([0.51471958, 0.48528042]), np.array([0.51495612, 0.48504388]), np.array([0.51473445, 0.48526555]),
    np.array([0.54, 0.46]), np.array([0.58, 0.42])]
    SetScoreDists = [np.array([0.01576853, 0.04723345, 0.08253247, 0.10987546, 0.12342136,
        0.06171053, 0.06842541, 0.01548256, 0.04651851, 0.08153156,
        0.10887454, 0.12267068, 0.0613352 , 0.05461975]), np.array([0.01500446, 0.05239947, 0.07579284, 0.12454442, 0.10996195,
        0.0612606 , 0.0702565 , 0.01472783, 0.03985681, 0.08661524,
        0.09532216, 0.1373999 , 0.06088177, 0.05597605]), np.array([0.01575673, 0.04796772, 0.08177476, 0.11161937, 0.12169578,
        0.06170372, 0.06845911, 0.0154709 , 0.04576982, 0.08225674,
        0.10715684, 0.12440623, 0.06132832, 0.05463398]), np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.]),
        np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.])]
    NumGamesDists = [np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516]), np.array([0.02973229, 0.09225628, 0.16240807, 0.21986659, 0.24736185,
        0.12214237, 0.12623255]), np.array([0.03122763, 0.09373754, 0.1640315 , 0.21877621, 0.24610201,
        0.12303204, 0.12309308]), np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516]), np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516])]

    # Set up a 'Match Network' using approach 1:
    [nodes5, dist5, parents5, outcomes5, info5] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 5)
    [nodes3, dist3, parents3, outcomes3, info3] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 3)

    # Scenarios:
    Distribution3Sets = np.zeros(28, dtype = float)
    Distribution5Sets = np.zeros(48, dtype = float)

    # 1: 2 sets, 6-0, 6-0, ~ = 12 games
    Distribution1 = Distribution3Sets
    Distribution1[0] = 1.

    # 2: 2 sets, 6-4, 7-5, ~ = 22 games
    Distribution2 = Distribution3Sets
    Distribution2[10] = 1.

    # 3: 2 sets, 2-6, 6-7, ~ = 21 games
    Distribution3 = Distribution3Sets
    Distribution3[9] = 1.

    # 4: 2 sets, 6-7, 6-7, ~ = 26 games
    Distribution4 = Distribution3Sets
    Distribution4[14] = 1.

    # 5: 3 sets, 6-3, 4-6, 7-6 = 32 games
    Distribution5 = Distribution3Sets
    Distribution5[20] = 1.

    # 6: 3 sets, 6-4, 5-7, 2-6 = 30 games
    Distribution6 = Distribution3Sets
    Distribution6[18] = 1.

    # 7: 3 sets, 7-6, 6-7, 7-6 = 39 games
    Distribution7 = Distribution3Sets
    Distribution7[27] = 1.

    # 8: 3 sets, 6-0, 6-0, 6-4, ~, ~ = 22 games
    Distribution8 = Distribution5Sets
    Distribution8[4] = 1.

    # 9: 3 sets, 4-6, 5-7, 6-7, ~, ~ = 35 games
    Distribution9 = Distribution5Sets
    Distribution9[17] = 1.

    # 10: 4 sets, 2-6, 6-7, 6-4, 5-7, ~ = 43 games
    Distribution10 = Distribution5Sets
    Distribution10[25] = 1.

    # 11: 4 sets, 6-7, 7-6, 6-3, 7-5, ~ = 47 games
    Distribution11 = Distribution5Sets
    Distribution11[29] = 1.

    # 12: 5 sets, 6-3, 4-6, 7-6, 5-7, 6-4 = 54 games
    Distribution12 = Distribution5Sets
    Distribution12[36] = 1.

    # 13: 5 sets, 6-4, 5-7, 3-6, 7-6, 7-6 = 57 games
    Distribution13 = Distribution5Sets
    Distribution13[18] = 1.

    # 14: 5 sets, 7-6, 6-7, 7-6, 6-7, 6-7 = 65 games
    Distribution14 = Distribution5Sets
    Distribution14[47] = 1.

    # Test the Total number of games distribution: (3 sets)
    if (np.allclose(dist3['TotalNumGames'][2, 6, 6, 6], Distribution1)):
        print('3a. Total Number of Games Test Failed')
    elif (np.allclose(dist3['TotalNumGames'][2, 10, 12, 8], Distribution2)):
        print('3a. Total Number of Games Test Failed')
    elif(np.allclose(dist3['TotalNumGames'][2, 8, 13, 9], Distribution3)):
        print('3a. Total Number of Games Test Failed')
    elif(np.allclose(dist3['TotalNumGames'][2, 13, 13, 6], Distribution4)):
        print('3a. Total Number of Games Test Failed')
    elif(np.allclose(dist3['TotalNumGames'][3, 9, 10, 13], Distribution5)):
        print('3a. Total Number of Games Test Failed')
    elif(np.allclose(dist3['TotalNumGames'][3, 10, 12, 8], Distribution6)):
        print('3a. Total Number of Games Test Failed')
    elif(np.allclose(dist3['TotalNumGames'][3, 13, 13, 13], Distribution7)):
        print('3a. Total Number of Games Test Failed')
    else:
        print('3a. Total Number of Games Test Passed')

    # Test the Number of Sets distribution: (5 sets)
    if (np.allclose(dist5['TotalNumGames'][3, 6, 6, 10, 8, 9], Distribution8)):
        print('3b. Total Number of Games Test Failed')
    elif (np.allclose(dist5['TotalNumGames'][3, 10, 12, 13, 6, 12], Distribution9)):
        print('3b. Total Number of Games Test Failed')
    elif (np.allclose(dist5['TotalNumGames'][4, 8, 13, 10, 12, 9], Distribution10)):
        print('3b. Total Number of Games Test Failed')
    elif (np.allclose(dist5['TotalNumGames'][4, 13, 13, 9, 12, 9], Distribution11)):
        print('3b. Total Number of Games Test Failed')
    elif (np.allclose(dist5['TotalNumGames'][5, 9, 10, 13, 12, 10], Distribution12)):
        print('3b. Total Number of Games Test Failed')
    elif (np.allclose(dist5['TotalNumGames'][5, 10, 12, 9, 13, 13], Distribution13)):
        print('3b. Total Number of Games Test Failed')
    elif (np.allclose(dist5['TotalNumGames'][5, 13, 13, 13, 13, 13], Distribution13)):
        print('3b. Total Number of Games Test Failed')
    else:
        print('3b. Total Number of Games Test Passed')

def UnitTest2AllSetScores():
    SetDists = [np.array([0.51471958, 0.48528042]), np.array([0.51495612, 0.48504388]), np.array([0.51473445, 0.48526555]),
    np.array([0.54, 0.46]), np.array([0.58, 0.42])]
    SetScoreDists = [np.array([0.01576853, 0.04723345, 0.08253247, 0.10987546, 0.12342136,
        0.06171053, 0.06842541, 0.01548256, 0.04651851, 0.08153156,
        0.10887454, 0.12267068, 0.0613352 , 0.05461975]), np.array([0.01500446, 0.05239947, 0.07579284, 0.12454442, 0.10996195,
        0.0612606 , 0.0702565 , 0.01472783, 0.03985681, 0.08661524,
        0.09532216, 0.1373999 , 0.06088177, 0.05597605]), np.array([0.01575673, 0.04796772, 0.08177476, 0.11161937, 0.12169578,
        0.06170372, 0.06845911, 0.0154709 , 0.04576982, 0.08225674,
        0.10715684, 0.12440623, 0.06132832, 0.05463398]), np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.]),
        np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0., 0., 0.1, 0.1, 0., 0.])]
    NumGamesDists = [np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516]), np.array([0.02973229, 0.09225628, 0.16240807, 0.21986659, 0.24736185,
        0.12214237, 0.12623255]), np.array([0.03122763, 0.09373754, 0.1640315 , 0.21877621, 0.24610201,
        0.12303204, 0.12309308]), np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516]), np.array([0.03125109, 0.09375196, 0.16406403, 0.21875   , 0.24609203,
        0.12304573, 0.12304516])]

    # Set up a 'Match Network' using approach 1:
    [nodes5, dist5, parents5, outcomes5, info5] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 5)
    [nodes3, dist3, parents3, outcomes3, info3] = TennisMatchNetwork1(SetDists, SetScoreDists, NumGamesDists, 3)

    # Scenarios:
    Distribution = np.zeros(14, dtype = float)

    # 1: 2 sets, 6-0, 6-0, ~ = 6-0 = probability of 1
    Distribution1 = Distribution
    Distribution1[0] = 1.

    # 2: 2 sets, 6-4, 7-5, ~ = 6-4 and 7-5 have probability of 0.5
    Distribution2 = Distribution
    Distribution2[3] = 0.5
    Distribution2[4] = 0.5

    # 3: 2 sets, 2-6, 6-7, ~ = 2-6 and 6-7 have probability of 0.5
    Distribution3 = Distribution
    Distribution3[9] = 0.5
    Distribution3[13] = 0.5

    # 4: 3 sets, 6-7, 6-0, 6-7 = 6-7 has probability of 2/3 and 6-0 has P of 1/3
    Distribution4 = Distribution
    Distribution4[13] = 2./3.
    Distribution4[0] = 1./3.

    # 5: 3 sets, 6-3, 4-6, 7-6 = all have P of 1/3
    Distribution5 = Distribution
    Distribution5[6] = 1./3.
    Distribution5[3] = 1./3.
    Distribution5[11] = 1./3.

    # 6: 3 sets, 6-4, 6-4, 6-4, ~, ~ = 6-4 has P of 1
    Distribution6 = Distribution
    Distribution6[4] = 1.

    # 7: 3 sets, 6-2, 6-3, 6-4, ~, ~ = all have P of 1/3
    Distribution7 = Distribution
    Distribution7[2] = 1./3.
    Distribution7[3] = 1./3.
    Distribution7[4] = 1./3.

    # 8: 4 sets, 7-6, 6-7, 6-4, 7-5, ~ = all have P of 1/4
    Distribution8 = Distribution
    Distribution8[6] = 1./4.
    Distribution8[13] = 1./4.
    Distribution8[4] = 1./4.
    Distribution8[5] = 1./4.

    # 9: 4 sets, 6-0, 6-0, 3-6, 6-1, ~ = 6-0 has P of 0.5, others have P of 1/4
    Distribution9 = Distribution
    Distribution9[0] = 1./2.
    Distribution9[1] = 1./4.
    Distribution9[10] = 1./4.

    # 10: 4 sets, 4-6, 4-6, 7-6, 4-6, ~ = 4-6 has P of 3/4 and 7-6 has P of 1/4
    Distribution10 = Distribution
    Distribution10[11] = 3./4.
    Distribution10[6] = 1./4.

    # 11: 5 sets, 2-6, 6-7, 6-4, 5-7, 6-3 = all have P of 1/5
    Distribution11 = Distribution
    Distribution11[9] = 1./5.
    Distribution11[13] = 1./5.
    Distribution11[4] = 1./5.
    Distribution11[12] = 1./5.
    Distribution11[3] = 1./5.

    # 12: 5 sets, 7-6, 0-6, 7-6, 0-6, 7-6 = 7-6 has P of 3/5 and 0-6 has P of 2/5
    Distribution12 = Distribution
    Distribution12[6] = 3./5.
    Distribution12[7] = 2./5.

    # Test the All Set Scores distribution: (3 sets)
    if (np.allclose(dist3['AllSetScores'][2, 1, 1, 8], Distribution1)):
        print('3a. All Set Scores Test Failed')
    elif (np.allclose(dist3['AllSetScores'][2, 5, 6, 11], Distribution2)):
        print('3a. All Set Scores Test Failed')
    elif(np.allclose(dist3['AllSetScores'][2, 10, 14, 2], Distribution3)):
        print('3a. All Set Scores Test Failed')
    elif(np.allclose(dist3['AllSetScores'][3, 14, 1, 14], Distribution4)):
        print('3a. All Set Scores Test Failed')
    elif(np.allclose(dist3['AllSetScores'][3, 4, 12, 7], Distribution5)):
        print('3a. All Set Scores Test Failed')
    else:
        print('3a. All Set Scores Test Passed')

    # Test the Number of Sets distribution: (5 sets)
    if (np.allclose(dist5['AllSetScores'][3, 5, 5, 5, 8, 9], Distribution6)):
        print('3b. All Set Scores Test Failed')
    elif (np.allclose(dist5['AllSetScores'][3, 3, 4, 5, 11, 12], Distribution7)):
        print('3b. All Set Scores Test Failed')
    elif (np.allclose(dist5['AllSetScores'][4, 7, 14, 5, 4, 9], Distribution8)):
        print('3b. All Set Scores Test Failed')
    elif (np.allclose(dist5['AllSetScores'][4, 1, 1, 11, 2, 7], Distribution9)):
        print('3b. All Set Scores Test Failed')
    elif (np.allclose(dist5['AllSetScores'][4, 12, 12, 7, 12, 5], Distribution10)):
        print('3b. All Set Scores Test Failed')
    elif (np.allclose(dist5['AllSetScores'][5, 10, 14, 5, 13, 4], Distribution11)):
        print('3b. All Set Scores Test Failed')
    elif (np.allclose(dist5['AllSetScores'][5, 7, 8, 7, 8, 7], Distribution12)):
        print('3b. All Set Scores Test Failed')
    else:
        print('3b. All Set Scores Test Passed')

def UnitTest3Network():
    # Set up a "Match Network" using the second approach:
    [nodes3, dist3, parents3, outcomes3, info3] = TennisMatchNetwork2(0.9, 0.7, 3)
    [nodes5, dist5, parents5, outcomes5, info5] = TennisMatchNetwork2(0.9, 0.7, 5)
    
    # Check number of nodes and parent nodes: (3 sets)
    if (len(nodes3) != 18 * 3 + 4):
        print('4a. Network Test Failed a')
    elif (len(parents3['ServerOdd2']) != 2):
        print('4a. Network Test Failed b')
    elif (dist3['ServerOdd2']['P2Serves',6] != [0., 1.]):
        print('4a. Network Test Failed c')    
    else:
        print('4a. Network Test Passed')

    # 5 sets:
    if (len(nodes5) != 18 * 5 + 4):
        print('4b. Network Test Failed a')
    elif (len(parents5['ServerOdd4']) != 2):
        print('4b. Network Test Failed b')
    elif (dist5['ServerOdd2']['P2Serves',7] != [1., 0.]):
        print('4a. Network Test Failed c')      
    else:
        print('4b. Network Test Passed')

def UnitTest3Sets():
    # Set up a "Match Network" using the second approach:
    [nodes3, dist3, parents3, outcomes3, info3] = TennisMatchNetwork2(0.9, 0.7, 3)
    [nodes5, dist5, parents5, outcomes5, info5] = TennisMatchNetwork2(0.9, 0.7, 5)

    # Check different game outcomes to see if the correct winner is assigned:
    if (dist3['Set1'][1,1,1,1,1,2,2,2,2,2,2,2,1] != [0., 1.]):
        print('4a. Sets Test Failed a')
    elif (dist3['Set1'][1,2,2,2,1,1,1,1,1,2,2,2,2] != [1., 0.]):
        print('4a. Sets Test Failed b')
        print(dist3['Set1'][1,2,2,2,1,1,1,1,1,2,2,2,2])
    elif (dist3['Set2'][1,2,1,2,1,2,1,2,1,2,1,2,2] != [0., 1.]):
        print('4a. Sets Test Failed c')
    elif (dist3['Set2'][1,1,1,1,1,1,2,2,2,2,2,2,2] != [1., 0.]):
        print('4a. Sets Test Failed d')
    elif (dist3['Set3'][1,2,2,1,1,2,1,1,1,2,2,2,2] != [1., 0.]):
        print('4a. Sets Test Failed e')
    else:
        print('4a. Sets Test Passed')
    
    # Check different game outcomes to see if the correct winner is assigned:
    if (dist5['Set1'][1,1,1,1,1,2,2,2,2,2,2,2,1] != [0., 1.]):
        print('4b. Sets Test Failed a')
    elif (dist5['Set1'][1,2,2,2,1,1,1,1,1,2,2,2,2] != [1., 0.]):
        print('4b. Sets Test Failed b')
    elif (dist5['Set2'][1,2,1,2,1,2,1,2,1,2,1,2,2] != [0., 1.]):
        print('4b. Sets Test Failed c')
    elif (dist5['Set2'][1,1,1,1,1,1,2,2,2,2,2,2,2] != [1., 0.]):
        print('4b. Sets Test Failed d')
    elif (dist5['Set3'][1,2,2,1,1,2,1,1,1,2,2,2,2] != [1., 0.]):
        print('4b. Sets Test Failed e')
    else:
        print('4b. Sets Test Passed')

def UnitTest3Match():
    # Set up a "Match Network" using the second approach:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.9, 0.7, 3)
    
    # Check several different scorelines get the correct set winner when 3 sets are played:
    if (dist['Match'][1,1,1] != [1.,0.]): 
        print('4a. Match Test Failed a')
    elif (dist['Match'][1,1,2] != [1.,0.]):
        print('4a. Match Test Failed b')
    elif (dist['Match'][2,2,2] != [0.,1.]): 
        print('4a. Match Test Failed c')
    elif (dist['Match'][2,2,1] != [0.,1.]):
        print('4a. Match Test Failed d')
    elif (dist['Match'][2,1,2] != [0.,1.]): 
        print('4a. Match Test Failed e')
    else:
        print('4a. Match Test Passed')

    # Check scoreline for 5 set matches:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.5, 0.7, 5)
    if (dist['Match'][1,1,1,1,1] != [1.,0.]): 
        print('4b. Match Test Failed a')
    elif (dist['Match'][2,1,1,1,1] != [1.,0.]): 
        print('4b. Match Test Failed b')
    elif (dist['Match'][1,1,2,2,1] != [1.,0.]): 
        print('4b. Match Test Failed c')
    elif (dist['Match'][2,1,2,1,2] != [0.,1.]):
        print('4b. Match Test Failed d')
    elif (dist['Match'][2,2,1,2,1] != [0.,1.]):
        print('4b. Match Test Failed e')
    else:
        print('4b. Match Test Passed')

def UnitTest3MatchScore():
    # Set up a "Match Network" using the second approach:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.9, 0.7, 3)
    
    # Check several different scorelines get the correct set winner when 3 sets are played:
    if (dist['MatchScore'][1,1,1] != [1.,0.,0.,0.]): # 2 sets
        print('4a. Match Score Test Failed a')
    elif (dist['MatchScore'][1,1,2] != [1.,0.,0.,0.]): # 2 sets
        print('4a. Match Score Test Failed b')
    elif (dist['MatchScore'][2,2,2] != [0.,0.,1.,0.]): # 2 sets
        print('4a. Match Score Test Failed c')
    elif (dist['MatchScore'][2,2,1] != [0.,0.,1.,0.]): # 2 sets
        print('4a. Match Score Test Failed d')
    elif (dist['MatchScore'][2,1,2] != [0.,0.,0.,1.]): # 3 sets
        print('4a. Match Score Test Failed e')
    else:
        print('4a. Match Score Test Passed')

    # Check scoreline for 5 set matches:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.5, 0.7, 5)
    if (dist['MatchScore'][1,1,1,1,1] != [1.,0.,0.,0.,0.,0.]): # 3 sets
        print('4b. Match Score Test Failed a')
    elif (dist['MatchScore'][2,1,1,1,1] != [0.,1.,0.,0.,0.,0.]): # 4 sets
        print('4b. Match Score Test Failed b')
    elif (dist['MatchScore'][1,1,2,2,1] != [0.,0.,1.,0.,0.,0.]): # 5 sets
        print('4b. Match Score Test Failed c')
    elif (dist['MatchScore'][2,1,2,1,2] != [0.,0.,0.,0.,0.,1.]): # 5 sets
        print('4b. Match Score Test Failed d')
    elif (dist['MatchScore'][2,2,1,2,1] != [0.,0.,0.,0.,1.,0.]): # 4 sets
        print('4b. Match Score Test Failed e')
    else:
        print('4b. Match Score Test Passed')

def UnitTest3TotalNumGames():
    # Set up a "Match Network" using the second approach:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.9, 0.7, 3)
    
    # Check several different scorelines get the correct set winner when 3 sets are played:
    if (dist['TotalNumGames'][1,7,8,9][3] != 1. or dist['TotalNumGames'][1,7,8,9][12] != 0.): # Total games = 15 
        print('4a. Total Number of Games Test Failed a')
    elif (dist['TotalNumGames'][2,7,8,9][3] != 0. or dist['TotalNumGames'][2,7,8,9][12] != 1.): # Total games = 24
        print('4a. Total Number of Games Test Failed b')
    elif (dist['TotalNumGames'][1,6,13,8][7] != 1. or dist['TotalNumGames'][1,6,13,8][15] != 0.): # Total games = 19
        print('4a. Total Number of Games Test Failed c')
    elif (dist['TotalNumGames'][4,6,13,8][15] != 1. or dist['TotalNumGames'][4,6,13,8][22] != 0.): # Total games = 27
        print('4a. Total Number of Games Test Failed d')
    elif (dist['TotalNumGames'][4,13,13,13][27] != 1. or dist['TotalNumGames'][4,13,13,13][14] != 0.): # Total games = 39
        print('4a. Total Number of Games Test Failed e')
    elif (dist['TotalNumGames'][3,6,6,6][0] != 1. or dist['TotalNumGames'][3,6,6,6][6] != 0.): # Total games = 12
        print('4a. Total Number of Games Test Failed f')
    else:
        print('4a. Total Number of Games Test Passed')

    # Check scoreline for 5 set TotalNumGameses:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetwork2(0.5, 0.7, 5)
    if (dist['TotalNumGames'][1,7,8,9,10,6][6] != 1. or dist['TotalNumGames'][1,7,8,9,10,6][16] != 0.): # Total games = 24 
        print('4b. Total Number of Games Test Failed a')
    elif (dist['TotalNumGames'][2,9,9,9,6,12][15] != 1. or dist['TotalNumGames'][2,9,9,9,6,12][27] != 0.): # Total games = 33
        print('4b. Total Number of Games Test Failed b')
    elif (dist['TotalNumGames'][3,13,13,13,13,13][47] != 1.):  # Total games = 65
        print('4b. Total Number of Games Test Failed c')
    elif (dist['TotalNumGames'][4,7,6,13,7,8][8] != 1.): # Total games = 26
        print('4b. Total Number of Games Test Failed d')
    elif (dist['TotalNumGames'][6,6,6,6,6,6][12] != 1.): # Total games = 30
        print('4b. Total Number of Games Test Failed e')
    elif (dist['TotalNumGames'][5,12,10,9,13,6][26] != 1.): # Total games = 44
        print('4b. Total Number of Games Test Failed f')
    else:
        print('4b. Total Number of Games Test Passed')

if __name__ == "__main__":
    TestSuite()
    