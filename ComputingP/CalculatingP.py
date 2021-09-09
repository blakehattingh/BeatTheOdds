from datetime import datetime, timedelta
from typing import Match
from pandas.core.base import DataError
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os, sys

from BuildingDatabase import *
from CalculatingP import *

# Add required folders to the system path:
currentPath = os.path.abspath(os.getcwd()) + '\\BeatTheOdds'

# Markov Model Files:
sys.path.insert(0, currentPath + '\\MarkovModel')
from FirstImplementation import *

# Optimisation Model Files:
sys.path.insert(0, currentPath + '\\OptimisationModel')
#from CVaRModel import RunCVaRModel

# Data Extraction Files:
sys.path.insert(0, currentPath + '\\DataExtraction')
from TestSetCollector import *
from DataCollector import *

def ObjectiveMetricMatchOutcome(MatchDist, Winner):
    # See who the Markov Model (MM) has as winner:
    if (MatchDist[0] > 0.5):
        MMWinner = 1
    else:
        MMWinner = 2
    
    # Compare it with the actual winner:
    if (MMWinner == Winner):
        Obj = 1
    else:
        Obj = 0
    return Obj

def ObjectiveMetricSetScore(AllSetScoreDist, SetScores):
    # Make sure AllSetScoreDist is a list:
    AllSetScoreDist = AllSetScoreDist.tolist()

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

def ObjectiveMetricMatchScore(MatchScoreDist, MatchScore):
    # Make sure MatchScoreDist is a list:
    MatchScoreDist = MatchScoreDist.tolist()

    # Possible Match scores:
    Scores = [[2,0],[2,1],[0,2],[1,2]]

    # See which match score the Markov Model has most likely:
    Ind = MatchScoreDist.index(max(MatchScoreDist))

    # See if it matches with the actual result:
    if (Scores[Ind] == MatchScore):
        Obj = 1
    else:
        Obj = 0
    return Obj

def ObjectiveMetricROI(outcome, Zk, bets):
    # This function takes an outcome, payoff matrix and bets to take and computes the ROI 
    ROI = 0
    for k in Zk:
        if (k == outcome):
            for bet in Zk[k]:
                ROI += bets[bet] * Zk[k][bet]
            if (sum(bets.values())  == 0):
                ROI = 0.
                spent = 0.
                returns = 0.
            else:
                spent = sum(bets.values())
                returns = ROI
                ROI = ((returns - spent)/spent) * 100.
    return [ROI, spent, returns]

def InterpolateDists(Pa, Pb, DB, Spacing = 0.02):
    # Takes in a set of P values and returns the interpolated distributions for them
    # Grid:
    # A ----E- B
    # |     x  |
    # |        |
    # C ----F- D
    
    # Ensure Pa and Pb are within bounds of the DB:
    if (Pa < 0.5):
        Pa = 0.5
    if (Pb < 0.5):
        Pb = 0.5

    # Compute the base point for the 4 points around this point (Point A):
    roundedA = round(Pa, 1)
    roundedB = round(Pb, 1)
    if (roundedA > Pa):
        roundedA -= 0.1
    if (roundedB > Pb):
        roundedB -= 0.1
    while (roundedA <= Pa):
            APointA = roundedA
            roundedA += Spacing
    while (roundedB <= Pb):
        APointB = roundedB
        roundedB += Spacing
    APointA = round(APointA,2)
    APointB = round(APointB,2)

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

def EvalEquations(DB, testData, equation, age, surface, weighting, theta = (1.-0.7256202149724478)):
    # Create the set of test matches:
    testYears = [2012,2014,2016,2018,2019]
    # sampledMatchesByYears = TestSetCollector.getTestMatchData(testYears)
    sampledMatchesByYears = testData
    ageGap = timedelta(days=365.25*age)
    matchesForTest = []

    # Create dictionary to store the objective metrics for each equation:
    objectiveValues = {'Equation 1': {'Match Outcome': 0, 'Match Score': 0, 'Set Score': 0}, 'Equation 2': {'Match Outcome': 0, 
    'Match Score': 0, 'Set Score': 0}, 'Equation 3': {'Match Outcome': 0, 'Match Score': 0, 'Set Score': 0}}
    count = 0
    for year in sampledMatchesByYears:
        for match in year:
            # Extract the test match data:
            dateOfMatch = match[3]
            MatchScore = [match[30],match[31]]
            SetScores = ExtractSetScores(match[28])
            startOfDataCollection = dateOfMatch - ageGap

            # Collect player data for the players in the match:
            p1vP2,p1vCO,p2vCO,COIds = getSPWData(match, startOfDataCollection)

            # Compute the P values using all 3 equations:
            eqNum = 0
            for eq in objectiveValues:
                eqNum += 1
                print('equation number = ' + str(eqNum))
                # Compute the P values for the two players:
                [Pa,Pb,predict] = CalcPEquation(eqNum, age, surface, weighting, match, p1vP2, p1vCO, p2vCO, COIds, theta)

                # Look to make predictions using these P values:
                if (predict):
                    count += 1
                    # Interpolate the distributions for these P values:
                    Dists = InterpolateDists(Pa, Pb, DB)

                    # Compute the objective metrics for this match:
                    objectiveValues[eq]['Match Outcome'] += ObjectiveMetricMatchOutcome(Dists['Match Outcome'], 1)
                    objectiveValues[eq]['Match Score'] += ObjectiveMetricMatchScore(Dists['Match Score'], MatchScore)
                    objectiveValues[eq]['Set Score'] += ObjectiveMetricSetScore(Dists['Set Score'], SetScores)
    
    # Compute metrics per match:
    for eq in objectiveValues:
        for metric in objectiveValues[eq]:
            objectiveValues[eq][metric] =  objectiveValues[eq][metric] / count

    return objectiveValues

