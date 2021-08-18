from datetime import datetime, timedelta
from typing import Match
from pandas.core.base import DataError
import os, sys
relativePath = os.path.abspath('')
#sys.path.append(relativePath + '\\MarkovModel')
sys.path.append(relativePath + '\\DataExtraction')
#from FirstImplementation import MarkovModelFirstImplementation
from TestSetCollector import *
from DataCollector import *
import pandas as pd
import numpy as np

def ObjectiveMetricMatchOutcome(MatchDist, Winner):
    # See who the Markov Model (MM) has as winner:
    if (MatchDist[0] > 0.5):
        MMWinner = 1
    else:
        MMWinner = 0
    
    # Compare it with the actual winner:
    if (MMWinner == Winner):
        Obj = 1
    else:
        Obj = 0
    return Obj

def ObjectiveMetricSetScore(AllSetScoreDist, SetScores):
    # See which Set Scores the Markov Model has as most likely: (top 3)
    BiggestSS = AllSetScoreDist.index(max(AllSetScoreDist))
    AllSetScoreDist.remove(max(AllSetScoreDist))
    SecondSS = AllSetScoreDist.index(max(AllSetScoreDist))
    AllSetScoreDist.remove(max(AllSetScoreDist))
    ThirdSS = AllSetScoreDist.index(max(AllSetScoreDist))

    # Set Scores:
    SS = [[6,0],[6,1],[6,2],[6,3],[6,4],[7,5],[7,6],[0,6],[1,6],[2,6],[3,6],[4,6],[5,7],[6,7]]
    TopSS = [SS[BiggestSS], SS[SecondSS], SS[ThirdSS]]

    # Record Points:
    Points = 0
    for Score in SetScores:
        for i in range(3):
            if (Score == TopSS[i]):
                Points += (3-i)
    return Points

def ObjectiveMatchScoreDist(MatchScoreDist, MatchScore):
    x = 10

def InterpolateDists(Pa, Pb):
    x = 10
    
def try_parsing_date(text):
    for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def EvalEquation(age):
    testYears = [2012,2014,2016,2018,2019]
    sampledMatchesByYears = getTestMatchData(testYears)
    ageGap = timedelta(days=365.25*age)

    for year in sampledMatchesByYears:
        for match in year:
            dateOfMatch = match[3]
            startOfDataCollection = dateOfMatch - ageGap
            p1vP2,p1vCO,p2vCO,COIds = getSPWData(match, startOfDataCollection)
            Pa,Pb = CalcPEquation1(match, p1vP2, p1vCO, p2vCO, COIds, 0.3,0.3)
            print(Pa,Pb)

    

    # Evaluate the objective metrics:

    # Match Outcome:
    #Prop = ObjectiveMatchScoreDist(MatchScoreDist, MatchData['MatchOutcome'])
    
    # Set Scores:
    #Points = ObjectiveMetricSetScore(AllSetScoresDist, MatchData['SetScores'])

    # Return Objective:
    #ObjectiveVals = {'MatchOutcome': Prop, 'SetScores': Points, 'MatchScore': 0}
    #return ObjectiveVals

