import numpy as np
import pandas as pd
import random as rm
import math
import datetime
import csv
from itertools import islice
from time import strptime

def try_parsing_date(text):
    for fmt in (' %d/%m/%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d'):
        try:
            return [datetime.datetime.strptime(text, fmt).date(), fmt]
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def MarkovChainPoint(p):
    prob = np.random.rand()
    if prob <= p:
        Winner = 'Server'
    else:
        Winner = 'Returner'
    return Winner

def MarkovChainGame(p):
    # Initial state does not matter as transition probabilites are the same:
    SPts = 0
    RPts = 0
    while ((SPts < 4) and (RPts < 4)):
        if MarkovChainPoint(p) == 'Server':
            # Point was won by server:
            SPts = SPts + 1
        else:
            # Point was won by returner:
            RPts = RPts + 1
        # Check for 'duece':
        if ((SPts == 3) and (RPts == 3)):
            count = 0
            while (abs(count) != 2):
                if MarkovChainPoint(p) == 'Server':
                    count = count + 1
                else:
                    count = count - 1
            # Check who won the duece battle:
            if count == 2:
                # Server won:
                SPts = SPts + 1
            else:
                RPts = RPts + 1
    # Find out who won:
    if SPts == 4:
        Winner = 'Server'
    else:
        Winner = 'Returner'
    # Return the winner:
    return (Winner)     

def MarkovChainSet(pi, pj, FirstServer, FirstTo):
    # Initial state is who is serving first (i or j):
    if (FirstServer == 'i'):
        Serving = 'i'
    else:
        Serving = 'j'
    iGames = 0
    jGames = 0
    while ((iGames < 6) and (jGames < 6)):
        if Serving == 'i':
            # Player A Serving:
            if MarkovChainGame(pi) == 'Server':
                iGames = iGames + 1
            else:
                jGames = jGames + 1
            
            # Change Server:
            Serving = 'j'
        else:
            # Player B Serving:
            if MarkovChainGame(pj) == 'Returner':
                iGames = iGames + 1
            else:
                jGames = jGames + 1 
            
            # Change Server:
            Serving = 'i'

    # Check for 'tie-breaker':
    if (abs(iGames - jGames) < 2):
        # Play another game:
        if Serving == 'i':
            if MarkovChainGame(pi) == 'Server':
                iGames = iGames + 1
            else:
                jGames = jGames + 1
            Serving == 'j'
        else:
            if MarkovChainGame(pj) == 'Returner':
                iGames = iGames + 1
            else:
                jGames = jGames + 1 
            Serving == 'i'   
            
        # Check if a tie-breaker is needed: (set score = 6-6)
        if ((iGames == 6) and (jGames == 6)):
            # A Tie-Breaker is needed:
            Winner = MarkovChainTieBreaker(pi, pj, Serving, FirstTo)
            # Update set score:
            if Winner == 'i':
                iGames = 7
                jGames = 5
            else:
                iGames = 5
                jGames = 7
            # The server needs to be changed for the next set:
            if Serving == 'i':
                Serving = 'j'
            else:
                Serving = 'i'
        else:
            # Won won the 12th game:
            if iGames == 7:
                Winner = 'i'
            else:
                Winner = 'j'
    else:
        # See who won the set:
        if iGames == 6:
            Winner = 'i'
        else:
            Winner = 'j'
    
    SetScore = [iGames, jGames]
    # Return the winner, set score and player to start serving in the next set:
    return (Winner, SetScore, Serving)