def CalcPEquation(equation,age,surface,weighting,MatchData,PrevMatches,PrevMatchesCommA,PrevMatchesCommB,CommonOpps,theta=0.5):
    # This function takes in a match, extracts who is playing, when the match is/was played, and what surface it is/was played on
    # It then computes the P values for both players using method 1 (FOR NOW, can integrate it to use a specified method)
    # Inputs:
    # - equation = What equation we will use to compute P
    # - age = Alpha hyperparameter
    # - weighting = A parameter corresponding to the weighting between spw(A,B) and spw(A,C)
    # - surface = A hyperparameter corresponding to the weighting on matches played on the same surface
    # - theta = The additional weighting parameter for equation 3
    # - MatchData = Data on a single match to be predicted on
    # - PrevMatches = The previous matches between the players playing in the match
    # - PrevMatchesCommA / B = The matches between player A / B and the common opponents
    # - CommonOpps = A list of common opponent IDs

    # Extract required info:
    dateOfMatch = MatchData[3]
    surfaceOfMatch = MatchData[4]
    PlayerA = MatchData[8]
    PlayerB = MatchData[18]
    SetScores = MatchData[28]
    AwonSets = MatchData[30]
    BwonSets = MatchData[31]
    AwonGames = MatchData[32]
    BwonGames = MatchData[32]

    # See how many matches have been played between A and B:
    numMatches = len(PrevMatches)

    # Check if we have sufficient historical data to make predictions:
    if (numMatches == 0):
        SPW = False
    else:
        SPW = True
    
    if (len(CommonOpps) == 0):
        SPC = False
    else:
        SPC = True

    # Compute the P values using Equation 1, given the historical data:
    if (SPW and SPC):
        # Compute SPW(A,B) and SPW(B, A):
        [spwAB, spwBA] = ComputeSPW(PlayerA, PlayerB, PrevMatches, surface, dateOfMatch, surfaceOfMatch)
        print('spwAB:', spwAB, 'spwBA:', spwBA)

        # Compute RPW(A,B) and RPW(B,A)
        rpwAB = 1. - spwBA
        rpwBA = 1. - spwAB

        # Compute SPW(A,C) and SPW(B,C):
        [spwAC, rpwAC] = ComputeSPWCommon(PlayerA, PrevMatchesCommA, CommonOpps, surface, dateOfMatch, surfaceOfMatch) 
        [spwBC, rpwBC] = ComputeSPWCommon(PlayerB, PrevMatchesCommB, CommonOpps, surface, dateOfMatch, surfaceOfMatch)
        print('spwAC:', spwAC, 'rpwAC:', rpwAC)
        print('spwBC:', spwBC, 'rpwBC:', rpwBC)

        # Compute PaS and PbS:
        PaS = (1  - weighting) * spwAB + weighting * spwAC
        PbS = (1  - weighting) * spwBA + weighting * spwBC

        # Compute PaR and PbR:
        PaR = (1  - weighting) * rpwAB + weighting * rpwAC
        PbR = (1  - weighting) * rpwBA + weighting * rpwBC

        # Compute P using the equation specified:
        if (equation == 1):
            Pa = PaS
            Pb = PbS
        elif (equation == 2):
            Pa = PaS / (PaS + PbR)
            Pb = PbS / (PbS + PaR)
        else:
            Pa = PaS * (1. - theta) + theta * (1. - PbR)
            Pb = PbS * (1. - theta) + theta * (1. - PaR)

    elif (SPW and not SPC):
        # Compute SPW(A,B) and SPW(B, A):
        [spwAB, spwBA] = ComputeSPW(PlayerA, PlayerB, PrevMatches, surface, dateOfMatch, surfaceOfMatch)
        print('spwAB:', spwAB, 'spwBA:', spwBA)

        # Compute RPW(A,B) and RPW(B,A)
        rpwAB = 1. - spwBA
        rpwBA = 1. - spwAB       

        # Compute PaS and PbS:
        print('Only using SPW to compute P')
        PaS = spwAB
        PbS = spwBA

        # Compute PaR and PbR:
        PaR = rpwAB
        PbR = rpwBA

        # Compute P using the equation specified:
        if (equation == 1):
            Pa = PaS
            Pb = PbS
        elif (equation == 2):
            Pa = PaS / (PaS + PbR)
            Pb = PbS / (PbS + PaR)
        else:
            Pa = PaS * (1. - theta) - theta * (1. - PbR)
            Pb = PbS * (1. - theta) - theta * (1. - PaR)

    elif (SPC and not SPW):
        # Compute SPW(A,C) and SPW(B,C):
        [spwAC, rpwAC] = ComputeSPWCommon(PlayerA, PrevMatchesCommA, CommonOpps, surface, dateOfMatch, surfaceOfMatch) 
        [spwBC, rpwBC] = ComputeSPWCommon(PlayerB, PrevMatchesCommB, CommonOpps, surface, dateOfMatch, surfaceOfMatch)
        print('spwAC:', spwAC, 'rpwAC:', rpwAC)
        print('spwBC:', spwBC, 'rpwBC:', rpwBC)

        # Compute PaS and PbS:
        print('Only using SPC to compute P')
        PaS = spwAC
        PbS = spwBC

        # Compute PaR and PbR:
        PaR = rpwAC
        PbR = rpwBC

        # Compute P using the equation specified:
        if (equation == 1):
            Pa = PaS
            Pb = PbS
        elif (equation == 2):
            Pa = PaS / (PaS + PbR)
            Pb = PbS / (PbS + PaR)
        else:
            Pa = PaS * (1. - theta) - theta * (1. - PbR)
            Pb = PbS * (1. - theta) - theta * (1. - PaR)
    
    else:
        # No data on this match up, thus we cannot estimate a Pa and Pb value:
        print('No historical data for these players')
        return [0.5,0.5,False]

    print('Pa:', Pa, 'Pb:', Pb)
    return [Pa, Pb, True]

