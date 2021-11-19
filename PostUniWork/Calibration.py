from EvaluatingPValues import EvalEquations
from DataExtractionFromDB import getSPWData
from CSVFileFunctions import ExportToCSV

def Calibration(fileName):
    # Set up points in the parameter space to evaluate metrics at:
    gridPoints = []
    agePoints = [1.25, 1.5, 1.75, 2., 2.25, 2.5, 2.75, 3.]
    surfacePoints = [0.2, 0.4, 0.6, 0.8]
    weightingPoints = [0.2, 0.4, 0.6, 0.8]
    for age in agePoints:
        for surface in surfacePoints:
            for weight in weightingPoints:
                gridPoints.append([age, surface, weight])

    # Set up a lists to store the accuracy metrics:
    matchOutcome = []
    matchScore = []
    numSets = []
    matchesPredicted = []
    ageParams = []
    surfaceParams = []
    weightingParams = []

    # Compute the classification accuracy for each grid point:
    for point in gridPoints:
        print('Grid Point: {} {} {}'.format(point[0],point[1],point[2]))
        # Evaluate the classification accuracy for this point:
        objective = EvalEquations(fileName, point)

        # Store metrics:
        matchOutcome.append(objective['Match Outcome'])
        matchScore.append(objective['Match Score'])
        numSets.append(objective['Number of Sets'])
        matchesPredicted.append(objective['Matches Predicted'])
        ageParams.append(point[0])
        surfaceParams.append(point[1])
        weightingParams.append(point[2])
    
    return [matchOutcome, matchScore, numSets, matchesPredicted, ageParams, surfaceParams, weightingParams]

def main():
    fileName1 = 'RandomSampleHardTraining.csv'
    fileName2 = 'RandomSampleHardTraining.csv'
    fileName3 = 'RandomSampleHardTraining.csv'

    # Run the calibration:
    [matchOutcome, matchScore, numSets, matchesPredicted, ageParams, surfaceParams, weightingParams] = Calibration(fileName1)
    data = [ageParams, surfaceParams, weightingParams, matchOutcome, matchScore, numSets, matchesPredicted]

    # Export data to a csv file for analysis and plotting purposes:
    ExportToCSV('CalibrationHard.csv', data)

    # Run the calibration:
    [matchOutcome, matchScore, numSets, matchesPredicted, ageParams, surfaceParams, weightingParams] = Calibration(fileName2)
    data = [ageParams, surfaceParams, weightingParams, matchOutcome, matchScore, numSets, matchesPredicted]

    # Export data to a csv file for analysis and plotting purposes:
    ExportToCSV('CalibrationGrass.csv', data)

    # Run the calibration:
    [matchOutcome, matchScore, numSets, matchesPredicted, ageParams, surfaceParams, weightingParams] = Calibration(fileName3)
    data = [ageParams, surfaceParams, weightingParams, matchOutcome, matchScore, numSets, matchesPredicted]

    # Export data to a csv file for analysis and plotting purposes:
    ExportToCSV('CalibrationClay.csv', data)

if __name__ == "__main__":
    main()