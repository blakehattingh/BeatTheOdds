import numpy as np
import scipy
from scipy.optimize import minimize
from CalculatingP import EvalEquations, ReadInGridDB
import os
import csv
from csv import writer

LISTOFOBJS = []
LISTOFPARAMS = []
BESTCURRENTSOL = 0.
LISTOFBESTOBJS = []
FILENAME2 = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\CalibratedPlottingDataEq3.csv'

# Grid axes are as follows:
# x = Lambda
# y = Surface 
# z = Theta (Only needed for equation 3)

def FiniteDifferencesFirst(x0, dir, h):
    # This function approximates the gradient at the point x0 in the direction dir using the central finite differences with 
    # a step size of h.
    # Inputs:
    # - x0 = starting position
    # - dir = the direction of the gradient we are interested in (x, y or z)
    # - h = step size
    
    # Compute the point behind and in front of the current point:
    xB = x0
    xF = x0
    if (dir == 'x'):
        xB[0] = x0[0] - h
        xF[0] = x0[0] + h
    elif (dir == 'y'):
        xB[1] = x0[1] - h
        xF[1] = x0[1] + h
    else:
        xB[2] = x0[2] - h
        xF[2] = x0[2] + h

    # Estimate the gradient at x0 using central finite differences:
    Grad = (objFunction(xF) - objFunction(xB)) / (2 * h)

    return Grad

def FiniteDifferencesSecond(x0, dir, h):
    # This function approximates the 2nd derivative at the point x0 in the direction dir using the central finite differences with 
    # a step size of h.
    # Inputs:
    # - x0 = starting position
    # - dir = the direction of the gradient we are interested in (x, y or z)
    # - h = step size

    # Compute the point behind and in front of the current point:
    xB = x0
    xF = x0
    if (dir == 'x'):
        xB[0] = x0[0] - h
        xF[0] = x0[0] + h
    elif (dir == 'y'):
        xB[1] = x0[1] - h
        xF[1] = x0[1] + h
    else:
        xB[2] = x0[2] - h
        xF[2] = x0[2] + h

    # Estimate the 2nd derivative at x0 using central finite differences:
    fxx = (objFunction(xF) - 2 * objFunction(x0) + objFunction(xB)) / (pow(h,2))

    return fxx

def FiniteDifferencesMixed(x0, dir, h1, h2):
    # This function approximates the mixed 2nd-order partial derivative at the point x0 in the direction dir.
    # Inputs:
    # - x0 = starting position
    # - dir = the direction of the gradient we are interested in (xy, xz, yz)
    # - h1 and h2 = step sizes in the 1st and 2nd directions

    # Compute the 4 points required for the approximation:
    xNeg1Neg1 = x0
    xNeg1Pos1 = x0
    xPos1Neg1 = x0
    xPos1Pos1 = x0
    if (dir == 'xy'):
        xNeg1Neg1[0] = x0[0] - h1
        xNeg1Neg1[1] = x0[1] - h2
        xNeg1Pos1[0] = x0[0] - h1
        xNeg1Pos1[1] = x0[1] + h2
        xPos1Neg1[0] = x0[0] + h1
        xPos1Neg1[1] = x0[1] - h2
        xPos1Pos1[0] = x0[0] + h1
        xPos1Pos1[1] = x0[1] + h2
    elif (dir == 'xz'):
        xNeg1Neg1[0] = x0[0] - h1
        xNeg1Neg1[2] = x0[2] - h2
        xNeg1Pos1[0] = x0[0] - h1
        xNeg1Pos1[2] = x0[2] + h2
        xPos1Neg1[0] = x0[0] + h1
        xPos1Neg1[2] = x0[2] - h2
        xPos1Pos1[0] = x0[0] + h1
        xPos1Pos1[2] = x0[2] + h2
    elif (dir == 'yz'):
        xNeg1Neg1[1] = x0[1] - h1
        xNeg1Neg1[2] = x0[2] - h2
        xNeg1Pos1[1] = x0[1] - h1
        xNeg1Pos1[2] = x0[2] + h2
        xPos1Neg1[1] = x0[1] + h1
        xPos1Neg1[2] = x0[2] - h2
        xPos1Pos1[1] = x0[1] + h1
        xPos1Pos1[2] = x0[2] + h2

    # Estimate the 2nd derivative:
    secondD = (objFunction(xPos1Pos1) - objFunction(xPos1Neg1) - objFunction(xNeg1Pos1) + objFunction(xPos1Pos1)) / (4 * h1 * h2)

    return secondD

