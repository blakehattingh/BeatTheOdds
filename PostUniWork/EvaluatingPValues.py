import os
import csv
from datetime import timedelta
from time import strptime
from typing import Match
from ModelDistributionsDB import ReadInGridDB
from CalculatingPValues import CalcPEquation2
from DataExtractionFromDB import getSPWData
from InterpolatingDistributions import InterpolateDists
from CVaRModel import RunCVaRModel
import datetime

def ObjectiveMetricMatchOutcome(MatchScoreDist, Winner):
    # See who the Markov Model (MM) has as winner:
    probAWins = MatchScoreDist[0] + MatchScoreDist[1]
    if (probAWins > 0.5):
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

def ObjectiveMetricNumSets(MatchScoreDist, NumSets):
    # Make sure MatchScoreDist is a list:
    MatchScoreDist = MatchScoreDist.tolist()

    # See how many sets the Markov Model has as most likely:
    twoSetsProb = MatchScoreDist[0] + MatchScoreDist[2]
    if (twoSetsProb >= 0.5):
        predictedNumSets = 2
    else:
        predictedNumSets = 3

    # See if it matches with the actual result:
    if (predictedNumSets == NumSets):
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

def EvalEquations(matchesFN, hyperparameters, riskProfile = 'Risk-Averse', alphas = [0.9, 0.8, 0.7], betas = [0.1, 0.2, 0.3]):
    # This function takes a test or training set of matches, an equation(s) to use and it evaluates the specified 
    # objective metric across the inputted data set.
    # Inputs:
    # - matchesFN: A csv filename for the test/training set of matches
    # - hyperparameters: age, surface, and weighting
    # - riskProfile: the risk profile used for the CVaR model
    # - alphas: a list of RHS values for the profile getting used
    # - betas: a list of beta values to use in the CVaR model

    # Returns:
    # - The objective metrics over the data inputted

    # Read in the model distributions:
    DB = ReadInGridDB('ModelDistributions2.csv')

    # Read in the data:
    testData = ReadInData(matchesFN, header=True)
    ageGap = timedelta(days = 365.25 * hyperparameters[0])

    # Create a dictionary to store the objective metric(s):
    objectiveValues = {}
    objectiveValues['Match Outcome'] = 0.
    objectiveValues['Match Score'] = 0.
    objectiveValues['Number of Sets'] = 0.
    # objectiveValues['Combination'] = 0.
    objectiveValues['Matches Predicted'] = 0.

    # Using the equations specified, compute the objective metric specified for each match in test data:
    count = 0
    for match in testData:
        print('Match {}'.format(count))
        count += 1
        # Extract the test match data:
        dateOfMatch = datetime.datetime.strptime(match[3], '%d/%m/%Y').date()
        matchScore = [int(match[30]),int(match[31])]
        numSets = sum(matchScore)
        startOfDataCollection = dateOfMatch - ageGap

        # Collect player data for the players in the match:
        p1vP2,p1vCO,p2vCO,COIds = getSPWData(match, startOfDataCollection)

        # Compute the P values for the two players:
        [Pa, Pb, predict] = CalcPEquation2(hyperparameters, match, p1vP2, p1vCO, p2vCO, COIds)

        # Look to make predictions using these P values:
        if (predict):
            # Interpolate the distributions for these P values:
            Dists = InterpolateDists(Pa, Pb, DB, pBoundaryL = 0.4, pBoundaryH = 0.8)

            # Compute the objective metrics for this match:
            objectiveValues['Match Outcome'] += ObjectiveMetricMatchOutcome(Dists['Match Score'], 1)
            objectiveValues['Match Score'] += ObjectiveMetricMatchScore(Dists['Match Score'], matchScore)
            objectiveValues['Number of Sets'] += ObjectiveMetricNumSets(Dists['Match Score'], numSets)
            objectiveValues['Matches Predicted'] += 1
        else:
            print('Did not predict on')
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

def ReadInData(fileName, header):
    # Get location of file:
    THIS_FOLDER = os.path.abspath('PostUniWork\\CSVFiles')
    location = os.path.join(THIS_FOLDER, fileName)

    # Read in CSV file:
    testData = []
    with open(location) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if (header):
                if line_count == 0:
                    line_count += 1
                else:
                    testData.append(row)
                    line_count += 1
            else:
                testData.append(row)
                line_count += 1
    
    return testData

def main():
    # This function tests the computing the P equations.
    
    # Read in files:
    p1vsP2 = ReadInData('IsnerVsTsitsipas.csv', header=True)
    p1VsCOs = ReadInData('IsnerVsCOs.csv',header=True)
    p2VsCOs = ReadInData('TsitsipasVsCos.csv',header=True)
    commOppsIDs = ReadInData('listOfCommonOpponentIDs.csv',header=False)

    commOppsIDs = commOppsIDs[0]
    commOppsIDs[0] = 5528
    for i in range(len(commOppsIDs)):
        commOppsIDs[i] = int(commOppsIDs[i])

    matchDetails = [4544, 26577, 'C']
    equation = 1
    calibratedParams = [8, 0.2, 0.2]

    # Calculate P:
    [Pa, Pb, Bet] = CalcPEquation(matchDetails,equation,calibratedParams,p1vsP2,p1VsCOs,p2VsCOs,commOppsIDs)
    print(Pa)
    print(Pb)

if __name__ == "__main__":
    main()