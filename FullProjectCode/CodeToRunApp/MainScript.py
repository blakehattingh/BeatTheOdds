from datetime import timedelta
from CalculatingPValues import CalcPEquation
from DataExtractionFromDB import getSPWData
from InterpolatingDistributions import InterpolateDists
from ModelDistributionsDB import ReadInGridDB
from CVaRModel import RunCVaRModel

def ComputeBets(matchDetails, riskProfile, riskParameters, betas, budget, oddsMO, oddsMS, oddsNS):
    # This function computes the optimal bets to suggest to a specific user, based off their risk profile.

    # Inputs:
    # - matchDetails: A list of required match details (P1ID, P2ID, Date of Match, Surface being Played on)
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

    # Use the calibrated parameters for the given user's risk profile:
    if (riskProfile == 'Risk-Seeking'):
        # Calibrated parameters for a risk-seeking profile:
        NEEDTOCALIBRATEMODEL = 10.
    else:
        # Calibrated parameters for a risk-neutral or risk-averse profile:
        calibratedParameters = [2.222, 0.244, 0.233] # Age, Surface, Weighting

    # Extract the required historical data for computing P:
    ageGap = timedelta(days = 365.25 * calibratedParameters[0])
    startOfDataCollection = matchDetails[2] - ageGap
    [p1vP2, p1vCO, p2vCO, COIds] = getSPWData(matchDetails[0],matchDetails[1],matchDetails[2],startOfDataCollection)

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
    matchScoreDB = ReadInGridDB('ModelDistributions2.csv')
    allDistsDB = ReadInGridDB('ModelDistributions.csv')

    # Interploate Distributions: (those needed for analysis and the other ones to display to the user)
    matchScoreDist = InterpolateDists(Pa, Pb, matchScoreDB)
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
            odds[option] = oddsMO
            betsConsidered.append(1)
        else:
            betsConsidered.append(0)
        counter += 1
    
    # Compute the Optimal Bets to make for the user:
    [Zk, suggestedBets, expectedProfit] = RunCVaRModel(betsConsidered, matchScoreDist, riskParameters, betas, odds)
    
    # Compute the features required to show the user:
    # 1) Amount betting:
    amountBetting = sum(suggestedBets.values())

    # 2) Expected Payout:
    expectedPayout = (expectedProfit + amountBetting) * budget

    # 3) Expected Profit:
    expectedProfit = expectedProfit * budget * amountBetting

    # 4) Payout under each possible scenario:
    outcomePayouts = {}
    for outcome in Zk:
        outcomePayouts[outcome] = 0.
        for bet in Zk[outcome]:
            outcomePayouts[outcome] += Zk[outcome][bet] * suggestedBets[bet]

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
    #       - Amount betting
    #       - Expected payout overall (includes their betted amount)
    #       - Expected profit (minus their bets)
    #       - Payout under eacu possible scenario (2-0, 2-1, 0-2, 1-2)
