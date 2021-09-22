import numpy as np
import csv
import os, sys

def BiLinearInterp(PCombo1, PCombo2, PCombo3, PCombo4, allDists = True):
    # Takes in 4 corner points with corresponding distributions and computes their average
    # Assumes an equally weighted averaged is required

    if (allDists):
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
    else:
        # Match Score Distribution:
        AvMatchScoreDist = ComputeAverageArray([PCombo1['Match Score'],PCombo2['Match Score'],PCombo3['Match Score'],
        PCombo4['Match Score']])    

        # Create dictionary of average distributions:
        AvDists = {'Match Score': AvMatchScoreDist}

    return AvDists

def LinearInterp(PCombo1, PCombo2, allDists = True, EvenWeight = True, Weighting = 0.5):
    # Takes in 2 points either sidewith corresponding distributions and computes their average
    # Assumes an equally weighted averaged is required unless specified otherwise

    if (allDists):
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
    else:
        if (EvenWeight):
            # Match Score Distribution:
            AvMatchScoreDist = ComputeAverageArray([PCombo1['Match Score'],PCombo2['Match Score']])
        else:
            # Match Score Distribution:
            AvMatchScoreDist = WeightedAverage([PCombo1['Match Score'],PCombo2['Match Score']],Weighting)

    if (allDists):
        # Create dictionary of average distributions:
        AvDists = {'Match Outcome': AvMatchOutcomeDist, 'Match Score': AvMatchScoreDist, 'Number of Games': AvNumGamesDist,
        'Set Score': AvSetScoreDist}
    else:
        AvDists = {'Match Score': AvMatchScoreDist}
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