def MarkovChainTieBreaker(pi, pj, Serving, FirstTo):
    # FirstTo tells us if it is a 7 or 10 point tie breaker ("normal" or "super" TB)
    # The person that recieved in the 12th game of the set starts serving
    # The serving goes as follows: (let A = the person with service initially)
    # Player A, Player B, Player B, Player A, Player A, Player B, Player B, Player A, Player A...
    iPoints = 0
    jPoints = 0
    
    # Perform first point:
    if Serving == 'i':
        if MarkovChainPoint(pi) == 'Server':
            iPoints = iPoints + 1
        else:
            jPoints = jPoints + 1
        Serving = 'j'
    else:
        if MarkovChainPoint(pj) == 'Returner':
            iPoints = iPoints + 1
        else:
            jPoints = jPoints + 1 
        Serving = 'i'
    
    Point = 2
    while ((iPoints < FirstTo) and (jPoints < FirstTo)):
        if Serving == 'i':
            if MarkovChainPoint(pi) == 'Server':
                iPoints = iPoints + 1
            else:
                jPoints = jPoints + 1
        else:
            if MarkovChainPoint(pj) == 'Returner':
                iPoints = iPoints + 1
            else:
                jPoints = jPoints + 1 
                
        # Change server if required:
        if Point % 2 == 1:
            if Serving == 'i':
                Serving = 'j'
            else:
                Serving = 'i'
        Point = Point + 1

    # Check the winner won by at least 2:
    if (abs(iPoints - jPoints) < 2):        
        while (abs(iPoints - jPoints) < 2):
            if Serving == 'i':
                if MarkovChainPoint(pi) == 'Server':
                    iPoints = iPoints + 1
                else:
                    jPoints = jPoints + 1
            else:
                if MarkovChainPoint(pj) == 'Returner':
                    iPoints = iPoints + 1
                else:
                    jPoints = jPoints + 1 
                    
            # Change server if required:
            if Point % 2 == 1:
                if Serving == 'i':
                    Serving = 'j'
                else:
                    Serving = 'i'
            Point = Point + 1
            
    # Check who won the tie-breaker:
    if (iPoints > jPoints):
        Winner = 'i'
    else:
        Winner = 'j'
    return Winner

def MarkovChainMatch(pi, pj, FirstServer, FirstToSets, FirstToTB):
    # Initial state does not matter as transition probabilites are the same:
    iSets = 0
    jSets = 0
    SetScores = []
    while ((iSets < FirstToSets) and (jSets < FirstToSets)):
        [Winner, SetScore, Serving] = MarkovChainSet(pi, pj, FirstServer, FirstToTB)
        SetScores.append(SetScore)
        if Winner == 'i':
            iSets = iSets + 1
        else:
            jSets = jSets + 1
        
        # Update first server for the next set:
        FirstServer = Serving
    
    # Check who won the Match:
    if iSets == FirstToSets:
        # Server won:
        Winner = 'i'
    else:
        Winner = 'j'
    
    # Return the winner and Set Scores
    return (Winner, SetScores)

def Game(P):
    # Single Service Game:
    Game = pow(P,4) * (15 - 4*P - ((10 * pow(P,2)) / (1 - 2 * P * (1 - P))))
    return Game

def TB(P, Q):
    # Import A Matrix:
    [A, B] = Matrices()
    # Tie-Breaker: (7 Pointer)
    TB = 0
    for i in range(28):
        TB += A[i][0] * pow(P,A[i][1]) * pow((1-P),A[i][2]) * pow(Q,A[i][3]) * pow((1-Q),A[i][4]) * pow(D(P, Q),A[i][5])
    return TB

def Set(P, Q, A, B):
    # Set:
    Set = 0
    for i in range(21):
        Set += B[i][0] * pow(Game(P),B[i][1]) * pow((1-Game(P)),B[i][2]) * pow(Game(Q),B[i][3]) * pow((1-Game(Q)),B[i][4])\
        * pow((Game(P)*Game(Q) + (Game(P)*(1-Game(Q)) + (1-Game(P))*Game(Q)) * TB(P,Q)),B[i][5])
    return Set

def Match3(P, Q, A, B):
    Match = pow(Set(P,Q,A,B),2) * (1 + 2 * (1 - Set(P,Q,A,B)))
    return Match

def Match5(P, Q, A, B):
    Match = pow(Set(P,Q,A,B),3) * (1 + 3 * (1 - Set(P,Q,A,B)) + 6 * pow((1 - Set(P,Q,A,B)),2))
    return Match

def D(P, Q):
    D = P * Q * pow((1 - (P * (1-Q) + (1-P) * Q)), -1)
    return D