def ComputeGradF(x0, dim, h):
    # This function computes the gradient operator on a function at the point x0.
    # Inputs:
    # - x0 = the point we are computing the gradient at
    # - dim = the number of dimensions that we are interested in (2 or 3)
    # - h = step size

    gradF = np.zeros(dim, dtype = float)
    for d in range(dim):
        # Estimate the gradient:
        if (d == 0):
            gradF[d] = FiniteDifferencesFirst(x0, 'x', h)
        elif (d == 1):
            gradF[d] = FiniteDifferencesFirst(x0, 'y', h)
        else:
            gradF[d] = FiniteDifferencesFirst(x0, 'z', h)
    return gradF

def ComputeHess(x0, dim, h1, h2):
    # This function computes the hessian of a function at the point x0. (double derivatives)
    # Inputs:
    # - x0 = the point we are computing the gradient at
    # - dim = the number of dimensions that we are interested in (2 or 3)
    # - h = step size

    # Directions:
    dirs = ['x', 'y', 'z']

    Hess = np.zeros([dim,dim], dtype = float)
    # Compute 2nd derivatives:
    for row in range(dim):
        for col in range(dim):
            dir = dirs[row]+dir[col]
            if (row == col):
                Hess[row][col] = FiniteDifferencesSecond(x0, dir, h1)
            else:
                Hess[row][col] = FiniteDifferencesMixed(x0, dir, h1, h2)
    return Hess

def Newtowns(x0, dim, h, tol = 1e-06, maxit = 100):

    k = 0
    xk = x0
    while (k < maxit):
        # Compute gradF and the Hessian:
        gradF = ComputeGradF(xk, dim, h)
        hessian = ComputeHess(xk, dim, h, h)

        # Check if Marquartd's modification is required: (Hessian = negative (semi) definite)
        if (min(np.linalg.eigvals(hessian)) < 0):
            mu = max(1, 1.5 * abs(min(np.linalg.eigvals(hessian)))) * np.diag(dim)
        else:
            mu = 0 * np.diag(dim)
        
        # Compute Marquardt's modification:
        M = hessian + mu

        # Compute the search direciton:
        dk = np.linalg.solve(M,gradF)

        # Normalise direction:
        dk = dk / np.linalg.norm(dk)

        # Check for convergence: # consider changing to be difference in objectives
        if (np.linalg.norm(gradF) < tol):
            return xk
        
        # Compute the step length:
        alpha = h / 10.

        # Compute the next search point:
        xOld = xk
        xk = xOld + alpha * dk
        k += 1

    return xk

def ObjectiveFunction(parameters, testDataFN, obj, equation, riskProfile = [], betas = []):
    # This function computes the objective function (overall ROI / Match Stats) for eqautions 1 & 2 and a 
    # set of given hyperparameters.
    # Inputs:
    # - paramaeters: A set of parameters to use
    # - testDataFN: the filename for the test set of matches
    # - obj: Which objective metric is being used (either 'Match Stats' or 'ROI')
    # - equation: The equatio we are using, for this function it is either 1 or 2
    # - riskProfile and betas: Only needed when using ROI as objective, describes the users risk profile
    
    # Evaluate the equation on the test set:
    objMetric = EvalEquations(testDataFN, obj, [equation], parameters[0], parameters[1], parameters[2], riskProfile,
    betas)

    # Compute the objective metric:
    if (obj == 'Match Stats'):
        value = (1 * objMetric['Equation {}'.format(equation)]['Match Outcome'] + 3 * objMetric['Equation {}'.
        format(equation)]['Match Score']) / objMetric['Equation {}'.format(equation)]['Matches Predicted']
    elif (obj == 'ROI'):
        # Compute the overall ROI:
        value = ((objMetric['Equation {}'.format(equation)]['Returns'] - objMetric['Equation {}'.format(equation)]
        ['Betted']) / objMetric['Equation {}'.format(equation)]['Betted']) * 100.
        
    # Print the parameters used and the objective value:
    print("parameters : ")
    print( parameters)
    print(objMetric['Equation {}'.format(equation)]['Matches Predicted'])
    print(value)

    # Collect and store the plotting data:
    LISTOFOBJS.append(value)
    LISTOFPARAMS.append(parameters)
    global BESTCURRENTSOL
    if(value >= BESTCURRENTSOL):
        BESTCURRENTSOL = value
        LISTOFBESTOBJS.append(value)
    else:
        LISTOFBESTOBJS.append(BESTCURRENTSOL) 

    # Minimising so return the negative of the value:
    return -1 * value

