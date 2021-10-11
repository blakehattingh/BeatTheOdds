from datetime import datetime, timedelta
from typing import Match
from pandas.core.base import DataError
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os, sys

from pulp.pulp import FractionElasticSubProblem

from BuildingDatabase import *
from CalculatingP import *

# Add required folders to the system path:
currentPath = os.path.abspath(os.getcwd())

# Markov Model Files:
#sys.path.insert(0, currentPath + '\\BeatTheOdds\\MarkovModel')
sys.path.insert(0, currentPath + '\\MarkovModel')
from FirstImplementation import *


# Optimisation Model Files:
#sys.path.insert(0, currentPath + '\\BeatTheOdds\\OptimisationModel')
sys.path.insert(0, currentPath + '\\OptimisationModel')
from CVaRModel import *

# Data Extraction Files:
#sys.path.insert(0, currentPath + '\\BeatTheOdds\\DataExtraction')
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

def InterpolateDists(Pa, Pb, DB, pBoundaryL = 0.4, pBoundaryH = 0.8, Spacing = 0.02):
    # Takes in a set of P values and returns the interpolated distributions for them
    # Grid:
    # A ----E- B
    # |     x  |
    # |        |
    # C ----F- D
    
    # Ensure Pa and Pb are within bounds of the DB:
    if (Pa < pBoundaryL):
        if (Pb < pBoundaryL):
            ZDists = {}
            for dist in DB[(pBoundaryL,pBoundaryL)]:
                # Convert distributions to arrays:
                pCorner = np.array(DB[(round(pBoundaryL,2),round(pBoundaryL,2))][dist])
                PaNext = np.array(DB[(round(pBoundaryL+Spacing,2),round(pBoundaryL,2))][dist])
                PbNext = np.array(DB[(round(pBoundaryL,2),round(pBoundaryL+Spacing,2))][dist])

                # Extrapolate to this point:
                ZDists[dist] = np.subtract(pCorner, ((pBoundaryL - Pa) * np.subtract(PaNext, pCorner) / Spacing))
                ZDists[dist] = np.subtract(ZDists[dist], ((pBoundaryL - Pb) * np.subtract(PbNext, pCorner) / Spacing))
                
                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists
        else:
            ZDists = {}
            for dist in DB[(pBoundaryL,pBoundaryL)]:
                # Find the points above and below the point:
                roundedB = round(Pb, 1)
                if (roundedB > Pb):
                    roundedB -= 0.1
                while (roundedB <= Pb):
                    PbBefore = round(roundedB,2)
                    roundedB += Spacing

                # Get the two sides: (A before it, B is after it on the edge of our grid)
                pBefore = (round(pBoundaryL,2), round(PbBefore,2))
                pAfter = (round(pBoundaryL,2), round(PbBefore + Spacing,2))

                # Compute gradient between A and B:
                gradPb = (np.subtract(np.array(DB[pAfter][dist]), np.array(DB[pBefore][dist]))) / Spacing

                # Compute gradient to extrapolate out to this point:
                gradPa = (np.subtract(np.array(DB[(round(pBoundaryL + Spacing,2),PbBefore)][dist]),np.array(DB[pBefore][dist]))) / Spacing

                # Extrapolate to this point:
                ZDists[dist] = DB[pBefore][dist] - (pBoundaryL - Pa) * gradPa + (Pb - PbBefore) * gradPb

                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists
    else:
        if (Pb < pBoundaryL):
            ZDists = {}
            for dist in DB[(pBoundaryL,pBoundaryL)]:
                # Find the points above and below the point:
                roundedA = round(Pa, 1)
                if (roundedA > Pa):
                    roundedA -= 0.1
                while (roundedA <= Pa):
                    PaBefore = round(roundedA,2)
                    roundedA += Spacing

                # Get the two sides: (A before it, B is after it on the edge of our grid)
                pBefore = (round(PaBefore,2),round(pBoundaryL,2))
                pAfter = (round(PaBefore + Spacing,2),round(pBoundaryL,2))

                # Compute gradient between A and B:
                gradPa = (np.subtract(np.array(DB[pAfter][dist]), np.array(DB[pBefore][dist]))) / Spacing

                # Compute gradient to extrapolate out to this point:
                gradPb = (np.subtract(np.array(DB[(PaBefore, round(pBoundaryL+Spacing,2))][dist]),np.array(DB[pBefore][dist]))) / Spacing

                # Extrapolate to this point:
                ZDists[dist] = DB[pBefore][dist] - (pBoundaryL - Pb) * gradPb + (Pa - PaBefore) * gradPa

                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists

    if (Pa > pBoundaryH):
        if (Pb > pBoundaryH):
            ZDists = {}
            for dist in DB[(pBoundaryH,pBoundaryH)]:
                # Convert distributions to arrays:
                pCorner = np.array(DB[(round(pBoundaryH,2),round(pBoundaryH,2))][dist])
                PaBefore = np.array(DB[(round(pBoundaryH-Spacing,2),round(pBoundaryH,2))][dist])
                PbBefore = np.array(DB[(round(pBoundaryH,2),round(pBoundaryH-Spacing,2))][dist])

                # Extrapolate to this point:
                ZDists[dist] = np.subtract(pCorner, ((pBoundaryH - Pa) * np.subtract(pCorner, PaBefore) / Spacing))
                ZDists[dist] = np.subtract(ZDists[dist], ((pBoundaryH - Pb) * np.subtract(pCorner, PbBefore) / Spacing))
                
                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists
        else:
            ZDists = {}
            for dist in DB[(pBoundaryH,pBoundaryH)]:
                # Find the points above and below the point:
                roundedB = round(Pb, 1)
                if (roundedB > Pb):
                    roundedB -= 0.1
                while (roundedB <= Pb):
                    PbBefore = round(roundedB,2)
                    roundedB += Spacing

                # Get the two sides: (A before it, B is after it on the edge of our grid)
                pBefore = (round(pBoundaryH,2), round(PbBefore,2))
                pAfter = (round(pBoundaryH,2), round(PbBefore + Spacing,2))

                # Compute gradient between A and B:
                gradPb = (np.subtract(np.array(DB[pAfter][dist]), np.array(DB[pBefore][dist]))) / Spacing

                # Compute gradient to extrapolate out to this point:
                gradPa = (np.subtract(np.array(DB[pBefore][dist]),np.array(DB[(round(pBoundaryH - Spacing,2),PbBefore)][dist]))) / Spacing

                # Extrapolate to this point:
                ZDists[dist] = DB[pBefore][dist] + (Pa - pBoundaryH) * gradPa + (Pb - PbBefore) * gradPb

                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists
    else:
        if (Pb > pBoundaryH):
            ZDists = {}
            for dist in DB[(pBoundaryH,pBoundaryH)]:
                # Find the points above and below the point:
                roundedA = round(Pa, 1)
                if (roundedA > Pa):
                    roundedA -= 0.1
                while (roundedA <= Pa):
                    PaBefore = round(roundedA,2)
                    roundedA += Spacing

                # Get the two sides: (A before it, B is after it on the edge of our grid)
                pBefore = (round(PaBefore,2),round(pBoundaryH,2))
                pAfter = (round(PaBefore + Spacing,2),round(pBoundaryH,2))

                # Compute gradient between A and B:
                gradPa = (np.subtract(np.array(DB[pAfter][dist]), np.array(DB[pBefore][dist]))) / Spacing

                # Compute gradient to extrapolate out to this point:
                gradPb = (np.subtract(np.array(DB[(PaBefore, round(pBoundaryH,2))][dist]),np.array(DB[(PaBefore,round(pBoundaryH-Spacing,2))][dist]))) / Spacing

                # Extrapolate to this point:
                ZDists[dist] = DB[pBefore][dist] + (Pb - pBoundaryH) * gradPb + (Pa - PaBefore) * gradPa

                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists

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
    for fmt in (' %d/%m/%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d'):
        try:
            return [datetime.strptime(text, fmt), fmt]
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def EvalEquations(testDataFN, obj, equations, age, surface, weighting, riskProfile, alphas, betas, theta = 0.5):
    # This function takes a test or training set of matches, an equation(s) to use and it evaluates the specified 
    # objective metric across the inputted data set.
    # Inputs:
    # - testDataFN = A csv filename for the test/training set of matches
    # - obj = the objective metric to use (either 'Match Stats' or 'ROI')
    # - equations = a list of integer(s) corresponding to the equations to use
    # - age, surface, weighting, theta are hyperparameters for the equations
    # - riskProfile = the risk profile used
    # - alphas = a list of RHS values for the profile getting used
    # - betas = a list of beta values to use in the CVaR model

    # Returns:
    # - The objective metric for the equations given on the data inputted

    # Read in the model distributions:
    DB = ReadInGridDB('ModelDistributions2.csv')

    # Read in the data:
    testData = ReadInData(testDataFN)
    ageGap = timedelta(days=365.25*age)

    # Create a dictionary to store the objective metric(s):
    objectiveValues = {}
    if (obj == 'Match Stats'):
        for eq in equations:
            objectiveValues['Equation {}'.format(eq)] = {'Match Outcome': 0, 'Match Score': 0, 'Set Score': 0, 
            'Matches Predicted': 0}        
    elif (obj == 'ROI'):
        for eq in equations:
            objectiveValues['Equation {}'.format(eq)] = {'ROI': [], 'Betted': 0, 'Returns': 0, 'Matches Predicted': 0}

    # Using the equations specified, compute the objective metric specified for each match in test data:
    for match in testData:
        # Extract the test match data:
        dateOfMatch = datetime.strptime(match[3], '%d/%m/%Y')
        matchScore = [int(match[30]),int(match[31])]
        SetScores = ExtractSetScores(match[28])
        outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))
        startOfDataCollection = dateOfMatch - ageGap

        # Collect player data for the players in the match:
        p1vP2,p1vCO,p2vCO,COIds = getSPWData(match, startOfDataCollection)

        # Compute the P values using the equations specified:
        for eq in equations:
            # Compute the P values for the two players:
            [Pa,Pb,predict] = CalcPEquation(eq, surface, weighting, match, p1vP2, p1vCO, p2vCO, COIds, theta)

            # Look to make predictions using these P values:
            if (predict):
                # Interpolate the distributions for these P values:
                Dists = InterpolateDists(Pa, Pb, DB, pBoundaryL = 0.5, pBoundaryH = 0.9)

                # Compute the objective metrics for this match:
                if (obj == 'Match Stats'):
                    objectiveValues['Equation {}'.format(eq)]['Match Outcome'] += ObjectiveMetricMatchOutcome(Dists['Match Outcome'], 1)
                    objectiveValues['Equation {}'.format(eq)]['Match Score'] += ObjectiveMetricMatchScore(Dists['Match Score'], matchScore)
                    objectiveValues['Equation {}'.format(eq)]['Set Score'] += ObjectiveMetricSetScore(Dists['Set Score'], SetScores)
                    objectiveValues['Equation {}'.format(eq)]['Matches Predicted'] += 1
                elif (obj == 'ROI'):
                    # Extract the odds for the bets we are considering: (change to inputs to function?)
                    betsConsidered = [1,1,1,0,0]
                    oddsMO = [float(match[58]),float(match[59])]
                    oddsMS = [float(match[63]),float(match[62]),float(match[60]),float(match[61])]
                    oddsNumSets = [float(match[65]),float(match[64])]

                    # Find the best set of bets to make:
                    [Zk, suggestedBets, objVal, minRegret] = RunCVaRModel(betsConsidered,Dists['Match Score'],riskProfile,alphas,betas,oddsMO,
                    oddsMS,oddsNumSets,oddsSS=[],oddsNumGames=[])

                    # Place these bets and compute the ROI:
                    [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
                    objectiveValues['Equation {}'.format(eq)]['ROI'].append(ROI)
                    objectiveValues['Equation {}'.format(eq)]['Betted'] += spent
                    objectiveValues['Equation {}'.format(eq)]['Returns'] += returns
                    objectiveValues['Equation {}'.format(eq)]['Matches Predicted'] += 1

    return objectiveValues

def CalcPEquation(equation,surface,weighting,MatchData,PrevMatches,PrevMatchesCommA,PrevMatchesCommB,CommonOpps,theta=0.5):
    # This function takes in a match, extracts who is playing, when the match is/was played, and what surface it is/was played on
    # It then computes the P values for both players using method 1 (FOR NOW, can integrate it to use a specified method)
    # Inputs:
    # - equation = What equation we will use to compute P
    # - weighting = A parameter corresponding to the weighting between spw(A,B) and spw(A,C)
    # - surface = A hyperparameter corresponding to the weighting on matches played on the same surface
    # - theta = The additional weighting parameter for equation 3
    # - MatchData = Data on a single match to be predicted on
    # - PrevMatches = The previous matches between the players playing in the match
    # - PrevMatchesCommA / B = The matches between player A / B and the common opponents
    # - CommonOpps = A list of common opponent IDs

    # Returns:
    # - Pa and Pb
    # - Boolean relating to if we can predict or not with the P values

    # Extract required info:
    surfaceOfMatch = MatchData[4]
    PlayerA = int(MatchData[8])
    PlayerB = int(MatchData[18])
   

    # See how many matches have been played between A and B:
    numMatches = len(PrevMatches)

    # Check if we have sufficient historical data to make predictions:
    if (numMatches == 0):
        if (len(CommonOpps) == 0):
            # We have no data to use to compute P, thus do NOT compute it:
            #print('No historical data for these players')
            return [0.5,0.5,False]
        else:
            # Pass a warning message:
            #print('First match between these 2 players')

            # Compute SPW(A,C) and SPW(B,C):
            [spwAC, rpwAC] = ComputeSPWCommon(PlayerA, PrevMatchesCommA, CommonOpps, surface, surfaceOfMatch) 
            [spwBC, rpwBC] = ComputeSPWCommon(PlayerB, PrevMatchesCommB, CommonOpps, surface, surfaceOfMatch)
            #print('spwAC:', spwAC, 'rpwAC:', rpwAC)
            #print('spwBC:', spwBC, 'rpwBC:', rpwBC)

            # Compute PaS and PbS:
            #print('Only using SPC to compute P')
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
                Pa = PaS * (1. - theta) + theta * (1. - PbR)
                Pb = PbS * (1. - theta) + theta * (1. - PaR)
    else:
        if (len(CommonOpps) == 0):
            # No common opponents, but they have played before: (rare occurence)
            # Compute SPW(A,B) and SPW(B, A):
            [spwAB, spwBA] = ComputeSPW(PlayerA, PlayerB, PrevMatches, surface, surfaceOfMatch)
            #print('spwAB:', spwAB, 'spwBA:', spwBA)

            # Compute RPW(A,B) and RPW(B,A)
            rpwAB = 1. - spwBA
            rpwBA = 1. - spwAB       

            # Compute PaS and PbS:
            #print('Only using SPW to compute P')
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
                Pa = PaS * (1. - theta) + theta * (1. - PbR)
                Pb = PbS * (1. - theta) + theta * (1. - PaR)
        else:
            # Compute SPW(A,B) and SPW(B, A):
            [spwAB, spwBA] = ComputeSPW(PlayerA, PlayerB, PrevMatches, surface, surfaceOfMatch)
            #print('spwAB:', spwAB, 'spwBA:', spwBA)

            # Compute RPW(A,B) and RPW(B,A)
            rpwAB = 1. - spwBA
            rpwBA = 1. - spwAB

            # Compute SPW(A,C) and SPW(B,C):
            [spwAC, rpwAC] = ComputeSPWCommon(PlayerA, PrevMatchesCommA, CommonOpps, surface, surfaceOfMatch) 
            [spwBC, rpwBC] = ComputeSPWCommon(PlayerB, PrevMatchesCommB, CommonOpps, surface, surfaceOfMatch)
            #print('spwAC:', spwAC, 'rpwAC:', rpwAC)
            #print('spwBC:', spwBC, 'rpwBC:', rpwBC)

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
        
    #print('Pa:', Pa, 'Pb:', Pb)
    return [Pa, Pb, True]

def ComputeSPW(PlayerA, PlayerB, PrevMatches, surface, surfaceOfMatch):
    # Inputs:
    # - surface = A hyperparameter corresponding to the weighting on matches played on the same surface
    # - PlayerA & PlayerB = IDs of both players of interest 
    # - PrevMatches = A list of tuples of all previous matches between player A and player B
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
        # Ensure the match has statistics:
        if (PrevMatches[match][42] != None):
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
    
    #print('Number of Previous Matches: ', len(PrevMatches))
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

def ComputeSPWCommon(PlayerA, PrevMatchesCommOpps, CommonOpps, surface, surfaceOfMatch):    
    # Inputs:
    # - PlayerA = ID of both player A
    # - PrevMatchesCommOpps = A list of tuples of all previous matches between player A the common opponents
    # - CommonOpps = A list of the IDs of all common opponents
    # - surface = A hyperparameter corresponding to the weighting on matches played on the same surface
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
        # Make sure the match has statistics:
        if (PrevMatchesCommOpps[match][42] != None):
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
    #print('Number of Previous Common Matches: ', len(PrevMatchesCommOpps))

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

def ReadInData(fileName):
    # Get location of file:
    THIS_FOLDER = os.path.abspath('CSVFiles')
    fileName = os.path.join(THIS_FOLDER, fileName)
    #folder = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\'
    #fileName = os.path.join(folder, fileName)
    # Read in CSV file:
    testData = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                testData.append(row)
                line_count += 1
    
    return testData

def test25Matches(DB, matchesFileName):
    # Test the ROI as an objective on a small test manually gathered.
    # Test multiple matches that I have collected odds data and their Pa and Pb values for.

    # Plots:
    # 1) ROI vs A single alpha value changing for 3 generic risk profiles
    #       - 3 plots, one for each alpha value
    # 2) Distribution of the Payoff and Amount betted for each generic risk profile
    #       - 2 distribution plots per risk profile

    plot1 = True
    plot2 = False

    # Save figures to:
    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'

    # Read in the matches, odds, and respective Pa and Pb values:
    matches = ReadInData(matchesFileName)
    
    # Iterate through the matches we have data for:
    if (plot1):
        overallROIs = {}
        overallROIs['Risk-Averse'] = {}
        overallROIs['Risk-Neutral'] = {}
        overallROIs['Risk-Seeking'] = {}
        overallROIs['Risk-Averse']['Spent'] = []
        overallROIs['Risk-Averse']['Returns'] = []
        overallROIs['Risk-Averse']['Overall ROI'] = []
        overallROIs['Risk-Neutral']['Spent'] = []
        overallROIs['Risk-Neutral']['Returns'] = []
        overallROIs['Risk-Neutral']['Overall ROI'] = []
        overallROIs['Risk-Seeking']['Spent'] = []
        overallROIs['Risk-Seeking']['Returns'] = []
        overallROIs['Risk-Seeking']['Overall ROI'] = []
    
    if (plot2):
        amountBetted = {}
        amountBetted['Risk-Averse'] = []
        amountBetted['Risk-Neutral'] = []
        amountBetted['Risk-Seeking'] = []
        payOffs = {}
        payOffs['Risk-Averse'] = []
        payOffs['Risk-Neutral'] = []
        payOffs['Risk-Seeking'] = []

    # Construct varying possible risk profiles:
    betsConsidered = [1,1,1,0,0]
    betas = [0.2, 1./3., 0.5]
    odds = {}
    riskProfiles = {'Risk-Averse': [0.5, 1./3., 0.2], 'Risk-Neutral': [0.75, 0.5, 0.3], 'Risk-Seeking': [1., 2./3., 0.5]}
    N = 30
    alphaValues_1 = {'Risk-Averse':np.linspace(1./3.,1.,N),'Risk-Neutral':np.linspace(0.5,1.,N),
        'Risk-Seeking':np.linspace(2./3.,1.,N)}
    alphaValues_2 = {'Risk-Averse':np.linspace(0.2,0.5,N),'Risk-Neutral':np.linspace(0.3,0.75,N),
        'Risk-Seeking':np.linspace(0.5,1.,N)}
    alphaValues_3 = {'Risk-Averse':np.linspace(0.1,1./3.,N),'Risk-Neutral':np.linspace(0.1,0.5,N),
        'Risk-Seeking':np.linspace(0.1,2./3.,N)}

    # Find the best bets to place:
    for profile in riskProfiles:

        # Produce the plot of ROI vs Changing Alpha Values:
        if (plot1):
            # Iterate through possible alpha_3 values:
            for alpha in alphaValues_1[profile]:
                # Update the alpha values:
                riskProfiles[profile][0] = alpha
                amountSpent = 0.
                amountReturned = 0.

                # Run the model on all matches in the data set:
                for match in matches:
                    # Compute the interpolated distributions:
                    Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

                    # Extract the required match details:
                    winner = 1
                    matchScore = [float(match[10]), float(match[11])]
                    setScores = ExtractSetScores(match[8])
                    outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

                    # Run CVaR model: (using generic risk profile)
                    [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],riskProfiles[profile],
                    betas,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
                    float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])

                    # "place" these bets and the computed the ROI:
                    [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
                    amountSpent += spent
                    amountReturned += returns
                
                # Compute the average ROI for this profile and alpha values:
                overallROIs[profile]['Overall ROI'].append(((amountReturned - amountSpent) / amountSpent) * 100.)
        
        # Produce the Distribution of Amount Betted and Payoff for each Generic Risk Profile:
        if (plot2):

            # Run the model on all matches in the data set:
            for match in matches:
                # Compute the interpolated distributions:
                Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

                # Extract the required match details:
                winner = 1
                matchScore = [float(match[10]), float(match[11])]
                setScores = ExtractSetScores(match[8])
                outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

                # Run CVaR model:
                [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],riskProfiles[profile],
                betas,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
                float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])

                # "place" these bets and the computed the ROI:
                [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
                amountBetted[profile].append(spent)
                payOffs[profile].append(returns - spent)

    if (plot1):
        # Create a plot of the 3 sequences of ROIs:
        for profile in overallROIs:
            plt.plot(alphaValues_1[profile], overallROIs[profile]['Overall ROI'], label = profile)
        plt.xlabel('Alpha 1 - Proportion willing to lose in the worst 20% of cases')
        plt.ylabel('Overall ROI as a Percentage')
        plt.legend()
        #plt.show()
        plt.savefig(plotsFolder+'ROIvsAlpha{} Over 25 Matches'.format(1))
        plt.clf()
    
    if (plot2):
        # Create distribution plots:
        # Amount Betted:
        plt.hist([amountBetted['Risk-Averse'],amountBetted['Risk-Neutral'],amountBetted['Risk-Seeking']], 
        color=['blue','green','red'],edgecolor='black',label=['Risk-Averse','Risk-Neutral','Risk-Seeking'],bins = 4)
        plt.legend()
        plt.xlabel('Amount Betted (as a proportion of your budget)')
        plt.ylabel('Frequency over the 25 Matches')
        # plt.show()
        plt.savefig(plotsFolder+'DistributionAmountBetted.png')
        plt.clf()

        # PayOffs:
        plt.hist([payOffs['Risk-Averse'],payOffs['Risk-Neutral'],payOffs['Risk-Seeking']], 
        color=['blue','green','red'],edgecolor='black',label=['Risk-Averse','Risk-Neutral','Risk-Seeking'],bins = 4)
        plt.legend()
        plt.xlabel('Payoff (irrespective of the amount betted)')
        plt.ylabel('Frequency over the 25 Matches')
        # plt.show()
        plt.savefig(plotsFolder+'DistributionPayOff.png')

def test1Match(DB, matchesFileName):
    # Test the ROI on just a sinlge match for plotting purposes.
    # Plots:
    # 1) ROI vs A single alpha value changing for 3 generic risk profiles
    #       - 3 plots, one for each alpha value
    # 2) Suggested Bets made vs a single changing alpha value for 3 generic risk profiles

    # Save figures to:
    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'

    plot1 = False
    plot2 = True

    # Set up required data storing structures:
    ROIs = {}
    ROIs['Risk-Averse'] = []
    ROIs['Risk-Neutral'] = []
    ROIs['Risk-Seeking'] = []
    allROIs = {}

    # Add the beta keys to all the required dictionarys:
    betas = ['20%','33%','50%']
    betsMade = {}
    bets = {}
    betsToPlot = {}
    for beta in betas:
        # Plot 1:
        allROIs[beta] = {}

        # For plot 2:
        betsMade[beta] = {}
        bets[beta] = {}
        betsToPlot[beta] = {}

        for profile in ROIs:
            betsMade[beta][profile] = {}
            bets[beta][profile] = {}
            betsToPlot[beta][profile] = {}

    # Read in data and extract ONLY the first match:
    match = ReadInData(matchesFileName)[0]

    # Construct varying possible risk profiles:
    betsConsidered = [1,1,1,0,0]
    betas = [0.2, 1./3., 0.5]
    odds = {}
    riskProfiles = {'Risk-Averse': {'20%': 0.5, '33%': 1./3., '50%': 0.2}, 'Risk-Neutral': {'20%': 0.75, '33%': 0.5,
    '50%': 0.3}, 'Risk-Seeking': {'20%': 1., '33%': 2./3., '50%': 0.5}}
    N = 30
    alphaValues = {}
    alphaValues['20%'] = {'Risk-Averse':np.linspace(1./3.,1.,N),'Risk-Neutral':np.linspace(0.5,1.,N),
        'Risk-Seeking':np.linspace(2./3.,1.,N)}
    alphaValues['33%'] = {'Risk-Averse':np.linspace(0.2,0.5,N),'Risk-Neutral':np.linspace(0.3,0.75,N),
        'Risk-Seeking':np.linspace(0.5,1.,N)}
    alphaValues['50%'] = {'Risk-Averse':np.linspace(0.1,1./3.,N),'Risk-Neutral':np.linspace(0.1,0.5,N),
        'Risk-Seeking':np.linspace(0.1,2./3.,N)}

    # Compute the interpolated distributions:
    Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

    # Extract the required match details:
    winner = 1
    matchScore = [float(match[10]), float(match[11])]
    setScores = ExtractSetScores(match[8])
    outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

    # Find the best bets to place:
    for profile in riskProfiles:
        # Iteratre through the different alpha values we can change:
        counter = 0
        for beta in allROIs:
            ROIs[profile] = []

            # Iterate through possible alpha values:
            for alpha in alphaValues[beta][profile]:
                # Set up the other 2 alpha values:
                alphasToUse = []
                for value in riskProfiles[profile]:
                    if (value == beta):
                        alphasToUse.append(alpha)
                    else:
                        alphasToUse.append(riskProfiles[profile][value])

                # Run CVaR model:
                [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],alphasToUse,
                betas,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
                float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])
                
                # Alpha Values used:
                alphaVals = '{}, {}, {}'.format(round(alphasToUse[0],3), round(alphasToUse[1],3), 
                round(alphasToUse[2],3))

                # Store the bets made for this set of alpha values:
                betsMade[beta][profile][alphaVals] = suggestedBets

                # "place" these bets and the computed the ROI:
                [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)

                # Append it to the ROIS dictionary for this profile:
                ROIs[profile].append(ROI)
            
            # Add to the overall dictionary of ROIs and amount betted:
            allROIs[beta][profile] = ROIs[profile]
            counter += 1

    if (plot1):
        # Create a plot of the 3 sequences of ROIs:
        fig, axes = plt.subplots(1, 3,sharey=True, figsize = [20, 12])
        fig.suptitle('ROI as the Users Risk Profile Changes', fontsize = 25)
        counter = 0
        for beta in allROIs:
            for profile in ROIs:
                axes[counter].plot(alphaValues[beta][profile], allROIs[beta][profile], label = profile)
        
            # Set subplot labels:
            axes[counter].set_title('{} Quantile'.format(beta))
            axes[counter].set_xlabel('User Response for the {} Quantile'.format(beta))
            axes[counter].set_ylabel('ROI as a Percentage')
            axes[counter].legend(['Risk-Averse','Risk-Neutral','Risk-Seeking'])
            counter += 1
            
        plt.savefig(plotsFolder+'ROIvsRiskProfile - All Profiles')
        plt.clf()

    if (plot2):
        # Keep track of the betting options that were considered by each profile for this match:
        tol = 1e-06
        for beta in betsMade:
            for profile in betsMade[beta]:
                for bet in suggestedBets:
                    # Initially Set to zero:
                    bets[beta][profile][bet] = 0.
                    for alphas in betsMade[beta][profile]:
                        # Sum up the amount betted on this specific bet over the changing alpha values:
                        bets[beta][profile][bet] += betsMade[beta][profile][alphas][bet]

        # Check which ones were actually considered:
        for beta in bets:
            for profile in bets[beta]:
                for bet in bets[beta][profile]:
                    if (bets[beta][profile][bet] > tol):
                        # Record these values for plotting:
                        betsToPlot[beta][profile][bet] = []
                        for alphas in betsMade[beta][profile]:
                            betsToPlot[beta][profile][bet].append(betsMade[beta][profile][alphas][bet])

        # Plot the bets:
        fig, axes = plt.subplots(3, 3,sharey=True, figsize = [12, 15])
        fig.suptitle('Amount Betted on Various Bets as the Users Risk Profile Changes', fontsize = 20)

        # Set up figure labels:
        fig.supxlabel('Response the Beta Quantile')
        fig.supylabel('The Generic Risk Profile Used')
        cols = ['{} Quantile Response'.format(round(beta,2)) for beta in betas]
        rows = ['{}'.format(profile) for profile in riskProfiles]
        for ax, col in zip(axes[0], cols):
            ax.set_title(col)
        for ax, row in zip(axes[:,0], rows):
            ax.set_ylabel(row, rotation=90, size='large')

        # Plot the various lines:
        counter2 = 0
        for beta in betsToPlot:
            counter1 = 0
            for profile in betsToPlot[beta]:
                labels = []
                for plot in betsToPlot[beta][profile]:
                    axes[counter1, counter2].plot(alphaValues[beta][profile], betsToPlot[beta][profile][plot])
                    labels.append(plot)

                # Set subplot labels:
                #axes[counter1,counter2].legend(labels, loc = "upper left")
                counter1 += 1
            counter2 += 1

        fig.legend(labels, loc = (0.8,0.77))
        plt.savefig(plotsFolder+'AmountBetted - All Risk Profiles')
        plt.clf()

def main():
    #outcome = '2-0'
    #zk = {'2-0':{'bet 1':2.2,'bet 2': 0.,'bet 3': 1.6,'bet 4': 0.}, '2-1':{'bet 1':2.2,'bet 2': 0.,'bet 3': 0.,'bet 4': 1.8},
    #'0-2':{'bet 1':0.,'bet 2':1.8,'bet 3': 1.6,'bet 4': 0.},'1-2':{'bet 1':0.,'bet 2':1.8,'bet 3':0.,'bet 4':1.8}}
    #bets = {'bet 1':2.5,'bet 2': 3.2,'bet 3': 0.,'bet 4': 1.2} 
    #print(ObjectiveMetricROI(outcome, zk, bets))
    
    # Test for CVaR Model:
    DB = ReadInGridDB('ModelDistributions2.csv')
    test1Match(DB, '2018_19MatchesWithOdds.csv')

if __name__ == "__main__":
    main()