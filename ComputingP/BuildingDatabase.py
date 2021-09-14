from typing import List
import numpy as np
import pandas as pd
import csv
import os, sys

# Add required folders to the system path:
currentPath = os.path.abspath(os.getcwd())

# Markov Model Files:
sys.path.insert(0, currentPath + '\\MarkovModel')
from FirstImplementation import *
from OMalleysEqns import *

def BuildingDB(PStartA, PEndA, PStartB, PEndB, Increment, AllDists, DBToAppendTo = {}):
    # This function runs our Markov Model for ALL possible P1 and P2 combinations
    # Inputs:
    # - PStartA and B: The lowest P values we want to consider for Pa and Pb respectively
    # - PEndA and B: The highest P values we want to consider for Pa and Pb respectively
    # - Increment: The increase in P values
    # - AllDists: Is a boolean informing us if we are using all 4 distributions or just Match Score
    # - DBToAppendTo: The database we want to keep building incrementally
    #   e.g. P1 = [0.6, 0.61, 0.62....0.90] has PStart = 0.6, PEnd = 0.9 and Increment = 0.01

    # Compute the number of p values to consider:
    Na = int(((PEndA - PStartA) / Increment) + 1)
    Nb = int(((PEndB - PStartB) / Increment) + 1)

    # Create a dictionary to store all distributions from each run of the model:
    # Dictionary Format:
    # - Key = (P1, P2)
    # - Values = Another Dictionary
    #   - Key = Distribution Name e.g. "Match Score"
    #   - Values = Distribution as an array
    DataBase = DBToAppendTo

    # Create an array of P values:
    PValuesA = np.linspace(PStartA/100., PEndA/100., Na)
    PValuesB = np.linspace(PStartB/100., PEndB/100., Nb)

    for P1 in PValuesA:
        for P2 in PValuesB:
            print('P-values: ', [P1],[P2])

            if (AllDists):                 
                # Run the model:
                [MatchOutcomeDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = MarkovModelFirstImplementation(P1,P2,3)

                # Create the dictionary of distributions for this run:
                Distributions = {'Match Outcome': [round(Num, 6) for Num in MatchOutcomeDist], 'Match Score': 
                [round(Num, 6) for Num in MatchScoreDist], 'Number of Games': [round(Num, 6) for Num in TotalNumGamesDist], 'Set Score':
                [round(Num, 6) for Num in AllSetScoresDist]}
            else:
                # If P1 = P2, we know the distribution is simply [0.25, 0.25, 0.25, 0.25]
                if (round(P1,3) == round(P2,3)):
                    Distributions = {'Match Score': [0.25, 0.25, 0.25, 0.25]}
                else:
                    # Run the model:
                    MatchScoreDist = MarkovModelFirstImplementation(P1, P2, 3)
                    Distributions = {'Match Score': [round(Num, 6) for Num in MatchScoreDist]}

            # Store the distributions:
            DataBase[(round(P1,2), round(P2,2))] = Distributions

    # Export the dictionary of distributions to a csv file:
    with open('CSVFiles\\ModelDistributions2.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in DataBase.items():
            writer.writerow([key, value])

def BuildingDB5SetsUsingOMalleys(PStartA, PEndA, PStartB, PEndB, Increment):
    # This function uses O'Malley's Equations to comptue the Match Score distribution for 5 set matches for all
    #  possible P1 and P2 combinations
    # Inputs:
    # - PStartA and B: The lowest P values we want to consider for Pa and Pb respectively
    # - PEndA and B: The highest P values we want to consider for Pa and Pb respectively
    # - Increment: The increase in P values

    # Compute the number of p values to consider:
    Na = int(((PEndA - PStartA) / Increment) + 1)
    Nb = int(((PEndB - PStartB) / Increment) + 1)

    # Create an array of P values:
    PValuesA = np.linspace(PStartA/100., PEndA/100., Na)
    PValuesB = np.linspace(PStartB/100., PEndB/100., Nb)

    # Fill up the Database:
    dataBase = {}
    for Pa in PValuesA:
        for Pb in PValuesB:
            # Compute the Match Score distribution:
            [A, B] = Matrices()
            oMallSetA = Set(P1S, (1.-P2S), A, B)
            oMallSetB = Set(P2S, (1.-P1S), A, B)
            avSetA = (oMallSetA + (1. - oMallSetB)) / 2
            avSetB = (oMallSetB + (1. - oMallSetA)) / 2

            # 3-0:
            ThreeNil = pow(avSetA, 3)
            NilThree = pow(avSetB, 3)

            # 3-1:
            ThreeOne = 3 * pow(avSetA) * (1. - avSetA)
            OneThree = 3 * pow(avSetB, 3) * (1. - avSetB)

            # 3-2:
            ThreeTwo = 6 * pow(avSetA, 3) * pow((1. - avSetA), 2)
            TwoThree = 6 * pow(avSetB, 3) * pow((1. - avSetB), 2)

            # Create the distribution and round it:
            MatchScoreDist = [ThreeNil, ThreeOne, ThreeTwo, NilThree, OneThree, TwoThree]
            Distributions = {'Match Score': [round(Num, 6) for Num in MatchScoreDist]}

            # Add it to the database:
            dataBase[(round(Pa,2),round(Pb,2))] = Distributions

    # Export the dictionary of distributions to a csv file:
    with open('CSVFiles\\ModelDistributions5Sets.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dataBase.items():
            writer.writerow([key, value])

def ValidatingStepSize(DB,StepSize):
    # This function interpolates every point between the points spaced 0.04 apart in the grid of parameter combos
    # It uses a bi-linear interpolation for the points between 4 points and a single linear interpolation for points
    # between 2 points in the grid.
    # The evaluation metric used is the RMSE, 1 for each distribution outputted from the model
    # Inputs:
    # - DB = Database of outputted distributions for all P value parameter combinations
    # - StepSize = The increment between p values in the grid

    # Compute the length of grid:
    NumKeys = len(DB.keys())
    N = pow(NumKeys, 0.5)

    Count = 0
    CountA = 0
    CountB = 0
    RMSEs = {'Match Outcome': 0, 'Match Score': 0, 'Number of Games': 0, 'Set Score': 0}
    for PCombos in DB:
        # Find where this point is in the grid:
        NoNeedToInterpolate = False
        if (CountA % 2 == 1):
            if (CountB % 2 == 1):
                # Case 1: Mid point - Use bi-linear interpolation
                AvDists = BiLinearInterp(DB[round(PCombos[0]-StepSize,2),round(PCombos[1]-StepSize,2)],DB[round(PCombos[0]+
                StepSize,2),round(PCombos[1]-StepSize,2)],DB[round(PCombos[0]-StepSize,2),round(PCombos[1]+StepSize,2)],
                DB[round(PCombos[0]+StepSize,2),round(PCombos[1]+StepSize,2)])
            else:
                # Case 2: Type 2 point (between 2 points laterally)
                AvDists = LinearInterp(DB[round(PCombos[0]-StepSize,2),PCombos[1]],DB[round(PCombos[0]+StepSize,2),PCombos[1]])
        else:
            if (CountB % 2 == 1):
                # Case 3: Type 3 point (between 2 points vertically)
                AvDists = LinearInterp(DB[PCombos[0],round(PCombos[1]-StepSize,2)],DB[PCombos[0],round(PCombos[1]+StepSize,2)])
            else:
                NoNeedToInterpolate = True
        
        # Compute the error metric (RMSE):
        if (NoNeedToInterpolate):
            RMSE = 0
        else:
            Count += 1
            for dist in DB[PCombos]:
                #MSE = sklearn.metrics.mean_squared_error(DB[PCombos][dist], InterpolatedMODist)
                E = [a - b for a, b in zip(DB[PCombos][dist], AvDists[dist])]
                SE = [Num ** 2 for Num in E]
                MSE = np.mean(SE)
                RMSE = pow(MSE, 0.5)
                RMSEs[dist] += RMSE
                if (dist == "Match Outcome"):
                    if (RMSE > 0.2):
                        print(PCombos)
                        print(RMSE)
            
        # Increase / reset counters:
        if (CountB == (N-1)):
            CountB = 0
            CountA += 1
        else:
            CountB += 1
    
    # Average the RMSE values:
    for i in RMSEs:
        RMSEs[i] = RMSEs[i] / Count

    return RMSEs

def BiLinearInterp(PCombo1, PCombo2, PCombo3, PCombo4):
    # Takes in 4 corner points with corresponding distributions and computes their average
    # Assumes an equally weighted averaged is required

    # Match Outcome Distribution:
    AvMatchOutcomeDist = ComputeAverageArray([PCombo1['Match Outcome'],PCombo2['Match Outcome'],PCombo3['Match Outcome'],
    PCombo4['Match Outcome']])

    # Match Score Distribution:
    AvMatchScoreDist = ComputeAverageArray([PCombo1['Match Score'],PCombo2['Match Score'],PCombo3['Match Score'],
    PCombo4['Match Score']])

    # Number of Games Distribution:
    AvNumGamesDist = ComputeAverageArray([PCombo1['Number of Games'],PCombo2['Number of Games'],
    PCombo3['Number of Games'],PCombo4['Number of Games']])

    # Set Score Distribution:
    AvSetScoreDist = ComputeAverageArray([PCombo1['Set Score'],PCombo2['Set Score'],PCombo3['Set Score'],
    PCombo4['Set Score']])

    # Create dictionary of average distributions:
    AvDists = {'Match Outcome': AvMatchOutcomeDist, 'Match Score': AvMatchScoreDist, 'Number of Games': AvNumGamesDist,
    'Set Score': AvSetScoreDist}
    return AvDists

def LinearInterp(PCombo1, PCombo2, EvenWeight = True, Weighting = 0.5):
    # Takes in 2 points either sidewith corresponding distributions and computes their average
    # Assumes an equally weighted averaged is required unless specified otherwise

    if (EvenWeight):
        # Match Outcome Distribution:
        AvMatchOutcomeDist = ComputeAverageArray([PCombo1['Match Outcome'],PCombo2['Match Outcome']])

        # Match Score Distribution:
        AvMatchScoreDist = ComputeAverageArray([PCombo1['Match Score'],PCombo2['Match Score']])

        # Number of Games Distribution:
        AvNumGamesDist = ComputeAverageArray([PCombo1['Number of Games'],PCombo2['Number of Games']])

        # Set Score Distribution:
        AvSetScoreDist = ComputeAverageArray([PCombo1['Set Score'],PCombo2['Set Score']])
    else:
        # Match Outcome Distribution:
        AvMatchOutcomeDist = WeightedAverage([PCombo1['Match Outcome'],PCombo2['Match Outcome']],Weighting)

        # Match Score Distribution:
        AvMatchScoreDist = WeightedAverage([PCombo1['Match Score'],PCombo2['Match Score']],Weighting)

        # Number of Games Distribution:
        AvNumGamesDist = WeightedAverage([PCombo1['Number of Games'],PCombo2['Number of Games']],Weighting)

        # Set Score Distribution:
        AvSetScoreDist = WeightedAverage([PCombo1['Set Score'],PCombo2['Set Score']],Weighting)    

    # Create dictionary of average distributions:
    AvDists = {'Match Outcome': AvMatchOutcomeDist, 'Match Score': AvMatchScoreDist, 'Number of Games': AvNumGamesDist,
    'Set Score': AvSetScoreDist}
    return AvDists

def ComputeAverageArray(ListOfArrays):
    # Each row is an array

    AvArray = np.zeros(len(ListOfArrays[0]), dtype = float)
    for i in range(len(ListOfArrays[0])):
        for j in range(len(ListOfArrays)):
            AvArray[i] += ListOfArrays[j][i]
    
    # Average the array:
    AvArray = AvArray / len(ListOfArrays)

    return AvArray

def WeightedAverage(Dist1, Dist2, alpha):
    # This function computes a weighted average distribution between 2 points
    # Inputs:
    # - Dist1 / 2 = The 2 distributions to weight
    # - alpha = Weighting between Dist1 and Dist2 

    # Create average array:
    AvArray = np.zeros(len(Dist1), dtype = float)
    for i in range(len(Dist1)):
        AvArray[i] = alpha * Dist1[i] + (1. - alpha) * Dist2[i]
    
    return AvArray

def ComputeWeighting(Pa, Pb, Spacing = 0.02):
    # This function takes in two computed P values and finds the weighting between the grid points
    # Inputs:
    # - Pa, Pb = The p-values of the point
    # - Spacing = The spacing between points on the grid (assumed to be 0.02)

    # Compute distance from Pa and Pb to the Pa and Pb point before this point:
    a = Pa % Spacing
    b = Pb % Spacing

    # Compute Weights:
    alpha = (Spacing - a) / Spacing
    beta = (Spacing - b) / Spacing

    return [alpha, beta]

def ReadInGridDB(FileName):
    # Get location of file:
    THIS_FOLDER = os.path.abspath('CSVFiles')
    FileName = os.path.join(THIS_FOLDER, FileName)

    # Read in the model distributions database: 
    DB = {} 
    # x = pd.read_csv('C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\ModelDistributions.csv', header = None)
    x = pd.read_csv(FileName, header = None)
    for row in range(len(x)):
        Pa = round(eval(x[0][row])[0],2)
        Pb = round(eval(x[0][row])[1],2)
        DB[(Pa, Pb)] = eval(x[1][row])

    return DB

def main():
    # Read in grid:
    DB = ReadInGridDB('ModelDistributions2.csv')

    # Compare both DBs:
    DB1 = ReadInGridDB('ModelDistributions.csv')
    DB2 = ReadInGridDB('ModelDistributions2.csv')
    
    # Iterate through each distribution:
    Diff = {}
    for pair in DB2:
        if (pair[0] >= 0.5):
            if (pair[1] >= 0.5):
                Diff[pair] = 0.
                for p in range(len(DB2[pair]['Match Score'])):
                    Diff[pair] += abs(DB2[pair]['Match Score'][p] - DB1[pair]['Match Score'][p])
    # print(Diff)

    # Build the DB of model distributions:
    #params: PaStart, PaEnd, PbStart, PbEnd, stepSize, AllDists?, DB
    BuildingDB(60, 60, 40, 80, 2, False, DBToAppendTo = DB)

    # Compute the RMSEs:
    # RMSEs = ValidatingStepSize(DB, 0.02)
    # print(RMSEs)

if __name__ == "__main__":
    main()