def ObjectiveFunction3(parameters, testDataFN, obj, riskProfile = [], betas = []):
    # This function computes the objective function (overall ROI / Match Stats) for eqautions 1 & 2 and a 
    # set of given hyperparameters.
    # Inputs:
    # - paramaeters: A set of parameters to use
    # - testDataFN: the filename for the test set of matches
    # - obj: Which objective metric is being used (either 'Match Stats' or 'ROI')
    # - riskProfile and betas: Only needed when using ROI as objective, describes the users risk profile

    # Evaluate the equation on the test set:
    objMetric = EvalEquations(testDataFN, obj, [3], parameters[0], parameters[1], parameters[2], parameters[3],
    riskProfile, betas)

    # Compute the objective metric:
    if (obj == 'Match Stats'):
        value = (1 * objMetric['Equation 3']['Match Outcome'] + 3 * objMetric['Equation 3']['Match Score']) / objMetric['Equation 3']['Matches Predicted']
    elif (obj == 'ROI'):
        # Compute the overall ROI:
        value = ((objMetric['Equation 3']['Returns'] - objMetric['Equation 3']['Betted']) / objMetric['Equation 3']['Betted']) * 100.
        
    # Print the parameters used and the objective value:
    print("parameters : ")
    print( parameters)
    print(value)

    # Collect and store the plotting data:
    LISTOFOBJS.append(value)
    LISTOFPARAMS.append(parameters)
    global BESTCURRENTSOL
    if(value >= BESTCURRENTSOL):
        BESTCURRENTSOL = value
        LISTOFBESTOBJS.append(value)
    else:
        LISTOFBESTOBJS.append(BESTCURRENTSOL) 

    # Minimising so return the negative of the value:
    return -1 * value

def CalibrateHyperparameters(testDataFN, obj, equation, startingPoints, riskProfile = [], betas = []):
    # This function calibrates an given equation using a given objective metric on a given set of training data from various different
    # starting points.
    # Inputs:
    # - testDataFN = the filename corresponding to the test data csv file
    # - obj = the objective metric to use to calibrate hyperparameters ('Match Stats' or 'ROI')
    # - equation = the equation we are tuning
    # - startingPoints = a list of parameters to start from, if not supplied then we use the standard ones    
    # # - riskProfile and betas: Only needed when using ROI as objective, describes the users risk profile

    # Returns:
    # - A set of calibrated hyperparameters
    
    # Track the best solution so far:
    bestSol = startingPoints[0]
    bestObj = 0
    allSolsObjs = []

    # Calibrate the hyperparameters for a range of different starting points:
    for start in startingPoints:
        if (equation <= 2):
            # Equation 1 or 2:
            optimizedResult = minimize(ObjectiveFunction,start,args=(testDataFN,obj,equation,riskProfile,betas),
            method='Nelder-Mead',bounds=[(1.,15.),(0.,1.),(0.,1.)])
            allSolsObjs.append((optimizedResult.x,optimizedResult.fun))

            # Check if the optimal solution is the best so far:
            if (optimizedResult.fun < bestObj):
                bestSol = optimizedResult.x
                bestObj = optimizedResult.fun
                print('New Best Solution Found')
                print('Objective Value is {}'.format(bestObj))
                print('New Solution is: Age = {}, Surface = {}, Weighting = {}'.format(bestSol[0],bestSol[1],
                bestSol[2]))
        else:
            # Equation 3:
            optimizedResult = minimize(ObjectiveFunction3,start,args=(testDataFN,obj,riskProfile,betas),
            method='Nelder-Mead',bounds=[(1.,15.),(0.,1.),(0.,1.),(0.,1.)])
            allSolsObjs.append((optimizedResult.x,optimizedResult.fun))

            # Check if the optimal solution is the best so far:
            if (optimizedResult.fun < bestObj):
                bestSol = optimizedResult.x
                bestObj = optimizedResult.fun
                print('New Best Solution Found')
                print('Objective Value is {}'.format(bestObj))
                print('New Solution is: Age = {}, Surface = {}, Weighting = {}, Theta = {}'.format(bestSol[0],
                bestSol[1],bestSol[2], bestSol[3]))

    return [bestSol, allSolsObjs]