def CalcPEquation1(MatchData,PrevMatches,PrevMatchesCommA,PrevMatchesCommB,CommonOpps,Lamda,SurfaceParameter):
    # This function takes in a match, extracts who is playing, when the match is/was played, and what surface it is/was played on
    # It then computes the P values for both players using method 1 (FOR NOW, can integrate it to use a specified method)
    # Inputs:
    # - MatchData = Data on a single match to be predicted on
    # - PrevMatches = The previous matches between the players playing in the match
    # - PrevMatchesCommA / B = The matches between player A / B and the common opponents
    # - CommonOpps = A list of common opponent IDs
    # - Lamda = A parameter corresponding to the weighting between spw(A,B) and spw(A,C)
    # - SurfaceParameter = A hyperparameter corresponding to the weighting on matches played on the same surface

    # Extract required info:
    Date = MatchData[3]
    Surface = MatchData[4]
    PlayerA = MatchData[8]
    PlayerB = MatchData[18]
    SetScores = MatchData[28]
    AwonSets = MatchData[30]
    BwonSets = MatchData[31]
    AwonGames = MatchData[32]
    BwonGames = MatchData[32]

    # Compute SPW(A,B) and SPW(B, A):
    [spwAB, spwBA] = ComputeSPW(PlayerA, PlayerB, PrevMatches, SurfaceParameter, Date, Surface)
    print('spwAB:', spwAB, 'spwBA:', spwBA)

    # Compute RPW(A,B) and RPW(B,A)
    rpwAB = 1. - spwBA
    rpwBA = 1. - spwAB

    # Compute SPW(A,C) and SPW(B,C):
    [spwAC, rpwAC] = ComputeSPWCommon(PlayerA, PrevMatchesCommA, CommonOpps, SurfaceParameter, Date, Surface) 
    [spwBC, rpwBC] = ComputeSPWCommon(PlayerB, PrevMatchesCommB, CommonOpps, SurfaceParameter, Date, Surface)

    print('spwAC:', spwAC, 'rpwAC:', rpwAC)
    print('spwBC:', spwBC, 'rpwBC:', rpwBC) 

    # Compute P Values:
    Pa = (1  - Lamda) * spwAB + Lamda * spwAC
    Pb = (1  - Lamda) * spwBA + Lamda * spwBC

    print('Pa:', Pa, 'Pb:', Pb)
    return Pa, Pb

def ComputeSPW(PlayerA, PlayerB, PrevMatches, SurfaceParameter, Date, Surface):
    # Inputs:
    # - PlayerA & PlayerB = IDs of both players of interest 
    # - PrevMatches = A list of tuples of all previous matches between player A and player B
    # - SurfaceParameter = A hyperparameter corresponding to the weighting on matches played on the same surface
    # - Date = The date of the match as a string in format '%Y-%m-%d'
    # - Surface = The surface that the match will be played on (as an abbrev, e.g. C = Clay)

    # Sum up the service points played for each player:
    PlayerAServePointsSurface = 0
    PlayerAServePointsWonSurface = 0
    PlayerBServePointsSurface = 0
    PlayerBServePointsWonSurface = 0
    PlayerAServePointsNS = 0
    PlayerAServePointsWonNS = 0
    PlayerBServePointsNS = 0
    PlayerBServePointsWonNS = 0
    for match in range(len(PrevMatches)):
        # Check when the match was played:
        MatchDate = PrevMatches[match][3]

        if ((Date - MatchDate).days > 0):
            if (PrevMatches[match][4] == Surface):
                if (PrevMatches[match][8] == PlayerA):
                    PlayerAServePointsSurface += PrevMatches[match][42]
                    PlayerAServePointsWonSurface += (PrevMatches[match][44] + PrevMatches[match][45])
                    PlayerBServePointsSurface += PrevMatches[match][51]
                    PlayerBServePointsWonSurface += (PrevMatches[match][53] + PrevMatches[match][54])
                else:
                    PlayerAServePointsSurface += PrevMatches[match][51]
                    PlayerAServePointsWonSurface += (PrevMatches[match][53] + PrevMatches[match][54])
                    PlayerBServePointsSurface += PrevMatches[match][42]
                    PlayerBServePointsWonSurface += (PrevMatches[match][44] + PrevMatches[match][45])
            else:
                if (PrevMatches[match][8] == PlayerA):
                    PlayerAServePointsNS += PrevMatches[match][42]
                    PlayerAServePointsWonNS += (PrevMatches[match][44] + PrevMatches[match][45])
                    PlayerBServePointsNS += PrevMatches[match][51]
                    PlayerBServePointsWonNS += (PrevMatches[match][53] + PrevMatches[match][54])
                else:
                    PlayerAServePointsNS += PrevMatches[match][51]
                    PlayerAServePointsWonNS += (PrevMatches[match][53] + PrevMatches[match][54])
                    PlayerBServePointsNS += PrevMatches[match][42]
                    PlayerBServePointsWonNS += (PrevMatches[match][44] + PrevMatches[match][45])
            
    # Compute the proportion of service points won:
    print(PlayerAServePointsSurface, PlayerAServePointsNS)
    print(len(PrevMatches))
    PlayerAServiceProp = (1 - SurfaceParameter) * (PlayerAServePointsWonSurface / PlayerAServePointsSurface) + SurfaceParameter * (PlayerAServePointsWonNS / PlayerAServePointsNS)
    PlayerBServiceProp = (1 - SurfaceParameter) * (PlayerBServePointsWonSurface / PlayerBServePointsSurface) + SurfaceParameter * (PlayerBServePointsWonNS / PlayerBServePointsNS)

    return PlayerAServiceProp, PlayerBServiceProp