def Matrices():
    A = [[1,3,0,4,0,0],[3,3,1,4,0,0],[4,4,0,3,1,0],[6,3,2,4,0,0],[16,4,1,3,1,0],[6,5,0,2,2,0],[10,2,3,5,0,0],[40,3,2,4,1,0],
    [30,4,1,3,2,0],[4,5,0,2,3,0],[5,1,4,6,0,0],[50,2,3,5,1,0],[100,3,2,4,2,0],[50,4,1,3,3,0],[5,5,0,2,4,0],[1,1,5,6,0,0],
    [30,2,4,5,1,0],[150,3,3,4,2,0],[200,4,2,3,3,0],[75,5,1,2,4,0],[6,6,0,1,5,0],[1,0,6,6,0,1],[36,1,5,5,1,1],[225,2,4,4,2,1],
    [400,3,3,3,3,1],[225,4,2,2,4,1],[36,5,1,1,5,1],[1,6,0,0,6,1]]
    B = [[1,3,0,3,0,0],[3,3,1,3,0,0],[3,4,0,2,1,0],[6,2,2,4,0,0],[12,3,1,3,1,0],[3,4,0,2,2,0],[4,2,3,4,0,0],[24,3,2,3,1,0],
    [24,4,1,2,2,0],[4,5,0,1,3,0],[5,1,4,5,0,0],[40,2,3,4,1,0],[60,3,2,3,2,0],[20,4,1,2,3,0],[1,5,0,1,4,0],[1,0,5,5,0,1],
    [25,1,4,4,1,1],[100,2,3,3,2,1],[100,3,2,2,3,1],[25,4,1,1,4,1],[1,5,0,0,5,1]]
    return A, B

def nth_index(iterable, value, n):
    # Find the nth position of a value in an array:
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)

def combine_recursion(n, k):
    # Combinatoric Generator:
    result = []
    combine_dfs(n, k, 1, [], result)
    return result

def combine_dfs(n, k, start, path, result):
    if k == len(path):
        result.append(path)
        return
    for i in range(start, n + 1):
        combine_dfs(n, k, i + 1, path + [i], result)

def TieBreakerProbability(P1S, P2S, Iter, FirstTo):
    # Compute the probability of winning a TB using the MarkovTB Simulation:
    Count1 = 0
    Count2 = 0
    for i in range(Iter):
        # Player 1 Serving first:
        Winner1 = MarkovChainTieBreaker(P1S, P2S, 'i', FirstTo)
        # Player 2 Serving first:
        Winner2 = MarkovChainTieBreaker(P1S, P2S, 'j', FirstTo)
        if (Winner1 == 'i'):
            Count1 = Count1 + 1
        if (Winner2 == 'j'):
            Count2 = Count2 + 1
    
    # Compute their probability of winning when they start the TB serving:
    return [Count1/Iter, Count2/Iter] # Prob Player 1 winning if he serves first, Prob Player 2 winning if he serves first

def ComputeTBProbabilities(P1S, P2S):
    #Find which row and column these Pserve probabilities correspond to in the TBProbs matrix:
    Row = round((P1S - 0.50) / 0.01)
    Col = round((P2S - 0.50) / 0.01)

    # Compute the tie-breaker probabilities using pre-calculated values from a simulation:
    with open('CSVFiles\\TBProbabilities.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == Row:
                P1TB = float(row[Col])
                # Compute P2TB:
                P2TB = 1. - P1TB
                return P1TB, P2TB
            else:
                line_count += 1

def OddsComputer(FirstOdds, Margin = 0.08):
    SecondOdds = FirstOdds / (FirstOdds * (1. + 0.5 * Margin) - 1)
    return SecondOdds

def RemainingOdds(Odds, Margin = 0.08):
    Probs = 0.
    for i in Odds:
        Probs += (1. / i)
    
    # Check if odds are too low:
    if (1. + Margin <= Probs):
        print("Increase Odds, current implied probability is {}".format(100*Probs))
    else:
        RemainP = (1. + Margin - Probs)
        return (1. / RemainP)