def buildCalibratedParamsDB(fileName, bestSolObjs, eqNum):
    # Open CSV file in append mode:
    with open(fileName, 'a', newline='') as csv_file:
        writer_obj = writer(csv_file) 
        for bestSolObj in bestSolObjs:
            row= [eqNum]
            row.append(bestSolObj[1])
            paramters = bestSolObj[0].tolist() 
            for param in paramters:
                row.append(param)
            writer_obj.writerow(row)
        csv_file.close()

def storePlottingDataCalibration(fileName, eqNum):
    with open(fileName, 'a', newline='') as csv_file:
        writer_obj = writer(csv_file)  
        writer_obj.writerow(LISTOFBESTOBJS)
        writer_obj.writerow(LISTOFOBJS)
        param1 =[]
        param2 =[]
        param3 = []
        param4 = []
        for i in range(len(LISTOFPARAMS)):
            param1.append(LISTOFPARAMS[i][0])
            param2.append(LISTOFPARAMS[i][1])
            param3.append(LISTOFPARAMS[i][2]) 
            if (eqNum == 3):
                param4.append(LISTOFPARAMS[i][3])
        writer_obj.writerow(param1)
        writer_obj.writerow(param2)
        writer_obj.writerow(param3)
        if(eqNum == 3):
            writer_obj.writerow(param4)
        csv_file.close()

def getCalibratedParamsFromCSV(eqNum,fromEq,thetas=[], fileName = ''):
    startingPoints = []
    #create starting points
    if(fileName == ''):
        ageValues = [2, 4]
        surfaceValues = [0.25, 0.5, 0.75]
        weightingValues = [0.25, 0.5, 0.75]
        thetaValues = [0.25, 0.5, 0.75]
        for valA in ageValues:
            for valS in surfaceValues:
                for valW in weightingValues:
                    if (eqNum == 3):
                        for valT in thetaValues:
                            startingPoints.append([valA,valS,valW,valT])
                    else:
                        startingPoints.append([valA,valS,valW])
    else:
        # Read in CSV file:
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    if(row[0] == str(fromEq)):
                        if(eqNum == 3):
                            if(fromEq != 3):
                                for theta in thetas:
                                    params = [float(row[2]),float(row[3]),float(row[4]), theta]
                                    startingPoints.append(params)
                            else:
                                params = [float(row[2]),float(row[3]),float(row[4]), float(row[5])]
                                startingPoints.append(params)
                        else:
                            params = [float(row[2]),float(row[3]),float(row[4])]
                            startingPoints.append(params)
                    line_count += 1
        
    return startingPoints

def storePlottingDataTesting(fileName, values, equation):
    # Open a new CSV file to write to:
    with open(fileName, mode = 'a') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in values.items():
            writer.writerow([equation, key, value])
        csv_file.close()

