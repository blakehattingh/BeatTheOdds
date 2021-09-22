import os
import csv
from datetime import timedelta
from time import strptime
from ModelDistributionsDB import ReadInGridDB
from CalculatingPValues import CalcPEquation
from DataExtractionFromDB import getSPWData
from InterpolatingDistributions import InterpolateDists
from CVaRModel import RunCVaRModel

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

def EvalEquations(testDataFN, obj, equations, age, surface, weighting, theta = 0.5, riskProfile = [], betas = []):
    # This function takes a test or training set of matches, an equation(s) to use and it evaluates the specified 
    # objective metric across the inputted data set.
    # Inputs:
    # - testDataFN = A csv filename for the test/training set of matches
    # - obj = the objective metric to use (either 'Match Stats' or 'ROI')
    # - equations = a list of integer(s) corresponding to the equations to use
    # - age, surface, weighting, theta are hyperparameters for the equations
    # - riskProfiles = a list of RHS values for the profile getting used
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
        dateOfMatch = strptime(match[3], '%d/%m/%Y')
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
                    [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],riskProfile,betas,oddsMO,
                    oddsMS,oddsNumSets,oddsSS=[],oddsNumGames=[])

                    # Place these bets and compute the ROI:
                    [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
                    objectiveValues['Equation {}'.format(eq)]['ROI'].append(ROI)
                    objectiveValues['Equation {}'.format(eq)]['Betted'] += spent
                    objectiveValues['Equation {}'.format(eq)]['Returns'] += returns
                    objectiveValues['Equation {}'.format(eq)]['Matches Predicted'] += 1

    return objectiveValues

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
    fileName = os.path.join('\\CSVFiles', fileName)

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