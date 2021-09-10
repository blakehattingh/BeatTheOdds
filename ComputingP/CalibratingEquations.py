import numpy as np
import scipy
from scipy.optimize import minimize
from CalculatingP import EvalEquations, ReadInGridDB

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
    value = 3*objMetric['Equation 1']['Match Outcome']+objMetric['Equation 1']['Set Score']+5*objMetric['Equation 1']['Match Score']
    print("parameters : ")
    print( parameters)
    print(value)
    return -1*value

def ObjectiveFunction3(parameters, DB, testDataFN, obj, equation):
    return EvalEquations(DB, testDataFN, obj, [equation], parameters[0], parameters[1], parameters[2], parameters[3])

def CalibrateHyperparameters(DB, testDataFN, obj, equation, x0):
    # This function calibrates an given equation using a given objective metric on a given set of training data.
    # Inputs:
    # - DB = The database of model distributions
    # - testDataFN = the filename corresponding to the test data csv file
    # - obj = the objective metric to use to calibrate hyperparameters ('Match Stats' or 'ROI')
    # - equation = the equation we are tuning
    # - x0 = the starting values for the hyperparameters we are trying to train

    # Returns:
    # - A set of calibrated hyperparameters

    if (equation <= 2):
        # Equation 1 or 2:
        sol = minimize(ObjectiveFunction,x0,args=(DB,testDataFN,obj,equation),method='Nelder-Mead',bounds=[(4.,12.),(0.,1.),
        (0.,1.)])
    else:
        # Equation 3:
        sol = minimize(ObjectiveFunction3,x0,args=(DB,testDataFN,obj,equation),method='Nelder-Mead',bounds=[(4.,12.),(0.,1.),
        (0.,1.),(0.,1.)])
    return sol

def main():
    x0 = [6, 0.5, 0.5]
    DB = ReadInGridDB('ModelDistributions.csv')
    testDataFN = 'threeHundredCalMatches.csv'
    obj = 'Match Stats'
    equation = 1
    solution = CalibrateHyperparameters(DB, testDataFN, 'Match Stats', equation, x0)

if __name__ == "__main__":
    main()