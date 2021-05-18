import numpy as np
import pandas as pd
import random as rm
import math

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