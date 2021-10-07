from datetime import timedelta, date
from time import strptime, strftime
from typing import Counter
from CalculatingPValues import CalcPEquation
from DataExtractionFromDB import getSPWData
from InterpolatingDistributions import InterpolateDists
from ReadInGridDB import ReadInGridDB
from CVaRModel import RunCVaRModel
import os
import csv
import datetime

def ComputeBets(matchDetails, riskProfile, riskParameters, betas, budget, oddsMO, oddsMS, oddsNS):
    # This function computes the optimal bets to suggest to a specific user, based off their risk profile.

    # Inputs:
    # - matchDetails: A list of required match details (P1ID, P2ID, Surface being Played on)
    # - riskProfile: The user's risk profile (either 'Risk-Seeking', 'Risk-Neutral' or 'Risk-Averse')
    # - riskParameters: A list of parameters relating to the users responses to the risk questions
    # - betas: The quantiles used in the questions
    # - budget: The users budget for the match they are wanting to bet on
    # - odds lists (oddsMO, oddsMS, oddsNS): 3 lists containing the bookmaker's odds (supplied by the user)
    #   - If the user doesn't want to consider a specific betting option, the list will contain only zeros

    # Returns:
    # - suggestedBets:

    # Model Parameters:
    equation = 2
    options = ['Match Outcome', 'Match Score', 'Number of Sets']

    # Todays Date:
    todaysDate = date.today()

    # Use the calibrated parameters for the given user's risk profile:
    if (riskProfile == 'Risk-Seeking'):
        # Calibrated parameters for a risk-seeking profile:
        calibratedParameters = [2.222, 0.244, 0.233]
    else:
        # Calibrated parameters for a risk-neutral or risk-averse profile:
        calibratedParameters = [2.222, 0.244, 0.233] # Age, Surface, Weighting

    # Extract the required historical data for computing P:
    ageGap = timedelta(days = 365.25 * calibratedParameters[0])
    startOfDataCollection = todaysDate - ageGap
    [p1vP2, p1vCO, p2vCO, COIds] = getSPWData(matchDetails[0],matchDetails[1], todaysDate, startOfDataCollection)

    # Compute Pa and Pb:
    [Pa, Pb, Message] = CalcPEquation(matchDetails, 2, calibratedParameters, p1vP2, p1vCO, p2vCO, COIds)

    # Check we are confident in suggesting bets for this match:
    if (Message == 4):
        # Inform the User that we are not confident in betting on this match due to the lack of historical data
        # between these two players:
        print('Due to the lack of historical data between these two players, we are not confident in predicting any match events for this match')
        return [[], False]
    elif (Message == 2 or Message == 3):
        # Inform the user that we are using limitied historical data to estimate the match event probabilities and
        # hence the user should take caution with the bets:
        print('There is a limited amount of historical data for this match-up and hence the estimated probabilities for the match events have a wider confidence level than usual')

    # Read in the model distributions DB:
    #matchScoreDB = ReadInGridDB('ModelDistributions2.csv')
    matchScoreDB = ReadInGridDB('C:/Uni/4thYearProject/repo/BeatTheOdds/FullProjectCode/CodeToRunApp/ModelDistributions2.csv')

    #allDistsDB = ReadInGridDB('ModelDistributions.csv')
    allDistsDB = ReadInGridDB('C:/Uni/4thYearProject/repo/BeatTheOdds/FullProjectCode/CodeToRunApp/ModelDistributions2.csv')

    # Interploate Distributions: (those needed for analysis and the other ones to display to the user)
    matchScoreDist = InterpolateDists(Pa, Pb, matchScoreDB)
    matchScoreDist = matchScoreDist['Match Score']
    plottingDists = InterpolateDists(Pa, Pb, allDistsDB)

    # Display Distributions to the user:
    # BLAKE TO DO

    # Check what bets the user wants to consider:
    odds = {}
    allOdds = [oddsMO, oddsMS, oddsNS]
    counter = 0
    betsConsidered = []
    for option in options:
        if (sum(allOdds[counter]) > 0.):
            # We are considering this option:
            odds[option] = allOdds[counter]
            betsConsidered.append(1)
        else:
            betsConsidered.append(0)
        counter += 1
    
    # Compute the Optimal Bets to make for the user:
    [Zk, suggestedBets, expectedProfit] = RunCVaRModel(betsConsidered, matchScoreDist, riskProfile, riskParameters, betas, odds)
    
    # Compute the features required to show the user:
    # 1) Amount betting:
    amountBetting = sum(suggestedBets.values())

    # 2) Expected Payout:
    expectedPayout = (expectedProfit + amountBetting) * budget

    # 3) Expected Profit:
    expectedProfit = expectedProfit * budget

    # 4) Payout under each possible scenario:
    outcomePayouts = {}
    for outcome in Zk:
        outcomePayouts[outcome] = 0.
        for bet in Zk[outcome]:
            outcomePayouts[outcome] += Zk[outcome][bet] * suggestedBets[bet] * budget
    print('done')
    # Display bets to user:
    # 1) Pie chart showing split up of budget over the various bets
    #       - Make the non-betting proportion of the budget grey
    #       - Compute the actual value in terms of their budget (not just 0.3 -> $30)
    #       - Have a message at the bottom that offers them an explanation as to why they arent betting their entire budget
    #         e.g. "Click here if you want to understand why we are suggesting you do not bet your entire budget"
    #       - Then have a page that explains why:
    #         e.g. Because of your responses to the risk profile questions, our algorithm is ensuring that you never lose
    #         more than X % of your budget, if you would like to change this, please click here etc.

    # 2) A table highlighting the follow features of their betting portfolio:
    #       - Amount betted
    #       - Expected payout overall (includes their betted amount)
    #       - Expected profit (minus their bets)
    #       - Payout under eacu possible scenario (2-0, 2-1, 0-2, 1-2)

 # Inputs:
    # - matchDetails: A list of required match details (P1ID, P2ID, Surface being Played on)
    # - riskProfile: The user's risk profile (either 'Risk-Seeking', 'Risk-Neutral' or 'Risk-Averse')
    # - riskParameters: A list of parameters relating to the users responses to the risk questions
    # - betas: The quantiles used in the questions
    # - budget: The users budget for the match they are wanting to bet on
    # - odds lists (oddsMO, oddsMS, oddsNS): 3 lists containing the bookmaker's odds (supplied by the user)
    #   - If the user doesn't want to consider a specific betting option, the list will contain only zeros