def ComputeSPW(PlayerA, PlayerB, PrevMatches, surface, dateOfMatch, surfaceOfMatch):
    # Inputs:
    # - surface = A hyperparameter corresponding to the weighting on matches played on the same surface
    # - PlayerA & PlayerB = IDs of both players of interest 
    # - PrevMatches = A list of tuples of all previous matches between player A and player B
    # - dateOfMatch = The date of the match as a string in format '%Y-%m-%d'
    # - surfaceOfMatch = The surface that the match will be played on (as an abbrev, e.g. C = Clay)

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
            if (PrevMatches[match][4] == surfaceOfMatch):
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
        PlayerAServiceProp = (1 - surface) * PlayerAServicePropSurface + surface * PlayerAServicePropNS
        PlayerBServiceProp = (1 - surface) * PlayerBServicePropSurface + surface * PlayerBServicePropNS
    else:
        PlayerAServiceProp = PlayerAServicePropSurface + PlayerAServicePropNS
        PlayerBServiceProp = PlayerBServicePropSurface + PlayerBServicePropNS

    return PlayerAServiceProp, PlayerBServiceProp

def ComputeSPWCommon(PlayerA, PrevMatchesCommOpps, CommonOpps, surface, dateOfMatch, surfaceOfMatch):    
    # Inputs:
    # - PlayerA = ID of both player A
    # - PrevMatchesCommOpps = A list of tuples of all previous matches between player A the common opponents
    # - CommonOpps = A list of the IDs of all common opponents
    # - surface = A hyperparameter corresponding to the weighting on matches played on the same surface
    # - dateOfMatch = The date of the match as a string in format '%Y-%m-%d'
    # - surfaceOfMatch = The surface that the match will be played on (as an abbrev, e.g. C = Clay)

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
            if (surfaceOfMatch == PrevMatchesCommOpps[match][4]):
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
            SPWCommonOppProps[Opp] = ((1 - surface) * (SPWCommonOppPropsSurface[Opp]) + surface * (SPWCommonOppPropsNS[Opp]))
            RPWCommonOppProps[Opp] = ((1 - surface) * (RPWCommonOppPropsSurface[Opp]) + surface * (RPWCommonOppPropsNS[Opp]))
        else:
            SPWCommonOppProps[Opp] = SPWCommonOppPropsSurface[Opp] + SPWCommonOppPropsNS[Opp]
            RPWCommonOppProps[Opp] = RPWCommonOppPropsSurface[Opp] + RPWCommonOppPropsNS[Opp]
    
    OverallSPWCommOpps = sum(SPWCommonOppProps) / len(CommonOpps)
    OverallRPWCommOpps = sum(RPWCommonOppProps) / len(CommonOpps)
    return [OverallSPWCommOpps, OverallRPWCommOpps]
        
