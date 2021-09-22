from datetime import timedelta
from CalculatingPValues import CalcPEquation
from DataExtractionFromDB import getSPWData
from InterpolatingDistributions import InterpolateDists
from ModelDistributionsDB import ReadInGridDB
from CVaRModel import RunCVaRModel

def ComputeBets(matchDetails, riskProfile, betsConsidered, ):
    # This function computes the optimal bets to suggest to a specific user, based off their risk profile.

    # Inputs:
    # - matchDetails: A list of required match details (P1ID, P2ID, Date of Match, Surface being Played on)
    # - riskProfile: The user's risk profile (a value between 1 and 64 corresponding to their profile)
    # - betsConsidered: A list of booleans corresponding to the types of the bets the user wants to consider
    #    e.g. [Match Outcome, Match Score, Number of Sets, Set Scores, Number of Games]

    # Returns:
    # - suggestedBets:
    # - 

    # Parameters from Calibration and Evaluation:
    equation = 2
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
        print('Due to the lack of historical data between these two players, we are not confident in suggesting bets')
        return [[], False]
    
    # Read in the model distributions DB:
    matchScoreDB = ReadInGridDB('ModelDistributions2.csv')
    allDistsDB = ReadInGridDB('ModelDistributions.csv')

    # Interploate Distributions: (those needed for analysis and the other ones to display to the user)
    matchScoreDist = InterpolateDists(Pa, Pb, matchScoreDB)
    plottingDists = InterpolateDists(Pa, Pb, allDistsDB)

    # Display Distributions to the user:
    # BLAKE TO DO

    # Compute the Optimal Bets to make for the user:
    RunCVaRModel(betsConsidered, matchScoreDist, )
    # Display bets to user 