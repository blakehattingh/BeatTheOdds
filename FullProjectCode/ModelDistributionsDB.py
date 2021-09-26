import numpy as np
import pandas as pd
import csv
from RunningTheMarkovModel import MarkovModelFirstImplementation
from HelperFunctions import Matrices, Set
from InterpolatingDistributions import *

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
    #writeToFile = 'CSVFiles\\ModelDistributions2.csv'
    writeToFile = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\ModelDistributions2.csv'
    with open(writeToFile, mode='w') as csv_file:
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
            oMallSetA = Set(Pa, (1.-Pb), A, B)
            oMallSetB = Set(Pb, (1.-Pb), A, B)
            avSetA = (oMallSetA + (1. - oMallSetB)) / 2
            avSetB = (oMallSetB + (1. - oMallSetA)) / 2

            # 3-0:
            ThreeNil = pow(avSetA, 3)
            NilThree = pow(avSetB, 3)

            # 3-1:
            ThreeOne = 3 * pow(avSetA, 3) * (1. - avSetA)
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

def ReadInGridDB(FileName):
    # Get location of file:
    FileName = os.path.join('FullProjectCode\\CSVFiles', FileName)

    # Read in the model distributions database: 
    DB = {} 
    x = pd.read_csv(FileName, header = None)
    for row in range(len(x)):
        Pa = round(eval(x[0][row])[0],2)
        Pb = round(eval(x[0][row])[1],2)
        DB[(Pa, Pb)] = eval(x[1][row])

    return DB