from datetime import datetime, timedelta
from typing import Match
from pandas.core.base import DataError
from FirstImplementation import MarkovModelFirstImplementation
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

def try_parsing_date(text):
    for fmt in ('%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

def EvalEquation(Pa, Pb, MatchData):
    # For given P Values, this function runs the model and evaluates the objective metrics
    # Inputs:
    # - Pa & Pb = Markov Model Parameters
    # - MatchData = A dictionary of the match data:
    #               Keys = 'Winner', 'Set Scores', 'Match Score'
    # Returns:
    # - ObjectiveVals = A dictionary of the various objective metric values
    #                   Keys = 'MatchOutcome', 'SetScores', 'MatchScore'

    # Run the model with the given inputs:
    [MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = MarkovModelFirstImplementation(Pa, Pb, 3, 7)

    print('MatchDist:', MatchDist)
    print('AllSetScoresDist:', AllSetScoresDist)
    # Evaluate the objective metrics:

    # Match Outcome:
    Prop = ObjectiveMatchScoreDist(MatchScoreDist, MatchData['MatchOutcome'])
    
    # Set Scores:
    Points = ObjectiveMetricSetScore(AllSetScoresDist, MatchData['SetScores'])

    # Return Objective:
    ObjectiveVals = {'MatchOutcome': Prop, 'SetScores': Points, 'MatchScore': 0}
    return ObjectiveVals

def CalcPEquation1(PlayerA, PlayerB, CommonOpps, MatchDataFileName, MatchDataFileNameCommA, MatchDataFileNameCommB, DateOfMatch, SurfaceOfMatch, 
Lamda, Age, Surface):
    # Compute SPW(A,B) and SPW(B, A):
    [spwAB, spwBA] = ComputeSPW(PlayerA, PlayerB, Age, Surface, MatchDataFileName, DateOfMatch, SurfaceOfMatch)
    print('spwAB:', spwAB, 'spwBA:', spwBA)

    # Compute RPW(A,B) and RPW(B,A)
    rpwAB = 1. - spwBA
    rpwBA = 1. - spwAB

    # Compute SPW(A,C) and SPW(B,C):
    [spwAC, rpwAC] = ComputeSPWCommon(PlayerA, CommonOpps, Age, Surface, MatchDataFileNameCommA, DateOfMatch, SurfaceOfMatch) 
    [spwBC, rpwBC] = ComputeSPWCommon(PlayerB, CommonOpps, Age, Surface, MatchDataFileNameCommB, DateOfMatch, SurfaceOfMatch)

    print('spwAC:', spwAC, 'rpwAC:', rpwAC)
    print('spwBC:', spwBC, 'rpwBC:', rpwBC) 

    # Compute P Values:
    Pa = (1  - Lamda) * spwAB + Lamda * spwAC
    Pb = (1  - Lamda) * spwBA + Lamda * spwBC

    print('Pa:', Pa, 'Pb:', Pb)

def ComputeSPW(PlayerA, PlayerB, Age, Surface, MatchDataFileName, DateOfMatch, SurfaceOfMatch):
    # Inputs:
    # - PlayerA & PlayerB = IDs of both players of interest 
    # - Age = A hyperparameter corresponding to how far back we go in terms of the data (integer, units = Years)
    # - Surface = A hyperparameter corresponding to the weighting on matches played on the same surface
    # - MatchDataFileName = The name of the csv file containing all match data between player A and player B
    # - DateOfMatch = The date of the match as a string in format '%d/%m/%Y'
    # - SurfaceOfMatch = The surface that the match will be played on (as an abbrev, e.g. C = Clay)

    # Required Columns:
    ColNames = ['date', 'surface', 'winner_id', 'w_sv_pt', 'w_1st_won', 'w_2nd_won', 'l_sv_pt', 'l_1st_won', 'l_2nd_won']

    # Read in the csv file corresponding to all the games between player A and player B:
    MatchData = pd.read_csv(MatchDataFileName, usecols = ColNames)

    # Compute the date of the match:
    DOMDate = datetime.strptime(DateOfMatch, '%d/%m/%Y')

    # Compute the date we want to collect data up until:
    AgeGap = timedelta(days = 365.25 * Age)

    # Sum up the service points played for each player:
    PlayerAServePointsSurface = 0
    PlayerAServePointsWonSurface = 0
    PlayerBServePointsSurface = 0
    PlayerBServePointsWonSurface = 0
    PlayerAServePointsNS = 0
    PlayerAServePointsWonNS = 0
    PlayerBServePointsNS = 0
    PlayerBServePointsWonNS = 0
    for match in range(len(MatchData)):
        # Check when the match was played:
        MatchDate = datetime.strptime(MatchData.iloc[match].loc['date'], '%d/%m/%Y')

        if (((DOMDate - MatchDate).days > 0) and (((DOMDate - AgeGap) - MatchDate).days < 0)):
            if (MatchData.iloc[match].loc['surface'] == SurfaceOfMatch):
                if (MatchData.iloc[match].loc['winner_id'] == PlayerA):
                    PlayerAServePointsSurface += MatchData.iloc[match].loc['w_sv_pt']
                    PlayerAServePointsWonSurface += (MatchData.iloc[match].loc['w_1st_won'] + MatchData.iloc[match].loc['w_2nd_won'])
                    PlayerBServePointsSurface += MatchData.iloc[match].loc['l_sv_pt']
                    PlayerBServePointsWonSurface += (MatchData.iloc[match].loc['l_1st_won'] + MatchData.iloc[match].loc['l_2nd_won'])
                else:
                    PlayerAServePointsSurface += MatchData.iloc[match].loc['l_sv_pt']
                    PlayerAServePointsWonSurface += (MatchData.iloc[match].loc['l_1st_won'] + MatchData.iloc[match].loc['l_2nd_won'])
                    PlayerBServePointsSurface += MatchData.iloc[match].loc['w_sv_pt']
                    PlayerBServePointsWonSurface += (MatchData.iloc[match].loc['w_1st_won'] + MatchData.iloc[match].loc['w_2nd_won'])
            else:
                if (MatchData.iloc[match].loc['winner_id'] == PlayerA):
                    PlayerAServePointsNS += MatchData.iloc[match].loc['w_sv_pt']
                    PlayerAServePointsWonNS += (MatchData.iloc[match].loc['w_1st_won'] + MatchData.iloc[match].loc['w_2nd_won'])
                    PlayerBServePointsNS += MatchData.iloc[match].loc['l_sv_pt']
                    PlayerBServePointsWonNS += (MatchData.iloc[match].loc['l_1st_won'] + MatchData.iloc[match].loc['l_2nd_won'])
                else:
                    PlayerAServePointsNS += MatchData.iloc[match].loc['l_sv_pt']
                    PlayerAServePointsWonNS += (MatchData.iloc[match].loc['l_1st_won'] + MatchData.iloc[match].loc['l_2nd_won'])
                    PlayerBServePointsNS += MatchData.iloc[match].loc['w_sv_pt']
                    PlayerBServePointsWonNS += (MatchData.iloc[match].loc['w_1st_won'] + MatchData.iloc[match].loc['w_2nd_won'])
            
    # Compute the proportion of service points won:
    PlayerAServiceProp = (1 - Surface) * (PlayerAServePointsWonSurface / PlayerAServePointsSurface) + Surface * (PlayerAServePointsWonNS / PlayerAServePointsNS)
    PlayerBServiceProp = (1 - Surface) * (PlayerBServePointsWonSurface / PlayerBServePointsSurface) + Surface * (PlayerBServePointsWonNS / PlayerBServePointsNS)

    return PlayerAServiceProp, PlayerBServiceProp

def ComputeSPWCommon(PlayerA, CommonOpps, Age, Surface, MatchDataFileName, DateOfMatch, SurfaceOfMatch):    
    # Required Columns:
    ColNames = ['date', 'surface', 'winner_id', 'loser_id', 'w_sv_pt', 'w_1st_won', 'w_2nd_won', 'l_sv_pt', 'l_1st_won', 'l_2nd_won']

    # Read in the csv file corresponding to all the games between player A and player B:
    MatchData = pd.read_csv(MatchDataFileName, usecols = ColNames)

    # Compute Match date:
    DOMDate = datetime.strptime(DateOfMatch, '%d/%m/%Y')

    # Compute the date we want to collect data up until:
    AgeGap = timedelta(days = 365.25 * Age)

    # Sum up the service points played for each player:
    PlayerAServePointsSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAServePointsWonSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAServePointsNS = np.zeros(len(CommonOpps), dtype = int)
    PlayerAServePointsWonNS = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsWonSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsNS = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsWonNS = np.zeros(len(CommonOpps), dtype = int)
    for match in range(len(MatchData)):
        # Check when the match was played:
        MatchDate = try_parsing_date(MatchData.iloc[match].loc['date'])
        #MatchDate = datetime.strptime(MatchData.iloc[match].loc['date'], '%d/%m/%Y')

        if (((DOMDate - MatchDate).days > 0) and (((DOMDate - AgeGap) - MatchDate).days < 0)):
            if (MatchData.iloc[match].loc['surface'] == SurfaceOfMatch):
                if (MatchData.iloc[match].loc['winner_id'] == PlayerA):
                    # Find who the opponent was:
                    Opp = CommonOpps.index(MatchData.iloc[match].loc['loser_id'])
                    PlayerAServePointsSurface[Opp] += MatchData.iloc[match].loc['w_sv_pt']
                    PlayerAServePointsWonSurface[Opp] += (MatchData.iloc[match].loc['w_1st_won'] + MatchData.iloc[match].loc['w_2nd_won'])
                    PlayerAReturnPointsSurface[Opp] += MatchData.iloc[match].loc['l_sv_pt']
                    PlayerAReturnPointsWonSurface[Opp] += (MatchData.iloc[match].loc['l_sv_pt'] - (MatchData.iloc[match].loc['l_1st_won'] + MatchData.iloc[match].loc['l_2nd_won']))
                else:
                    # Find who the opponent was:
                    Opp = CommonOpps.index(MatchData.iloc[match].loc['winner_id'])
                    PlayerAServePointsSurface[Opp] += MatchData.iloc[match].loc['l_sv_pt']
                    PlayerAServePointsWonSurface[Opp] += (MatchData.iloc[match].loc['l_1st_won'] + MatchData.iloc[match].loc['l_2nd_won'])
                    PlayerAReturnPointsSurface[Opp] += MatchData.iloc[match].loc['w_sv_pt']
                    PlayerAReturnPointsWonSurface[Opp] += (MatchData.iloc[match].loc['w_sv_pt'] - (MatchData.iloc[match].loc['w_1st_won'] + MatchData.iloc[match].loc['w_2nd_won']))
            else:
                if (MatchData.iloc[match].loc['winner_id'] == PlayerA):
                    # Find who the opponent was:
                    Opp = CommonOpps.index(MatchData.iloc[match].loc['loser_id'])
                    PlayerAServePointsNS[Opp] += MatchData.iloc[match].loc['w_sv_pt']
                    PlayerAServePointsWonNS[Opp] += (MatchData.iloc[match].loc['w_1st_won'] + MatchData.iloc[match].loc['w_2nd_won'])
                    PlayerAReturnPointsNS[Opp] += MatchData.iloc[match].loc['l_sv_pt']
                    PlayerAReturnPointsWonNS[Opp] += (MatchData.iloc[match].loc['l_sv_pt'] - (MatchData.iloc[match].loc['l_1st_won'] + MatchData.iloc[match].loc['l_2nd_won']))
                else:
                    # Find who the opponent was:
                    Opp = CommonOpps.index(MatchData.iloc[match].loc['winner_id'])
                    PlayerAServePointsNS[Opp] += MatchData.iloc[match].loc['l_sv_pt']
                    PlayerAServePointsWonNS[Opp] += (MatchData.iloc[match].loc['l_1st_won'] + MatchData.iloc[match].loc['l_2nd_won'])
                    PlayerAReturnPointsNS[Opp] += MatchData.iloc[match].loc['w_sv_pt']
                    PlayerAReturnPointsWonNS[Opp] += (MatchData.iloc[match].loc['w_sv_pt'] - (MatchData.iloc[match].loc['w_1st_won'] + MatchData.iloc[match].loc['w_2nd_won']))
    
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
    # Create match data:
    MatchData = {'MatchOne': {'MatchOutcome': 2, 'SetScores': [[4,6],[6,4]], 'MatchScore': 3, 'Date': '19/08/2018', 'Surface': 'H'}, 
    'MatchTwo': {'MatchOutcome': 2, 'SetScores': [[6,7],[7,5],[6,7]], 'MatchScore': 4, 'Date': '03/11/2018', 'Surface': 'H'}}

    # Common Opponents:
    CommOpps = [5216,3898,4913,5663,3900,4606,4742,5442,3786,3602,4053,4789,3720,2318,4541,3206,3344,3163,4868,3017,26577,2450,5201,4526,
    5220,27834,5763,3096,3084,6219,4752,4659,4544,644,2148,6409,2257,3656,5670,4570,5349,3888,4338,4467,3454,3103,4728,3498,6418,3507,4311,5070,
    5630,3990,3333,5918,3285,3835,4416,3484,2783,3632,4664,3781,6387,3852,3428,5543,3823,5131,5922,4585,4259,5515,4994,3292,5016,3917,
    3813,4068,4035,3758,5166,5159,6401,4122,4098,2179,4022,5210,4470,2839,4269,4229,4675,3582,11547,4019,3843,3808,3970,5055,4716,4214,
    3694,2845,2565,2720,6029,5565,5303,3909,34553,5655,4198,5324,4677,32067,3566,6044,4291,5088,6407,5034,3598,4794,5801,4180,4337,
    5978,4894,5902,4385,5539,4596,3722,3429,5057,5231,26006,4533,4654,4252,5438,6284,6364,3908,5986,2967,4619,3812,6031,5718,4499,3752,
    5046,26413,4921,4914,3794,3565,4225,5571,6057,33214,3893,4326,4879,5793,4592,11176,36221,5370,26010,5375,4493,3503,3110,5636,4331,
    3181,6214,4591,4974]

    # Store Objective Points:
    Objective = {'MatchOutcome': 0, 'SetScores': 0, 'MatchScore': 0}

    # Run the model using equation 1 for the matches:
    for match in MatchData.values():
        # Compute the P values:
        [Pa, Pb] = CalcPEquation1(3819, 4920, CommOpps, 'SQLData/fedVsDjok.csv', 'SQLData/fedVsComOppDjok.csv', 'SQLData/DjokVsComOppfed.csv',
        match['Date'], match['Surface'], 0.5, 12, 0.5)

        # Evaluate how well the model did:
        Obj = EvalEquation(Pa, Pb, match)

        # Record the objective scores:
        for Metric in Obj:
            Objective[Obj] += Obj[Metric]

    print(Objective)


if __name__ == "__main__":
    main()