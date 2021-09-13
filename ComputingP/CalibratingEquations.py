import numpy as np
import scipy
from scipy.optimize import minimize
from CalculatingP import EvalEquations, ReadInGridDB
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

def ObjectiveFunction(parameters, DB, testDataFN, obj, equation):
    # This function computes the objective function (overall ROI) for eqautions 1 & 2 and a set of given hyperparameters
    objMetric = EvalEquations(DB, testDataFN, obj, [equation], parameters[0], parameters[1], parameters[2])
    value = (1*objMetric['Equation {}'.format(equation)]['Match Outcome']+3*objMetric['Equation {}'.format(equation)]
    ['Match Score'])/objMetric['Equation {}'.format(equation)]['Matches Predicted']#+objMetric['Equation 1']['Set Score']
    print("parameters : ")
    print( parameters)
    print(value)
    return -1*value

def ObjectiveFunction3(parameters, DB, testDataFN, obj, equation):
    objMetric = EvalEquations(DB, testDataFN, obj, [equation], parameters[0], parameters[1], parameters[2], parameters[3])
    value = (1*objMetric['Equation {}'.format(equation)]['Match Outcome']+3*objMetric['Equation {}'.format(equation)]
    ['Match Score'])/objMetric['Equation {}'.format(equation)]['Matches Predicted']#+objMetric['Equation 1']['Set Score']
    print("parameters : ")
    print( parameters)
    print(value)
    LISTOFOBJS.append(value)
    LISTOFPARAMS.append(parameters)
    global BESTCURRENTSOL
    if(value >= BESTCURRENTSOL):
        BESTCURRENTSOL = value
        LISTOFBESTOBJS.append(value)
    else:
        LISTOFBESTOBJS.append(BESTCURRENTSOL)
    return -1*value


def CalibrateHyperparameters(DB, testDataFN, obj, equation, eq3StartingPoints = []):
    # This function calibrates an given equation using a given objective metric on a given set of training data from various different
    # starting points.
    # Inputs:
    # - DB = The database of model distributions
    # - testDataFN = the filename corresponding to the test data csv file
    # - obj = the objective metric to use to calibrate hyperparameters ('Match Stats' or 'ROI')
    # - equation = the equation we are tuning

    # Returns:
    # - A set of calibrated hyperparameters

    startingPoints = []
    ageValues = [6, 9, 12]
    surfaceValues = [0.25, 0.5, 0.75]
    weightingValues = [0.25, 0.5, 0.75]
    thetaValues = [0.25, 0.5, 0.75]
    for valA in ageValues:
        for valS in surfaceValues:
            for valW in weightingValues:
                startingPoints.append([valA,valS,valW])

    # Track the best solution so far:
    bestSol = startingPoints[0]
    bestObj = 0
    allSolsObjs = []

    # Calibrate the hyperparameters for a range of different starting points:
    
    if (equation <= 2):
        for start in startingPoints:
            # Equation 1 or 2:
            optimizedResult = minimize(ObjectiveFunction,start,args=(DB,testDataFN,obj,equation),method='Nelder-Mead',bounds=[(4.,15.),(0.,1.),
            (0.,1.)])
            allSolsObjs.append((optimizedResult.x,optimizedResult.fun))
            # Check if the optimal solution is the best so far:
            if (optimizedResult.fun < bestObj):
                bestSol = optimizedResult.x
                bestObj = optimizedResult.fun
                print('New Best Solution Found')
                print('Objective Value is {}'.format(bestObj))
                print('New Solution is: Age = {}, Surface = {}, Weighting = {}'.format(bestSol[0],bestSol[1],bestSol[2]))
    else:
        for start in eq3StartingPoints:
            for valT in thetaValues:
                startingParams = start[0:3]
                startingParams.append(valT)
                # Equation 3:
                optimizedResult = minimize(ObjectiveFunction3,startingParams,args=(DB,testDataFN,obj,equation),method='Nelder-Mead',bounds=[(4.,15.),(0.,1.),
                (0.,1.),(0.,1.)])
                allSolsObjs.append((optimizedResult.x,optimizedResult.fun))
                # Check if the optimal solution is the best so far:
                if (optimizedResult.fun < bestObj):
                    bestSol = optimizedResult.x
                    bestObj = optimizedResult.fun
                    print('New Best Solution Found')
                    print('Objective Value is {}'.format(bestObj))
                    print('New Solution is: Age = {}, Surface = {}, Weighting = {}, Theta = {}'.format(bestSol[0],bestSol[1],bestSol[2], bestSol[3]))

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

def storePlottingData(fileName, eqNum):
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

def getStartParamsFromCSV(fileName):
    # Read in CSV file:
    StartingParams = []
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                if(row[0] == '2'):
                    params = [float(row[2]),float(row[3]),float(row[4])]
                    StartingParams.append(params)
                line_count += 1
                    
    
    return StartingParams



def main():
    DB = ReadInGridDB('ModelDistributions.csv')
    testDataFN = 'threeHundredCalMatches.csv'
    obj = 'Match Stats'
    equation = 3
    fileName = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\CalibratedParametersAllEquations.csv'
    fileName2 = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\CalibratedPlottingDataEq3.csv'
    startingPintsEq3 = getStartParamsFromCSV(fileName)
    #testSolObjs = [(np.array([6.15,0.25,0.25, 34]),-1.634),(np.array([4.56,0.565,0.56, 344]),-1.574),(np.array([8.17,0.67,0.5, 345]),-1.5),(np.array([6.15,0.56,0.87,34]),-1.987)]
    [bestSol,allSolsObjs] = CalibrateHyperparameters(DB, testDataFN, 'Match Stats', equation, startingPintsEq3)
    bestSolObjs = sorted(allSolsObjs,key = lambda x: x[1])[:6]
    # Get location of file:
    #THIS_FOLDER = os.path.abspath('CSVFiles')
    #fileName = os.path.join(THIS_FOLDER, fileName)
    print(bestSolObjs)
    buildCalibratedParamsDB(fileName, bestSolObjs, equation)
    storePlottingData(fileName2, equation)
    print(bestSol)
    print(allSolsObjs)

if __name__ == "__main__":
    main()