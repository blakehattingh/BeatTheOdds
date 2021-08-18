from datetime import datetime, timedelta
from typing import Match
from pandas.core.base import DataError
import os, sys
relativePath = os.path.abspath('')
sys.path.append(relativePath + '\\MarkovModel')
sys.path.append(relativePath + '\\DataExtraction')
from MarkovModel import FirstImplementation
from DataExtraction import TestSetCollector, DataCollector
from BuildingDatabase import *
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

def InterpolateDists(Pa, Pb, DB, Spacing = 0.02):
    # Takes in a set of P values and returns the interpolated distributions for them
    # Grid:
    # A ----E- B
    # |     x  |
    # |        |
    # C ----F- D
    
    # Compute the base point for the 4 points around this point (Point A):
    APointA = round((Pa - (Pa % 0.02)),2)
    APointB = round((Pb - (Pb % 0.02)),2)

    # Extract the distribtions for all 4 corner points:
    ADists = DB[(APointA,APointB)]
    BDists = DB[(round((APointA+0.02),2), APointB)]
    CDists = DB[(APointA, round((APointB+0.02),2))]
    DDists = DB[(round((APointA+0.02),2),round((APointB+0.02),2))]

    # Compute the weighting between side points (alpha) and bottom and top points (beta):
    [alpha, beta] = ComputeWeighting(Pa, Pb)

    # Extract the average distributions along each side:
    XDists = {}
    for dist in ADists:
        EDists = WeightedAverage(ADists[dist], BDists[dist], alpha)
        FDists = WeightedAverage(CDists[dist], DDists[dist], alpha)
        XDists[dist] = WeightedAverage(EDists, FDists, beta)

    return XDists
    
