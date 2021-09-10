# Import the required functions:
from TennisMatchNetworkCE import TennisMatchNetworkCE
import numpy as np
from TennisSetNetworkEfficient import TennisSetNetworkEfficient
from loopybeliefprop import beliefpropagation
import time

def TimingTennisSetNetwork(P1S, P2S, Iterations, Tol):
    # Set up the Bayesian Network and run the blief propagation algorithm for each set played:
    # Set 1:
    print("Set 1:")
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(P1S, P2S)
    [SetScoreDist1] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['SetScore'])

    # Compute the probability distribution of the number of games played in the set:
    NumGamesDist1 = np.zeros(7, dtype = float)
    for i in range(7):
        NumGamesDist1[i] = SetScoreDist1[i] + SetScoreDist1[i+7]

    # Construct the initial distribution for the next set, based off the number of games in set 1:
    InitServerDist = [sum(NumGamesDist1[[0,2,4,5]]), sum(NumGamesDist1[[1,3,6]])]

    # Set 2:
    print("Set 2:")
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(P1S, P2S, InitServerDist)
    [SetScoreDist2] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['SetScore'])

    # Compute the probability distribution of the number of games played in the set:
    NumGamesDist2 = np.zeros(7, dtype = float)
    for i in range(7):
        NumGamesDist2[i] = SetScoreDist2[i] + SetScoreDist2[i+7]

    # Construct the initial distribution for the next set, based off the number of games in set 2 and the initial server:
    P1Serving = (InitServerDist[0]*sum(NumGamesDist2[[0,2,4,5]]) + InitServerDist[1]*sum(NumGamesDist2[[1,3,6]]))
    InitServerDist = [P1Serving, 1. - P1Serving]

    # Set 3:
    print("Set 3:")
    [nodes, dist, parents, outcomes, info] = TennisSetNetworkEfficient(P1S, P2S, InitServerDist)
    [SetScoreDist3] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol,['SetScore'])

    # Print Distributions:
    print(SetScoreDist1)
    print(SetScoreDist2)
    print(SetScoreDist3)

    return [SetScoreDist1, SetScoreDist2, SetScoreDist3]

def TimingTennisMatchNetwork(SetScoreDists, ConditionalEvents, Iterations, Tol):
    # Run the Match network for given set score distributions:
    [nodes, dist, parents, outcomes, info] = TennisMatchNetworkCE(SetScoreDists, ConditionalEvents)
    [MatchScoreDist,TotalNumGamesDist,AllSetScoresDist] = beliefpropagation(nodes, dist, parents, outcomes, info, 
    Iterations, Tol, ['MatchScore','TotalNumGames','AllSetScores'])
    
    # Print the distributions:
    print(MatchScoreDist)
    print(TotalNumGamesDist)
    print(AllSetScoresDist)

def main():
    # See how long it takes to run 3 Set networks and the match network with conditional events:

    # Set up 5 sets of P values:
    Ps = [[0.6,0.62],[0.54,0.67],[0.75,0.68],[0.76,0.77],[0.643,0.641]]

    # Conditional Events:
    ConditionalEvents = {'CE 1': {'Match Score': [1]}, 'CE2': {'Match Score': [4]}, 'CE 3': {'AllSetScores': [3]},
    'CE 4': {'AllSetScores': [9]}}
    time1Av = 0.
    time2Av = 0.

    # Run each model:
    counter = 0
    for P in Ps:
        counter += 1
        print('Match {}:'.format(counter))
        start1 = time.time()
        # Run the set networks:
        SetScores = TimingTennisSetNetwork(P[0],P[1], 100, 0.001)
        end1 = time.time()
        time1Av += (end1-start1)
        # Run the match network for different conditional events:
        CEcounter = 0
        for CE in ConditionalEvents:
            CEcounter += 1
            print('Conditional Events {}'.format(CEcounter))
            CondEvents = ConditionalEvents[CE]
            start2 = time.time()
            TimingTennisMatchNetwork(SetScores, CondEvents, 100, 0.001)
            end2 = time.time()
            time2Av += (end2-start2)
    time1Av = time1Av/5
    time2Av = time2Av/20
    print("average time TennisSetNetwork")
    print(time1Av)
    print("average time TennisMatchNetwork")
    print(time2Av)

if __name__ == "__main__":
    main()