def TestEquations(testDataFN, calibratedParms, obj, equation, riskProfile = [], betas = []):
    # This function takes in a set of calibrated parameters for a given equation and computes a specified objective 
    # metric for each set on the given data set.
    # Inputs:
    # - testDataFN: The filename of the testdata in CSVFiles
    # - calibratedParms: A list of sets of calibrated parameters to use, it also includes the equation number
    # - obj: The objective metric we will be using (either 'Match Stats' or 'ROI')
    # - equation: The equation we are testing
    # - riskProfile and betas: Only needed when using ROI as objective, describes the users risk profile

    # Create a dictionary to store the objective value for each set of parameters:
    objValues = {}

    # Iterate through each set of parameters:
    for set in calibratedParms:
        # Compute the objective metric for this set:
        if (equation == 3):
            # Extract the parameters:
            parameters = [set[0],set[1],set[2],set[3]]

            # Compute the objective value:
            objValues[((round(set[0],3),round(set[1],3),round(set[2],3),round(set[3],3)))] = ObjectiveFunction3(parameters, 
            testDataFN, obj, riskProfile, betas)
        else:
            # Extract the parameters:
            parameters = [set[0],set[1],set[2]]
            objValues[((round(set[0],3),round(set[1],3),round(set[2],3)))] = ObjectiveFunction(parameters, 
            testDataFN, obj, equation, riskProfile, betas)

    return objValues

def main():
    # Set up file names:
    person = 'Blake'
    
    if (person == 'Blake'):
        #trainingDataFN = 'threeHundredCalMatches.csv'
        trainingDataFN = 'trainingSetForCalibrationWithROI.csv'
        testDataFN = 'hundredCalMatches.csv'
        #fileName = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\CalibratedParametersAllEquations.csv'
        #fileName = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\CalibratedParametersAllEquations2.csv'
        fileName = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\CalibratedParametersROI.csv'
        #fileName2 = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\CalibratedPlottingDataEq3.csv'
        #fileName2 = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\CalibratedPlottingDataRound2.csv'
        fileName2 = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\CalibratedPlottingDataROI.csv'
        fileName3 = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\ObjectiveValuesForCalibratedParametersRound2.csv'
        fileNameFinalCal = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\FinalCalibratedParametersAllEquations.csv'
    elif (person == 'Campbell'):
        # Get location of file:
        THIS_FOLDER = os.path.abspath('CSVFiles')
        fileName = os.path.join(THIS_FOLDER, 'CalibratedParametersAllEquations.csv')
        fileName2 = os.path.join(THIS_FOLDER, 'CalibratedPlottingDataEq3.csv')
        fileName3 = os.path.join(THIS_FOLDER, 'ObjectiveValuesForCalibratedParameters.csv')

    # What are we doing? (Calibrated or testing? Match Stats or ROI? What equation?)
    purpose = 'Calibration'
    obj = 'ROI'
    equation = [2]
    fromEquation = 2
    riskProfile = [1.,1.,1.]
    betas = [0.2, 1./3., 0.5]
    thetas = [0.25,0.5,0.75]

    if (purpose == 'Calibration'):
        for eq in equation:

            # Calibrate the specified equation with the given objective metric:
            if (eq <= 2):
                startingPoints = getCalibratedParamsFromCSV(eq, eq)
                [bestSol,allSolsObjs] = CalibrateHyperparameters(trainingDataFN, obj, eq,startingPoints, riskProfile, betas)
                bestSolObjs = sorted(allSolsObjs,key = lambda x: x[1])[:6]
                buildCalibratedParamsDB(fileName, bestSolObjs, eq)
                storePlottingDataCalibration(fileName2, eq)
            elif (eq == 3):
                # Get the starting points from the calibrated parameters for eq 2:
                startingPoints = getCalibratedParamsFromCSV(eq,fromEquation,thetas, fileName)
                [bestSol,allSolsObjs] = CalibrateHyperparameters(trainingDataFN, obj, eq, startingPoints, 
                riskProfile, betas)
                bestSolObjs = sorted(allSolsObjs,key = lambda x: x[1])[:6]
                buildCalibratedParamsDB(fileName, bestSolObjs, eq)
                storePlottingDataCalibration(fileName2, eq)

        # Print the best set of calibrated parameters and their respective objective values:
        print(bestSol)
        print(allSolsObjs)
    
    elif (purpose == 'Testing'):
        for eq in equation:
            # Read in the calibrated parameters to test:
            calibratedParams = getCalibratedParamsFromCSV(eq,eq,fileName=fileNameFinalCal)
            # Test the equation:
            objectiveValues = TestEquations(testDataFN, calibratedParams , obj, eq, riskProfile, betas)

            # Store the values for each set of calibrated parameters for plotting:
            storePlottingDataTesting(fileName3, objectiveValues, eq)

if __name__ == "__main__":
    main()