# Import the required functions:
from MarkovModel import AdditionalFunctions, loopybeliefprop, OMalleysEqns
#from AdditionalFunctions import combine_recursion, nth_index
#from loopybeliefprop import choose
#from OMalleysEqns import TB

def TennisSetNetworkEfficient(P1S, P2S, InitServerDist = [0.5, 0.5], ConditionalEvents = {}):
    # Specify the names of the nodes in the Bayesian network
    nodes=['ServerOdd','ServerEven','SetScore','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12','TB']

    # Defining parent nodes:
    parents={}
    parents['ServerEven']=['ServerOdd']
    GameNodes = ['G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12','TB']
    EvenGames = ['G2','G4','G6','G8','G10','G12']
    OddGames = ['G1','G3','G5','G7','G9','G11','TB']
    for node in GameNodes:
        if (node in OddGames):
            parents[node] = ['ServerOdd']
        else:
            parents[node] = ['ServerEven']
    parents['SetScore']=['G1', 'G2', 'G3', 'G4','G5','G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'TB']

    # Set up the possible outcomes for each node:
    outcomes={}
    outcomes['ServerOdd']=['P1Serves','P2Serves']
    outcomes['ServerEven']=['P1Serves','P2Serves']
    for node in GameNodes:
        outcomes[node] = [1, 2]
    outcomes['SetScore']=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]

    # Compute the probability of winning a game on serve from the on-serve point probabilities:
    P1G = pow(P1S, 4) * (15 - 4 * P1S - (10 * pow(P1S, 2) / (1 - 2 * P1S * (1 - P1S))))
    P2G = pow(P2S, 4) * (15 - 4 * P2S - (10 * pow(P2S, 2) / (1 - 2 * P2S * (1 - P2S))))

    # Compute the probability of winning a TB starting with service:
    P1TB = OMalleysEqns.TB(P1S, 1 - P2S)
    P2TB = OMalleysEqns.TB(P2S, 1 - P1S)

    # Set up dictionaries for each game:
    dist={}
    for node in nodes:
        dist[node] = {}

    # Equal chance of each player serving the first game: (Can update if the toss has been done)
    dist['ServerOdd'] = InitServerDist
    dist['ServerEven']['P1Serves'] = [0.,1.]
    dist['ServerEven']['P2Serves'] = [1.,0.]

    # Define the probabilities for each game, given the server:
    for node in GameNodes:
        if (node == 'TB'):
            dist[node]['P1Serves'] = [P1TB, 1. - P1TB]
            dist[node]['P2Serves'] = [1. - P2TB, P2TB]
        else:
            dist[node]['P1Serves'] = [P1G, 1. - P1G]
            dist[node]['P2Serves'] = [1. - P2G, P2G]

    # Define the possible outcomes of the set, given a sequence of outcomes from all 12 games and the TB:
    dist['SetScore'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]

    # Possible Set Scores and Number of Games:
    SetScores = [[6,0],[6,1],[6,2],[6,3],[6,4],[7,5],[7,6],[0,6],[1,6],[2,6],[3,6],[4,6],[5,7],[6,7]]

    for i in range(1,14):
        Seqs = AdditionalFunctions.combine_recursion(13,i)

        for j in Seqs:
            # Reset Sequences and distributions:
            InitialSeq = [1,1,1,1,1,1,1,1,1,1,1,1,1]
            SetScoresDist = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]

            # Place the '2's in each possible combination:
            for games in j:
                InitialSeq[games-1] = 2

            # Assign the correct winner:
            Sequence = tuple(InitialSeq)

            # Compute the set score:
            Game = 0
            iGames = 0
            jGames = 0

            # Case 1: Set did not go beyond 10 games
            if (i <= 4 or i > 8):
                while (iGames < 6 and jGames < 6):
                    if (InitialSeq[Game] == 1):
                        iGames = iGames + 1
                    else:
                        jGames = jGames + 1
                    Game = Game + 1
                
                # Compute score and number of games:
                SetScore = [iGames, jGames]
                NumGames = sum(SetScore)

                # Find the index corresponding to this outcome:
                IndexSS = SetScores.index(SetScore)

                # Assign the correct outcome to the respective leaf node:
                SetScoresDist[IndexSS] = 1.
                dist['SetScore'][Sequence] = SetScoresDist

            else: # Case 2:
                # Check if the game went beyond 10 games:
                First10Games = InitialSeq[0:10]
                if (First10Games.count(1) == 5):
                    # Set went to 10+ games
                    while (iGames < 7 and jGames < 7):
                        if (InitialSeq[Game] == 1):
                            iGames = iGames + 1
                        else:
                            jGames = jGames + 1
                        Game = Game + 1

                    # Compute score and number of games:
                    SetScore = [iGames, jGames]
                    NumGames = sum(SetScore)

                    # Find the index corresponding to this outcome:
                    IndexSS = SetScores.index(SetScore)

                    # Assign the correct outcome to the respective leaf node:
                    SetScoresDist[IndexSS] = 1.
                    dist['SetScore'][Sequence] = SetScoresDist

                else: 
                    # Set went to 10- games
                    while (iGames < 6 and jGames < 6):
                        if (InitialSeq[Game] == 1):
                            iGames = iGames + 1
                        else:
                            jGames = jGames + 1
                        Game = Game + 1

                    # Compute score and number of games:
                    SetScore = [iGames, jGames]

                    # Find the index corresponding to this outcome:
                    IndexSS = SetScores.index(SetScore)

                    # Assign the correct outcome to the respective leaf node:
                    SetScoresDist[IndexSS] = 1.
                    dist['SetScore'][Sequence] = SetScoresDist

    # Set up initial information:
    info={}
    for i in nodes:
        if (i in ConditionalEvents.keys()):
            # Fix certian nodes identfied by user:
            info[i] = loopybeliefprop.choose(outcomes[i], ConditionalEvents[i])
        else:
            # Otherwise leave them unfixed:
            info[i] = loopybeliefprop.choose(outcomes[i], [])
    return(nodes, dist, parents, outcomes, info)