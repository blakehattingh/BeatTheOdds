from typing import List
from FirstImplementation import MarkovModelFirstImplementation
import numpy as np
import pandas as pd
import csv
#import sklearn 

def BuildingDB(PStart, PEnd, Increment):
    # This function runs our Markov Model for ALL possible P1 and P2 combinations
    # Inputs:
    # - PStart: The lowest P values we want to consider
    # - PEnd: The highest P values we want to consider
    # - Increment: The increase in P values
    #   e.g. P1 = [0.6, 0.61, 0.62....0.90] has PStart = 0.6, PEnd = 0.9 and Increment = 0.01

    # Compute the number of p values to consider:
    N = int(((PEnd - PStart) / Increment) + 1)

    # Create a dictionary to store all distributions from each run of the model:
    # Dictionary Format:
    # - Key = (P1, P2)
    # - Values = Another Dictionary
    #   - Key = Distribution Name e.g. "Match Score"
    #   - Values = Distribution as an array
    DataBase = {}

    # Create an array of P values:
    PValues = np.linspace(PStart/100., PEnd/100., N)

    for P1 in PValues:
        for P2 in PValues:
            # Run the model:
            [MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = MarkovModelFirstImplementation(P1, P2, 3, 7)

            # Create the dictionary of distributions for this run:
            Distributions = {'Match Outcome': [round(Num, 5) for Num in MatchDist], 'Match Score': [round(Num, 5) for Num in
            MatchScoreDist], 'Number of Games': [round(Num, 5) for Num in TotalNumGamesDist], 'Set Score': [round(Num, 5) for
            Num in AllSetScoresDist]}

            # Store the distributions:
            DataBase[(round(P1,2), round(P2,2))] = Distributions

    # Export the dictionary of distributions to a csv file:
    with open('ModelDistributions.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in DataBase.items():
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
                AvDists = BiLinearInterp(DB[PCombos[0]-StepSize,PCombos[1]-StepSize],DB[PCombos[0]+StepSize,PCombos[1]-StepSize], 
                    DB[PCombos[0]-StepSize,PCombos[1]+StepSize],DB[PCombos[0]+StepSize,PCombos[1]+StepSize])
            else:
                # Case 2: Type 2 point (between 2 points laterally)
                AvDists = BiLinearInterp(DB[PCombos[0], PCombos[1]-StepSize], DB[PCombos[0], PCombos[1]+StepSize])
        else:
            if (CountB % 2 == 1):
                # Case 3: Type 3 point (between 2 points vertically)
                AvDists = BiLinearInterp(DB[PCombos[0]-StepSize, PCombos[1]], DB[PCombos[0]+StepSize, PCombos[1]])
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

def ComputeAverageArray(ListOfArrays):
    # Each row is an array

    AvArray = np.zeros(len(ListOfArrays[0]), dtype = float)
    for i in len(ListOfArrays[0]):
        for j in len(ListOfArrays):
            AvArray[i] += ListOfArrays[j][i]
    
    # Average the array:
    AvArray = AvArray / len(AvArray)

def main():
    # Read in the model distributions database: 
    DB = {}     
    with open('ModelDistributions.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if (row == []):
                break
            else:
                DB[row[0]] = row[1]

    # Compute the RMSEs:
    RMSEs = ValidatingStepSize(DB, 0.02)
    print(RMSEs)

if __name__ == "__main__":
    main()