def addPValuesToCsv(fileToRead,fileToWrite):
    matchAndOddsData = []
    matchDetails = []
    rawMatchDetails =[]
    dates = []
    fileNameRead = os.path.join('C:/Uni/4thYearProject/repo/BeatTheOdds/FullProjectCode/CSVFiles', fileToRead)
    fileNameWrite = os.path.join('C:/Uni/4thYearProject/repo/BeatTheOdds/FullProjectCode/CSVFiles', fileToWrite)
    calibratedParameters = [2.222, 0.244, 0.233] # Age, Surface, Weighting
    with open(fileNameRead) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            matchAndOddsData.append(row)
            line_count += 1
        csv_file.close()

    for match in matchAndOddsData:
        idP1 = match[8]
        idP2 = match[18]
        surface = match[4]
        dateToUse = match[3]
        matchDetails.append([idP1,idP2,surface])
        dates.append(dateToUse)
        rawMatchDetails.append(match)


    # Write the test data to a CSV file:
    #fileName = os.path.join('\\CSVFiles', file)
    
    with open(fileNameWrite, mode = 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        counter = 0
        for row in matchDetails:
            #Extract the required historical data for computing P:
            dateToUse = dates[counter]
            dateToUse1 = datetime.datetime.strptime(dateToUse,"%d/%m/%Y" ).date()
            ageGap = timedelta(days = 365.25 * calibratedParameters[0])
            startOfDataCollection = dateToUse1 - ageGap
            [p1vP2, p1vCO, p2vCO, COIds] = getSPWData(row[0],row[1], dateToUse1, startOfDataCollection)
            [Pa, Pb, Message] = CalcPEquation(row, 2, calibratedParameters, p1vP2, p1vCO, p2vCO, COIds)
            rawMatchDetails[counter].append(Pa)
            rawMatchDetails[counter].append(Pb)
            rawMatchDetails[counter].append(Message)
            writer.writerow(rawMatchDetails[counter])
            counter += 1
        csv_file.close()

def main():
    # Run Compete Bets:
    #ComputeBets([50810,27834,'H'], 'Risk-Averse',[0.9,0.8,0.8], [0.2,1./3,0.5],100, [1.53,2.5], [2.25,4.0,5.5,4.0], [2.31,1.6])
    fileNameRead ='testSetForCalibrationWithROIWithManualyAddedData.csv'
    fileNameWrite ='testSetForCalibrationWithROIWithManualyAddedDataWithPValues.csv'
    addPValuesToCsv(fileNameRead,fileNameWrite)
if __name__ == "__main__":
    main()