def try_parsing_date(text):
    for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def EvalEquation(age):
    testYears = [2012,2014,2016,2018,2019]
    sampledMatchesByYears = TestSetCollector.getTestMatchData(testYears)
    ageGap = timedelta(days=365.25*age)

    for year in sampledMatchesByYears:
        for match in year:
            dateOfMatch = match[3]
            startOfDataCollection = dateOfMatch - ageGap
            p1vP2,p1vCO,p2vCO,COIds = DataCollector.getSPWData(match, startOfDataCollection)
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

    # Check how many matches are being analysed:
    nonSurfaceMatchesCount = 0
    surfaceMatchesCount = 0

    for match in range(len(PrevMatches)):
        # Check when the match was played:
        # MatchDate = PrevMatches[match][3]

        # Ensure the match has statistics:
        if (PrevMatches[match][42 != None]):

            # if ((Date - MatchDate).days > 0):
            if (PrevMatches[match][4] == Surface):
                surfaceMatchesCount += 1
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
                nonSurfaceMatchesCount += 1
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
    
    print('Number of Previous Matches: ', len(PrevMatches))
    # Check if any matches were analysed:
    if (surfaceMatchesCount > 0):
        # Compute the proportion of service points won on the surface:
        PlayerAServicePropSurface = PlayerAServePointsWonSurface / PlayerAServePointsSurface
        PlayerBServicePropSurface = PlayerBServePointsWonSurface / PlayerBServePointsSurface
    else:
        PlayerAServicePropSurface = 0
        PlayerBServicePropSurface = 0

    if (nonSurfaceMatchesCount > 0):
        PlayerAServicePropNS = PlayerAServePointsWonNS / PlayerAServePointsNS
        PlayerBServicePropNS = PlayerBServePointsWonNS / PlayerBServePointsNS
    else:
        PlayerAServicePropNS = 0
        PlayerBServicePropNS = 0
        
    if ((surfaceMatchesCount > 0) and (nonSurfaceMatchesCount > 0)):
        PlayerAServiceProp = (1 - SurfaceParameter) * PlayerAServicePropSurface + SurfaceParameter * PlayerAServicePropNS
        PlayerBServiceProp = (1 - SurfaceParameter) * PlayerBServicePropSurface + SurfaceParameter * PlayerBServicePropNS
    else:
        PlayerAServiceProp = PlayerAServicePropSurface + PlayerAServicePropNS
        PlayerBServiceProp = PlayerBServicePropSurface + PlayerBServicePropNS

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

    # Check how many matches are being analysed:
    surfaceMatchesCount = np.zeros(len(CommonOpps), dtype = float)
    nonSurfaceMatchesCount = np.zeros(len(CommonOpps), dtype = float)

    for match in range(len(PrevMatchesCommOpps)):
        # Check when the match was played:
        #MatchDate = PrevMatchesCommOpps[match][3]

        # Make sure the match has statistics:
        if (PrevMatchesCommOpps[match][42] != None):

        #if ((Date - MatchDate).days > 0):
            if (Surface == PrevMatchesCommOpps[match][4]):
                if (PrevMatchesCommOpps[match][8] == PlayerA):
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][18])
                    PlayerAServePointsSurface[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAServePointsWonSurface[Opp] += (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45])
                    PlayerAReturnPointsSurface[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAReturnPointsWonSurface[Opp] += (PrevMatchesCommOpps[match][51] - (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54]))
                    surfaceMatchesCount[Opp] += 1
                else:
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][8])
                    PlayerAServePointsSurface[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAServePointsWonSurface[Opp] += (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54])
                    PlayerAReturnPointsSurface[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAReturnPointsWonSurface[Opp] += (PrevMatchesCommOpps[match][42] - (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45]))
                    surfaceMatchesCount[Opp] += 1
            else:
                if (PrevMatchesCommOpps[match][8] == PlayerA):
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][18])
                    PlayerAServePointsNS[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAServePointsWonNS[Opp] += (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45])
                    PlayerAReturnPointsNS[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAReturnPointsWonNS[Opp] += (PrevMatchesCommOpps[match][51] - (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54]))
                    nonSurfaceMatchesCount[Opp] += 1
                else:
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][8])
                    PlayerAServePointsNS[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAServePointsWonNS[Opp] += (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54])
                    PlayerAReturnPointsNS[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAReturnPointsWonNS[Opp] += (PrevMatchesCommOpps[match][42] - (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45]))
                    nonSurfaceMatchesCount[Opp] += 1

    # Compute the proportion of service points won against each common opponent:
    SPWCommonOppPropsSurface = np.zeros(len(CommonOpps), dtype = float)
    RPWCommonOppPropsSurface = np.zeros(len(CommonOpps), dtype = float)
    SPWCommonOppPropsNS = np.zeros(len(CommonOpps), dtype = float)
    RPWCommonOppPropsNS = np.zeros(len(CommonOpps), dtype = float)
    SPWCommonOppProps = np.zeros(len(CommonOpps), dtype = float)
    RPWCommonOppProps = np.zeros(len(CommonOpps), dtype = float)
    print('Number of Previous Common Matches: ', len(PrevMatchesCommOpps))

    for Opp in range(len(CommonOpps)):
        # Check if any matches were analysed for this common opponent:
        if (surfaceMatchesCount[Opp] > 0):
            SPWCommonOppPropsSurface[Opp] = PlayerAServePointsWonSurface[Opp] / PlayerAServePointsSurface[Opp]
            RPWCommonOppPropsSurface[Opp] = PlayerAReturnPointsWonSurface[Opp] / PlayerAReturnPointsSurface[Opp]
   
        if (nonSurfaceMatchesCount[Opp] > 0):
            SPWCommonOppPropsNS[Opp] = PlayerAServePointsWonNS[Opp] / PlayerAServePointsNS[Opp]
            RPWCommonOppPropsNS[Opp] = PlayerAReturnPointsWonNS[Opp] / PlayerAReturnPointsNS[Opp]
        
        # Check if the weighting is needed:
        if ((surfaceMatchesCount[Opp] > 0) and (nonSurfaceMatchesCount[Opp] > 0)):
            # Compute overall proportion:
            SPWCommonOppProps[Opp] = ((1 - SurfaceParameter) * (SPWCommonOppPropsSurface[Opp]) + SurfaceParameter * (SPWCommonOppPropsNS[Opp]))
            RPWCommonOppProps[Opp] = ((1 - SurfaceParameter) * (RPWCommonOppPropsSurface[Opp]) + SurfaceParameter * (RPWCommonOppPropsNS[Opp]))
        else:
            SPWCommonOppProps[Opp] = SPWCommonOppPropsSurface[Opp] + SPWCommonOppPropsNS[Opp]
            RPWCommonOppProps[Opp] = RPWCommonOppPropsSurface[Opp] + RPWCommonOppPropsNS[Opp]
    
    OverallSPWCommOpps = sum(SPWCommonOppProps) / len(CommonOpps)
    OverallRPWCommOpps = sum(RPWCommonOppProps) / len(CommonOpps)
    return [OverallSPWCommOpps, OverallRPWCommOpps]
        
def main():
    Age = 8
    EvalEquation(8)
    #DB = ReadInGridDB('ModelDistributions.csv')
    #Dists = InterpolateDists(0.615, 0.605, DB)
    #print(Dists)

if __name__ == "__main__":
    main()