def ExtractSetScores(setScoresStirng):
    # Extract individual set scores:
    setScores = setScoresStirng.split()

    # Convert to a 2-element list -> [PlayerAGames, PlayerBGames]
    # 3 Cases:
    # 1) Normal set e.g. 6-3
    # 2) Game reached a TB e.g. 7-6(5)
    # 3) Game reached a superTB (last set of the match) e.g. 12-10

    extractedSS = []
    for set in setScores:
        # Split up A and B's games:
        [gamesA, gamesB] = set.split("-")

        # Check for case 2:
        if ('(' in gamesB):
            # the '(x)' is always on the right of the game number:
            [gamesB, i] = gamesB.split('(')
        
        # Check for case 3:
        if (int(gamesA) > 7 or int(gamesB) > 7):
            # Reduce the score down to 7-6 or 6-7:
            if (gamesA > gamesB):
                extractedSS.append([7,6])
            else:
                extractedSS.append([6,7])
        else:
            extractedSS.append([int(gamesA), int(gamesB)])

    return extractedSS

def test(DB, matchesFileName):
    # Test the ROI as an objective
    FirstTest = False
    ExtensiveTest = True

    # Betting Odds from 'OddsPedia':
    # - These odds are from Bet365 where available, otherwise the average odds are taken
    # - The number of games odds are formatted as follows:
    # - Under/Over 18.5, Under/Over 20.5, Under/Over 22.5, Under/Over 24.5, Under/Over 26.5, Under/Over 28.5

    if (FirstTest):
        # Test Match 1: Andy Murray vs Robin Haase (played 5 times previously)
        # - Match played on 01/03/2021
        # - Match Score: 1-2
        # - Set Scores: 6-2, 6-7, 3-6
        # - Number of Games: 30
        # - P1 = 0.628 and P2 = 0.65
        outcome = '1-2'
        matchScore = [1,2]
        setScores = [[6,2],[6,7],[3,6]]
        NumGames = 30
        P1 = 0.628
        P2 = 0.65
        odds = {'Match Outcome':[2.75,1.44],'Match Score':[4.5,6.0,2.1,4.0],'Number of Sets':[1.51,2.44],'Set Score':[81.0,41.0,15.0,15.0,6.5,
        19.0,9.5,41.0,11.0,10.0,4.33,7.5,13.0,7.5],'Number of Games':[[4.04,1.23],[2.38,1.55],[1.72,2.0],[1.6,2.26],[1.41,2.9],[1.28,3.63]]}
    elif (ExtensiveTest):
        # Test multiple matches that I have collected odds data and their Pa and Pb values for.
        # Read in the matches, odds, and respective Pa and Pb values:
        THIS_FOLDER = os.path.abspath('CSVFiles')
        fileName = os.path.join(THIS_FOLDER, matchesFileName)
        matches = []
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
            line_count = 0
            for row in csv_reader:
                if (line_count > 0):
                    matches.append(row)
                line_count += 1
            
    # Iterate through the matches we have data for:
    objectiveValues = {}
    objectiveValues['Match Outcome'] = []
    objectiveValues['Match Score'] = []
    objectiveValues['Set Score'] = []
    objectiveValues['ROI'] = {}
    objectiveValues['ROI']['Risk-Averse'] = []
    objectiveValues['ROI']['Risk-Neutral'] = []
    objectiveValues['ROI']['Risk-Seeking'] = []
    ROIs = {}    
    ROIs['Risk-Averse'] = []
    ROIs['Risk-Neutral'] = []
    ROIs['Risk-Seeking'] = []
    overallROIs = {}
    overallROIs['Risk-Averse'] = {}
    overallROIs['Risk-Neutral'] = {}
    overallROIs['Risk-Seeking'] = {}
    overallROIs['Risk-Averse']['Spent'] = []
    overallROIs['Risk-Averse']['Returns'] = []
    overallROIs['Risk-Neutral']['Spent'] = []
    overallROIs['Risk-Neutral']['Returns'] = []
    overallROIs['Risk-Seeking']['Spent'] = []
    overallROIs['Risk-Seeking']['Returns'] = []

    # Construct varying possible risk profiles:
    betsConsidered = [1,1,1,0,0]
    betas = [0.2, 1./3., 0.5]
    odds = {}
    riskProfiles = {'Risk-Averse': [0.5, 1./3., 0.2], 'Risk-Neutral': [0.75, 0.5, 0.3], 'Risk-Seeking': [1., 2./3., 0.5]}
    N = 20
    alphaValues_3 = {'Risk-Averse':np.linspace(0.1,1./3.,N),'Risk-Neutral':np.linspace(0.1,0.5,N),
        'Risk-Seeking':np.linspace(0.1,2./3.,N)}

    for match in matches:
        # Compute the interpolated distributions:
        Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

        # Extract the required match details:
        winner = 1
        matchScore = [float(match[10]), float(match[11])]
        setScores = ExtractSetScores(match[8])
        outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

        # Compute the objective metrics for this match:
        objectiveValues['Match Outcome'].append(ObjectiveMetricMatchOutcome(Dists['Match Outcome'], winner))
        objectiveValues['Match Score'].append(ObjectiveMetricMatchScore(Dists['Match Score'], matchScore))
        objectiveValues['Set Score'].append(ObjectiveMetricSetScore(Dists['Set Score'], setScores))

        # Find the best bets to place:
        for profile in riskProfiles:
            # Set up the list to store all the ROI values for each alpha 3:
            allROIs = np.zeros(N, dtype = float)
            allSpent = np.zeros(N, dtype = float)
            allReturns = np.zeros(N, dtype = float) 
            counter = 0

            # Iterate through possible alpha_3 values:
            for alpha_3 in alphaValues_3[profile]:
                riskProfiles[profile][2] = alpha_3
                # Run CVaR model:
                [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],riskProfiles[profile],
                betas,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
                float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])

                # "place" these bets and the computed the ROI:
                [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
                allROIs[counter] = ROI
                allSpent[counter] = spent
                allReturns[counter] = returns
                counter += 1

            # Store it in ROIs:
            ROIs[profile].append(allROIs)
            overallROIs[profile]['Spent'].append(allSpent)
            overallROIs[profile]['Returns'].append(allReturns) 

    # Compute the average ROI for each profile:
    averageOverallROIs = {}
    for profile in objectiveValues['ROI']:
        averageROIs = np.zeros(N, dtype = float)
        averageSpent = np.zeros(N, dtype = float)
        averageReturns = np.zeros(N, dtype = float)
        for alpha in range(N):
            for match in range(len(ROIs[profile])):
                averageROIs[alpha] += ROIs[profile][match][alpha]
                averageSpent[alpha] += overallROIs[profile]['Spent'][match][alpha]
                averageReturns[alpha] += overallROIs[profile]['Returns'][match][alpha]
            averageReturns[alpha] = averageReturns[alpha] - averageSpent[alpha]

        # Divide by number of matches:
        averageROIs = averageROIs / N
        objectiveValues['ROI'][profile] = averageROIs
        averageOverallROIs[profile] = (averageReturns / averageSpent) * 100.

    # Create a plot of the 3 sequences of ROIs:
    for profile in objectiveValues['ROI']:
        plt.plot(alphaValues_3[profile], objectiveValues['ROI'][profile], label = profile)
    plt.xlabel('Alpha 3 - Proportion willing to lose in the worst 50% of cases')
    plt.ylabel('ROI as a percentage')
    plt.legend()
    plt.show()

    for profile in averageOverallROIs:
        plt.plot(alphaValues_3[profile], averageOverallROIs[profile], label = profile)
        plt.xlabel('Alpha 3 - Proportion willing to lose in the worst 50% of cases')
        plt.ylabel('Overall ROI as a percentage')
    plt.legend()
    plt.show()

def main():
    DB = ReadInGridDB('ModelDistributions.csv')
    #test(DB, '2018_19MatchesWithOdds.csv')\
    matches = getSpecificMatches([178827])
    #print(matches)
    surface = [0.2, 0.5, 0.7]
    weighting = [0.2, 0.5, 0.7]
    for surfaceWeight in surface :
        for weight in weighting :
            print('surface = ' + str(surfaceWeight) ) 
            print('weighting = ' + str(weight) )  
            #print(EvalEquations(DB,matches,1,8,surfaceWeight,surfaceWeight))
            EvalEquations(DB,matches,1,8,surfaceWeight,weight)

if __name__ == "__main__":
    main()