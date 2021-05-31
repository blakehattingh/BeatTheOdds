def main():
    # Model Parameters:
    


    # Set up the model and run it with no first server info:
    [nodes, dist, parents, outcomes, info] = TennisMatch(3)
    #info['Set'] = choose(outcomes['Set'], "1")
    start = time.time()
    #DistNoServer = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol)
    DistSet1, DistSet2, DistSet3\
        , numGames1, numGames2, numGames3,\
            setScore1,setScore2,setScore3,\
                totalGames, allSetScores, match = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol)
    end = time.time()
    timeTaken = end - start

    print("time taken (s) = " + str(timeTaken))
    print("")

    print("set1 = " + str(DistSet1))
    print("set2 = " + str(DistSet2))
    print("set3 = " + str(DistSet3))
    print("")

    print("Number of Games 1 = " + str(numGames1))
    print("Number of Games 2 = " + str(numGames2))
    print("Number of Games 3 = " + str(numGames3))
    print("")

    print("Set Score set 1 = " + str(setScore1))
    print("Set Score set 2 = " + str(setScore2))
    print("Set Score set 3 = " + str(setScore3))
    print("")

    print("total games = " + str(totalGames))
    print("all set scores = " + str(allSetScores))

    print("Match = " + str(match))

    
    # - Set, Set2, ... Set5
    # - NumGames, NumGames2...
    # - Match
    
    # - SetScore, SetScore2...
    # - TotalNumGames, AllSetScores


    # In-match betting:
    # Known Events: 
    # Specify any given information for any in-match event
    # - Utilise the "choose" function which takes two arguments: an ordered list of outcomes, and the specified outcome name.

    # Before Play betting:
    # No in-match events known
    # We Still need to specify the "info" for each node in our network
    # - Use any name/number not in the list of outcomes as your choice (done in Tennis function)    

######################### USER INPUT ENDS HERE ############################

if __name__ == "__main__":
    main()


from typing import Sequence
import numpy as np
import math
import statistics as stats
# import matplotlib.pyplot as plt
from loopybeliefprop import beliefpropagation, noinfo, choose
from MarkovSimulations import MarkovChainTieBreaker
from itertools import islice
from tennisMatch2 import TennisMatch1, TennisMatch2
# import seaborn as sns

    ######################## USER INPUT STARTS HERE ###########################

def main():
    # Model Parameters:
    P1S = 0.7
    P2S = 0.65
    FirstToSets = 3
    FirstToTBPoints = 7

    # Max Number of Iterations until Steady State reached:
    Iterations = 100
    # Tolerance level on Steady States:
    Tol = 0.0001
    
    # Compute the Tie-Breaker probabilities using a simulation approach:
    [P1TB, P2TB] = TieBreakerProbability(P1S, P2S, Iter = 10000, FirstTo = 7)

    distNoServersNoInfo = []
    distNoServersP1S = []
    distNoServersP2S = []
    distNoServersAll = []

    distTBNoInfo = []
    distTBP1S = []
    distTBP2S = []
    distTBAll = []

    trialRuns = 2

    # [nodes, dist, parents, outcomes, info] = TennisSet()
    # #info['Set'] = choose(outcomes['Set'], 1)
    # info['ServerOdd'] = choose(outcomes['ServerOdd'], "P2Serves")
    # [DistNoServer, distTB] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol)
    
    for i in range(trialRuns):
    # Set up the model and run it with no first server info:
        [nodes, dist, parents, outcomes, info] = TennisSet()
        #info['ServerOdd'] = choose(outcomes['ServerOdd'], "P1Serves")
        [DistNoServer, distTB] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol)
        distNoServersNoInfo.append(DistNoServer[0])
        distTBNoInfo.append(distTB[0])


    for i in range(trialRuns):
    # Set up the model and run it with no first server info:
        [nodes, dist, parents, outcomes, info] = TennisSet()
        info['ServerOdd'] = choose(outcomes['ServerOdd'], "P1Serves")
        [DistNoServer, distTB] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol)
        distNoServersP1S.append(DistNoServer[0])
        distTBP1S.append(distTB[0])


    for i in range(trialRuns):
    # Set up the model and run it with no first server info:
        [nodes, dist, parents, outcomes, info] = TennisSet()
        info['ServerOdd'] = choose(outcomes['ServerOdd'], "P2Serves")
        [DistNoServer, distTB] = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol)
        distNoServersP2S.append(DistNoServer[0])
        distTBP2S.append(distTB[0]) 

    distNoServersAll = distNoServersNoInfo + distNoServersP1S + distNoServersP2S
    distTBAll = distTBNoInfo + distTBP1S + distTBP2S

    print("")
    print("Variance (no info) = " + str(stats.variance(distNoServersNoInfo)))
    print("Mean (no info) = " + str(stats.mean(distNoServersNoInfo)))
    print("Spread (no info) = " + str((max(distNoServersNoInfo)- min(distNoServersNoInfo))*100) + "%")
    print("")

    print("Variance TB (no info) = " + str(stats.variance(distTBNoInfo)))
    print("Mean TB (no info) = " + str(stats.mean(distTBNoInfo)))
    print("Spread TB (no info) = " + str((max(distTBNoInfo)- min(distTBNoInfo))*100) + "%")
    print("")

    print("Variance (P1Serves) = " + str(stats.variance(distNoServersP1S)))
    print("Mean (P1Serves) = " + str(stats.mean(distNoServersP1S)))
    print("Spread (P1Serves) = " + str((max(distNoServersP1S)- min(distNoServersP1S))*100) + "%")
    print("")

    print("Variance TB (P1Serves) = " + str(stats.variance(distTBP1S)))
    print("Mean TB (P1Serves) = " + str(stats.mean(distTBP1S)))
    print("Spread TB (P1Serves) = " + str((max(distTBP1S)- min(distTBP1S))*100) + "%")
    print("")

    print("Variance (P2Serves) = " + str(stats.variance(distNoServersP2S)))
    print("Mean (P2Serves) = " + str(stats.mean(distNoServersP2S)))
    print("Spread (P2Serves) = " + str((max(distNoServersP2S)- min(distNoServersP2S))*100) + "%")
    print("")

    print("Variance TB (P2Serves) = " + str(stats.variance(distTBP2S)))
    print("Mean TB (P2Serves) = " + str(stats.mean(distTBP2S)))
    print("Spread TB (P2Serves) = " + str((max(distTBP2S)- min(distTBP2S))*100) + "%")
    print("")

    print("Variance (all) = " + str(stats.variance(distNoServersAll)))
    print("Mean (all) = " + str(stats.mean(distNoServersAll)))
    print("Spread (all) = " + str((max(distNoServersAll)- min(distNoServersAll))*100) + "%")
    print("")

    print("Variance TB (all) = " + str(stats.variance(distTBAll)))
    print("Mean TB (all) = " + str(stats.mean(distTBAll)))
    print("Spread TB (all) = " + str((max(distTBAll)- min(distTBAll))*100) + "%")
    print("")

if __name__ == "__main__":
    main()



