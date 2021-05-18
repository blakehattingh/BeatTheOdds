import numpy as np
import math
# import matplotlib.pyplot as plt
from loopybeliefprop import beliefpropagation, noinfo, choose
from MarkovSimulations import MarkovChainTieBreaker

# Combinatoric Generator:
def combine_recursion(n, k):
    result = []
    combine_dfs(n, k, 1, [], result)
    return result

def combine_dfs(n, k, start, path, result):
    if k == len(path):
        result.append(path)
        return
    for i in range(start, n + 1):
        combine_dfs(n, k, i + 1, path + [i], result)


def TennisSet():
    # Specify the names of the nodes in the Bayesian network
    nodes=['ServerOdd', 'ServerEven','Set','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12','TB']

    # Defining parent nodes:
    parents={}
    parents['ServerEven']=['ServerOdd']
    parents['G1']=['ServerOdd']
    parents['G2']=['ServerEven']
    parents['G3']=['ServerOdd']
    parents['G4']=['ServerEven']
    parents['G5']=['ServerOdd']
    parents['G6']=['ServerEven']
    parents['G7']=['ServerOdd']
    parents['G8']=['ServerEven']
    parents['G9']=['ServerOdd']
    parents['G10']=['ServerEven']
    parents['G11']=['ServerOdd']
    parents['G12']=['ServerEven']
    parents['TB']=['ServerOdd']
    parents['Set']=['G1', 'G2', 'G3', 'G4','G5','G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'TB']

    # Set up the possible outcomes for each node:
    outcomes={}
    outcomes['ServerOdd']=["P1Serves","P2Serves"]
    outcomes['ServerEven']=["P1Serves","P2Serves"]
    outcomes['G1']=[1,2]
    outcomes['G2']=[1,2]
    outcomes['G3']=[1,2]
    outcomes['G4']=[1,2]
    outcomes['G5']=[1,2]
    outcomes['G6']=[1,2]
    outcomes['G7']=[1,2]
    outcomes['G8']=[1,2]
    outcomes['G9']=[1,2]
    outcomes['G10']=[1,2]
    outcomes['G11']=[1,2]
    outcomes['G12']=[1,2]
    outcomes['TB']=[1,2]
    outcomes['Set']=[1,2]

    # Compute the probability of winning a game on serve from the on-serve point probabilities:
    P1S = 0.7
    P2S = 0.65
    P1G = pow(P1S, 2) / (pow(P1S, 2) + pow((1-P1S), 2))
    P2G = pow(P2S, 2) / (pow(P2S, 2) + pow((1-P2S), 2))

    # Compute the probability of winning a TB using the MarkovTB Simulation:
    Iter = 1000
    FirstTo = 7 # Need to update this to include all possibilities, e.g. 'if Tournament = US Open then firstTo = 7'

    # Player A serving first:
    Count1 = 0
    Count2 = 0
    for i in range(Iter):
        Winner1 = MarkovChainTieBreaker(P1S, P2S, 'i', FirstTo)
        Winner2 = MarkovChainTieBreaker(P1S, P2S, 'j', FirstTo)
        if (Winner1 == 'i'):
            Count1 = Count1 + 1
        if (Winner2 == 'j'):
            Count2 = Count2 + 1
    
    # Compute their probability of winning when they start the TB serving:
    P1TB = Count1/Iter
    P2TB = Count2/Iter

    # Equal chance of each player serving the first game: (Can update if the toss has been done)
    dist={}
    dist['ServerOdd'] = [0.5,0.5]
    dist['ServerEven'] = {}
    dist['ServerEven']["P1Serves"] = [0.,1.]
    dist['ServerEven']["P2Serves"] = [1.,0.]

    # Set up dictionaries for each game:
    dist['G1']={}
    dist['G2']={}
    dist['G3']={}
    dist['G4']={}
    dist['G5']={}
    dist['G6']={}
    dist['G7']={}
    dist['G8']={}
    dist['G9']={}
    dist['G10']={}
    dist['G11']={}
    dist['G12']={}
    dist['TB']={}
    
    # Define the probabilities for each game, given the server:
    # Player 1 serving:
    dist['G1']["P1Serves"]=[P1G,1.-P1G]
    dist['G2']["P1Serves"]=[P1G,1.-P1G]
    dist['G3']["P1Serves"]=[P1G,1.-P1G]
    dist['G4']["P1Serves"]=[P1G,1.-P1G]
    dist['G5']["P1Serves"]=[P1G,1.-P1G]
    dist['G6']["P1Serves"]=[P1G,1.-P1G]
    dist['G7']["P1Serves"]=[P1G,1.-P1G]
    dist['G8']["P1Serves"]=[P1G,1.-P1G]
    dist['G9']["P1Serves"]=[P1G,1.-P1G]
    dist['G10']["P1Serves"]=[P1G,1.-P1G]
    dist['G11']["P1Serves"]=[P1G,1.-P1G]
    dist['G12']["P1Serves"]=[P1G,1.-P1G]
    dist['TB']["P1Serves"]=[P1TB,1.-P1TB]

    # Player 2 serving:
    dist['G1']["P2Serves"]=[1.-P2G,P2G]
    dist['G2']["P2Serves"]=[1.-P2G,P2G]
    dist['G3']["P2Serves"]=[1.-P2G,P2G]
    dist['G4']["P2Serves"]=[1.-P2G,P2G]
    dist['G5']["P2Serves"]=[1.-P2G,P2G]
    dist['G6']["P2Serves"]=[1.-P2G,P2G]
    dist['G7']["P2Serves"]=[1.-P2G,P2G]
    dist['G8']["P2Serves"]=[1.-P2G,P2G]
    dist['G9']["P2Serves"]=[1.-P2G,P2G]
    dist['G10']["P2Serves"]=[1.-P2G,P2G]
    dist['G11']["P2Serves"]=[1.-P2G,P2G]
    dist['G12']["P2Serves"]=[1.-P2G,P2G]
    dist['TB']["P2Serves"]=[1.-P2TB,P2TB]

    # Define the possible outcomes of the set, given a sequence of outcomes from all 12 games and the TB:
    dist['Set']={}
    dist['Set'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1.,0.]
    for i in range(1,14):
        Seqs = combine_recursion(13,i)

        for j in Seqs:
            InitialSeq = [1,1,1,1,1,1,1,1,1,1,1,1,1]

            # Place the '2's in each possible combination:
            for spots in j:
                InitialSeq[spots-1] = 2

            # Assign the correct winner:
            InitialSeq = tuple(InitialSeq)

            # Case 1: (i (Player 2 wins) < 6)
            if (i < 6):
                # Player 1 wins:
                dist['Set'][InitialSeq] = [1.,0.]
            
            # Case 2: (i > 7):
            elif (i > 7):
                # Player 2 wins:
                dist['Set'][InitialSeq] = [0.,1.]

            # Case 3: (i = 6 or 7)
            else:
                # Check the first 12 games to see if a tie-breaker was required:
                First12 = InitialSeq[:-1]
                P2Wins = First12.count(2)
                if (P2Wins > 5):
                    # Player 2 wins:
                    dist['Set'][InitialSeq] = [0.,1.]
                else:
                    # Player 1 wins:
                    dist['Set'][InitialSeq] = [1.,0.]
                
                # Check if a tie-breaker was needed:
                if (P2Wins == 6):
                    # Check who won the TB:
                    if (InitialSeq[-1] == 2):
                        # Player 2 won the TB and therefore the set too:
                        dist['Set'][InitialSeq] = [0.,1.]
                    else:
                        # Player 1 wins:
                        dist['Set'][InitialSeq] = [1.,0.]                 
   
    # Set up initial information:
    info={}
    for i in nodes:
        info[i] = choose(outcomes[i], "NotSure")
    
    return(nodes, dist, parents, outcomes, info)

    ######################## USER INPUT STARTS HERE ###########################

def main():
    # Model Parameters:
    
    # Max Number of Iterations until Steady State reached:
    Iterations = 100
    # Tolerance level on Steady States:
    Tol = 0.001

    # Set up the model and run it with no first server info:
    [nodes, dist, parents, outcomes, info] = TennisSet()
    DistNoServer = beliefpropagation(nodes,dist,parents,outcomes,info,Iterations,Tol)

    # In-match betting:
    # Known Events: 
    # Specify any given information for any in-match event
    # - Utilise the "choose" function which takes two arguments: an ordered list of outcomes, and the specified outcome name.

    # Before Play betting:
    # No in-match events known
    # We Still need to specify the "info" for each node in our network
    # - Use any name/number not in the list of outcomes as your choice (done in Tennis function)    

def TennisMatch(NumSets):
    x = 10
######################### USER INPUT ENDS HERE ############################

if __name__ == "__main__":
    main()
