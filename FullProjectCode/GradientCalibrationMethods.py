import numpy as np
from Calibration import ObjectiveFunction, ObjectiveFunction3

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
    Grad = (ObjectiveFunction(xF) - ObjectiveFunction(xB)) / (2 * h)

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
    fxx = (ObjectiveFunction(xF) - 2 * ObjectiveFunction(x0) + ObjectiveFunction(xB)) / (pow(h,2))

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
    secondD = (ObjectiveFunction(xPos1Pos1) - ObjectiveFunction(xPos1Neg1) - ObjectiveFunction(xNeg1Pos1) + ObjectiveFunction(xPos1Pos1)) / (4 * h1 * h2)

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