def ComputeSPWCommon(PlayerA, PrevMatchesCommOpps, CommonOpps, SurfaceParameter, Date, Surface):    
    # Inputs:
    # - PlayerA = ID of both player A
    # - PrevMatchesCommOpps = A list of tuples of all previous matches between player A the common opponents
    # - CommonOpps = A list of the IDs of all common opponents
    # - SurfaceParameter = A hyperparameter corresponding to the weighting on matches played on the same surface
    # - Date = The date of the match as a string in format '%Y-%m-%d'
    # - Surface = The surface that the match will be played on (as an abbrev, e.g. C = Clay)

    # Sum up the service points played for each player:
    PlayerAServePointsSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAServePointsWonSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAServePointsNS = np.zeros(len(CommonOpps), dtype = int)
    PlayerAServePointsWonNS = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsWonSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsNS = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsWonNS = np.zeros(len(CommonOpps), dtype = int)
    for match in range(len(PrevMatchesCommOpps)):
        # Check when the match was played:
        MatchDate = PrevMatchesCommOpps[match][3]

        if ((Date - MatchDate).days > 0):
            if (Surface == PrevMatchesCommOpps[match][4]):
                if (PrevMatchesCommOpps[match][8] == PlayerA):
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][18])
                    PlayerAServePointsSurface[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAServePointsWonSurface[Opp] += (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45])
                    PlayerAReturnPointsSurface[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAReturnPointsWonSurface[Opp] += (PrevMatchesCommOpps[match][51] - (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54]))
                else:
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][8])
                    PlayerAServePointsSurface[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAServePointsWonSurface[Opp] += (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54])
                    PlayerAReturnPointsSurface[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAReturnPointsWonSurface[Opp] += (PrevMatchesCommOpps[match][42] - (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45]))
            else:
                if (PrevMatchesCommOpps[match][8] == PlayerA):
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][18])
                    PlayerAServePointsNS[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAServePointsWonNS[Opp] += (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45])
                    PlayerAReturnPointsNS[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAReturnPointsWonNS[Opp] += (PrevMatchesCommOpps[match][51] - (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54]))
                else:
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][8])
                    PlayerAServePointsNS[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAServePointsWonNS[Opp] += (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54])
                    PlayerAReturnPointsNS[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAReturnPointsWonNS[Opp] += (PrevMatchesCommOpps[match][42] - (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45]))
    
    # Remove any common opponents
    # Compute the proportion of service points won against each common opponent:
    SPWCommonOppProps = np.zeros(len(CommonOpps), dtype = float)
    RPWCommonOppProps = np.zeros(len(CommonOpps), dtype = float)
    print(PlayerAServePointsSurface)
    print(PlayerAServePointsNS)
    for Opp in range(len(CommonOpps)):
        SPWCommonOppProps[Opp] = ((1 - Surface) * (PlayerAServePointsWonSurface[Opp] / PlayerAServePointsSurface[Opp]) + Surface * (PlayerAServePointsWonNS[Opp] / PlayerAServePointsNS[Opp]))
        RPWCommonOppProps[Opp] = ((1 - Surface) * (PlayerAReturnPointsWonSurface[Opp] / PlayerAReturnPointsSurface[Opp]) + Surface * (PlayerAReturnPointsWonNS[Opp] / PlayerAReturnPointsNS[Opp]))

    OverallSPWCommOpps = sum(SPWCommonOppProps) / len(CommonOpps)
    OverallRPWCommOpps = sum(RPWCommonOppProps) / len(CommonOpps)
    return [OverallSPWCommOpps, OverallRPWCommOpps]

def main():
    EvalEquation(8)


if __name__ == "__main__":
    main()