def InterpolateDists(Pa, Pb, DB, pBoundaryL = 0.4, pBoundaryH = 0.8, Spacing = 0.02):
    # Takes in a set of P values and returns the interpolated distributions for them
    # Grid:
    # A ----E- B
    # |     x  |
    # |        |
    # C ----F- D
    
    # Ensure Pa and Pb are within bounds of the DB:
    if (Pa < pBoundaryL):
        if (Pb < pBoundaryL):
            ZDists = {}
            for dist in DB[(pBoundaryL,pBoundaryL)]:
                # Convert distributions to arrays:
                pCorner = np.array(DB[(round(pBoundaryL,2),round(pBoundaryL,2))][dist])
                PaNext = np.array(DB[(round(pBoundaryL+Spacing,2),round(pBoundaryL,2))][dist])
                PbNext = np.array(DB[(round(pBoundaryL,2),round(pBoundaryL+Spacing,2))][dist])

                # Extrapolate to this point:
                ZDists[dist] = np.subtract(pCorner, ((pBoundaryL - Pa) * np.subtract(PaNext, pCorner) / Spacing))
                ZDists[dist] = np.subtract(ZDists[dist], ((pBoundaryL - Pb) * np.subtract(PbNext, pCorner) / Spacing))
                
                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists
        else:
            ZDists = {}
            for dist in DB[(pBoundaryL,pBoundaryL)]:
                # Find the points above and below the point:
                roundedB = round(Pb, 1)
                if (roundedB > Pb):
                    roundedB -= 0.1
                while (roundedB <= Pb):
                    PbBefore = round(roundedB,2)
                    roundedB += Spacing

                # Get the two sides: (A before it, B is after it on the edge of our grid)
                pBefore = (round(pBoundaryL,2), round(PbBefore,2))
                pAfter = (round(pBoundaryL,2), round(PbBefore + Spacing,2))

                # Compute gradient between A and B:
                gradPb = (np.subtract(np.array(DB[pAfter][dist]), np.array(DB[pBefore][dist]))) / Spacing

                # Compute gradient to extrapolate out to this point:
                gradPa = (np.subtract(np.array(DB[(round(pBoundaryL + Spacing,2),PbBefore)][dist]),np.array(DB[pBefore][dist]))) / Spacing

                # Extrapolate to this point:
                ZDists[dist] = DB[pBefore][dist] - (pBoundaryL - Pa) * gradPa + (Pb - PbBefore) * gradPb

                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists
    else:
        if (Pb < pBoundaryL):
            ZDists = {}
            for dist in DB[(pBoundaryL,pBoundaryL)]:
                # Find the points above and below the point:
                roundedA = round(Pa, 1)
                if (roundedA > Pa):
                    roundedA -= 0.1
                while (roundedA <= Pa):
                    PaBefore = round(roundedA,2)
                    roundedA += Spacing

                # Get the two sides: (A before it, B is after it on the edge of our grid)
                pBefore = (round(PaBefore,2),round(pBoundaryL,2))
                pAfter = (round(PaBefore + Spacing,2),round(pBoundaryL,2))

                # Compute gradient between A and B:
                gradPa = (np.subtract(np.array(DB[pAfter][dist]), np.array(DB[pBefore][dist]))) / Spacing

                # Compute gradient to extrapolate out to this point:
                gradPb = (np.subtract(np.array(DB[(PaBefore, round(pBoundaryL+Spacing,2))][dist]),np.array(DB[pBefore][dist]))) / Spacing

                # Extrapolate to this point:
                ZDists[dist] = DB[pBefore][dist] - (pBoundaryL - Pb) * gradPb + (Pa - PaBefore) * gradPa

                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists

    if (Pa > pBoundaryH):
        if (Pb > pBoundaryH):
            ZDists = {}
            for dist in DB[(pBoundaryH,pBoundaryH)]:
                # Convert distributions to arrays:
                pCorner = np.array(DB[(round(pBoundaryH,2),round(pBoundaryH,2))][dist])
                PaBefore = np.array(DB[(round(pBoundaryH-Spacing,2),round(pBoundaryH,2))][dist])
                PbBefore = np.array(DB[(round(pBoundaryH,2),round(pBoundaryH-Spacing,2))][dist])

                # Extrapolate to this point:
                ZDists[dist] = np.subtract(pCorner, ((pBoundaryH - Pa) * np.subtract(pCorner, PaBefore) / Spacing))
                ZDists[dist] = np.subtract(ZDists[dist], ((pBoundaryH - Pb) * np.subtract(pCorner, PbBefore) / Spacing))
                
                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists
        else:
            ZDists = {}
            for dist in DB[(pBoundaryH,pBoundaryH)]:
                # Find the points above and below the point:
                roundedB = round(Pb, 1)
                if (roundedB > Pb):
                    roundedB -= 0.1
                while (roundedB <= Pb):
                    PbBefore = round(roundedB,2)
                    roundedB += Spacing

                # Get the two sides: (A before it, B is after it on the edge of our grid)
                pBefore = (round(pBoundaryH,2), round(PbBefore,2))
                pAfter = (round(pBoundaryH,2), round(PbBefore + Spacing,2))

                # Compute gradient between A and B:
                gradPb = (np.subtract(np.array(DB[pAfter][dist]), np.array(DB[pBefore][dist]))) / Spacing

                # Compute gradient to extrapolate out to this point:
                gradPa = (np.subtract(np.array(DB[pBefore][dist]),np.array(DB[(round(pBoundaryH - Spacing,2),PbBefore)][dist]))) / Spacing

                # Extrapolate to this point:
                ZDists[dist] = DB[pBefore][dist] + (Pa - pBoundaryH) * gradPa + (Pb - PbBefore) * gradPb

                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists
    else:
        if (Pb > pBoundaryH):
            ZDists = {}
            for dist in DB[(pBoundaryH,pBoundaryH)]:
                # Find the points above and below the point:
                roundedA = round(Pa, 1)
                if (roundedA > Pa):
                    roundedA -= 0.1
                while (roundedA <= Pa):
                    PaBefore = round(roundedA,2)
                    roundedA += Spacing

                # Get the two sides: (A before it, B is after it on the edge of our grid)
                pBefore = (round(PaBefore,2),round(pBoundaryH,2))
                pAfter = (round(PaBefore + Spacing,2),round(pBoundaryH,2))

                # Compute gradient between A and B:
                gradPa = (np.subtract(np.array(DB[pAfter][dist]), np.array(DB[pBefore][dist]))) / Spacing

                # Compute gradient to extrapolate out to this point:
                gradPb = (np.subtract(np.array(DB[(PaBefore, round(pBoundaryH,2))][dist]),np.array(DB[(PaBefore,round(pBoundaryH-Spacing,2))][dist]))) / Spacing

                # Extrapolate to this point:
                ZDists[dist] = DB[pBefore][dist] + (Pb - pBoundaryH) * gradPb + (Pa - PaBefore) * gradPa

                # Convert it back to a list:
                ZDists[dist].tolist()

            return ZDists

    # Compute the base point for the 4 points around this point (Point A):
    roundedA = round(Pa, 1)
    roundedB = round(Pb, 1)
    if (roundedA > Pa):
        roundedA -= 0.1
    if (roundedB > Pb):
        roundedB -= 0.1
    while (roundedA <= Pa):
            APointA = roundedA
            roundedA += Spacing
    while (roundedB <= Pb):
        APointB = roundedB
        roundedB += Spacing
    APointA = round(APointA,2)
    APointB = round(APointB,2)

    # Extract the distribtions for all 4 corner points:
    ADists = DB[(APointA,APointB)]
    BDists = DB[(round((APointA+0.02),2), APointB)]
    CDists = DB[(APointA, round((APointB+0.02),2))]
    DDists = DB[(round((APointA+0.02),2),round((APointB+0.02),2))]

    # Compute the weighting between side points (alpha) and bottom and top points (beta):
    [alpha, beta] = ComputeWeighting(Pa, Pb)

    # Extract the average distributions along each side:
    XDists = {}
    for dist in ADists:
        EDists = WeightedAverage(ADists[dist], BDists[dist], alpha)
        FDists = WeightedAverage(CDists[dist], DDists[dist], alpha)
        XDists[dist] = WeightedAverage(EDists, FDists, beta)

    return XDists