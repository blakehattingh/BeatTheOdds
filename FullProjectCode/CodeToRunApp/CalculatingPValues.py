import numpy as np

def CalcPEquation(matchDetails,equation,calibratedParams,PrevMatches,PrevMatchesCommA,PrevMatchesCommB,CommonOpps):
    # This function computes the respective P values for two opponents playing on a specified surface.

    # Inputs:
    # - matchDetails: A list of required match details (P1ID, P2ID, Date of Match, Surface being Played on)
    # - equation: What equation we will use to compute P
    # - calibratedParams: A list of hyperparameters to use to compute P (Age, Surface, Weightin, Theta if needed)
    # - PrevMatches = The previous matches between the players playing in the match
    # - PrevMatchesCommA / B = The matches between player A / B and the common opponents
    # - CommonOpps = A list of common opponent IDs

    # Returns:
    # - Pa and Pb
    # - Return Message: An integer relating to one of the following:
    #   - 1: Confident in Estimates
    #   - 2: Estimated P Values ONLY use Common Opponent(s) data
    #   - 3: Estimated P Values ONLY use Historic data between the two
    #   - 4: No Historic data between the two players therefore, NOT comfortable using the estimates to bet

    # Extract required info:
    PlayerA = int(matchDetails[0])
    PlayerB = int(matchDetails[1])
    dateOfMatch = matchDetails[2]
    surfaceOfMatch = matchDetails[3]

    # Extract calibrated parameters:
    age = calibratedParams[0]
    surface = calibratedParams[1]
    weighting = calibratedParams[2]
    if (equation == 3):
        theta = calibratedParams[3]
   
    # See how many matches have been played between A and B:
    numMatches = len(PrevMatches)

    # Check if we have sufficient historical data to make predictions:
    if (numMatches == 0):
        if (len(CommonOpps) == 0):
            # We have no data to use to compute P, thus do NOT compute it:
            return [0.5,0.5,4]
        else:
            # Compute SPW(A,C) and SPW(B,C):
            [spwAC, rpwAC] = ComputeSPWCommon(PlayerA, PrevMatchesCommA, CommonOpps, surface, surfaceOfMatch) 
            [spwBC, rpwBC] = ComputeSPWCommon(PlayerB, PrevMatchesCommB, CommonOpps, surface, surfaceOfMatch)

            # Compute PaS and PbS:
            PaS = spwAC
            PbS = spwBC

            # Compute PaR and PbR:
            PaR = rpwAC
            PbR = rpwBC

            # Compute P using the equation specified:
            if (equation == 1):
                Pa = PaS
                Pb = PbS
            elif (equation == 2):
                Pa = PaS / (PaS + PbR)
                Pb = PbS / (PbS + PaR)
            else:
                Pa = PaS * (1. - theta) + theta * (1. - PbR)
                Pb = PbS * (1. - theta) + theta * (1. - PaR)
            return [Pa, Pb, 2]
    else:
        if (len(CommonOpps) == 0):
            # No common opponents, but they have played before: (rare occurence)
            [spwAB, spwBA] = ComputeSPW(PlayerA, PlayerB, PrevMatches, surface, surfaceOfMatch)

            # Compute RPW(A,B) and RPW(B,A)
            rpwAB = 1. - spwBA
            rpwBA = 1. - spwAB       

            # Compute PaS and PbS:
            PaS = spwAB
            PbS = spwBA

            # Compute PaR and PbR:
            PaR = rpwAB
            PbR = rpwBA

            # Compute P using the equation specified:
            if (equation == 1):
                Pa = PaS
                Pb = PbS
            elif (equation == 2):
                Pa = PaS / (PaS + PbR)
                Pb = PbS / (PbS + PaR)
            else:
                Pa = PaS * (1. - theta) + theta * (1. - PbR)
                Pb = PbS * (1. - theta) + theta * (1. - PaR)
            return [Pa, Pb, 3]
        else:
            # Compute SPW(A,B) and SPW(B, A):
            [spwAB, spwBA] = ComputeSPW(PlayerA, PlayerB, PrevMatches, surface, surfaceOfMatch)

            # Compute RPW(A,B) and RPW(B,A)
            rpwAB = 1. - spwBA
            rpwBA = 1. - spwAB

            # Compute SPW(A,C) and SPW(B,C):
            [spwAC, rpwAC] = ComputeSPWCommon(PlayerA, PrevMatchesCommA, CommonOpps, surface, surfaceOfMatch) 
            [spwBC, rpwBC] = ComputeSPWCommon(PlayerB, PrevMatchesCommB, CommonOpps, surface, surfaceOfMatch)

            # Compute PaS and PbS:
            PaS = (1  - weighting) * spwAB + weighting * spwAC
            PbS = (1  - weighting) * spwBA + weighting * spwBC

            # Compute PaR and PbR:
            PaR = (1  - weighting) * rpwAB + weighting * rpwAC
            PbR = (1  - weighting) * rpwBA + weighting * rpwBC

            # Compute P using the equation specified:
            if (equation == 1):
                Pa = PaS
                Pb = PbS
            elif (equation == 2):
                Pa = PaS / (PaS + PbR)
                Pb = PbS / (PbS + PaR)
            else:
                Pa = PaS * (1. - theta) + theta * (1. - PbR)
                Pb = PbS * (1. - theta) + theta * (1. - PaR)        
        
            return [Pa, Pb, 1]

def ComputeSPW(PlayerA, PlayerB, PrevMatches, surface, surfaceOfMatch):
    # Inputs:
    # - PlayerA & PlayerB = IDs of both players of interest 
    # - PrevMatches = A list of tuples / lists of all previous matches between player A and player B
    # - surface = A hyperparameter corresponding to the weighting on matches played on the same surface
    # - surfaceOfMatch = The surface that the match will be played on (as an abbrev, e.g. C = Clay)

    # Sum up the service points played for each player:
    PlayerAServePointsSurface = 0
    PlayerAServePointsWonSurface = 0
    PlayerBServePointsSurface = 0
    PlayerBServePointsWonSurface = 0
    PlayerAServePointsNS = 0
    PlayerAServePointsWonNS = 0
    PlayerBServePointsNS = 0
    PlayerBServePointsWonNS = 0

    # Check how many matches are being analysed:
    nonSurfaceMatchesCount = 0
    surfaceMatchesCount = 0

    for match in range(len(PrevMatches)):
        # Ensure the match has statistics:
        if (PrevMatches[match][42] != None):
            if (PrevMatches[match][4] == surfaceOfMatch):
                surfaceMatchesCount += 1
                if (PrevMatches[match][8] == PlayerA):
                    PlayerAServePointsSurface += PrevMatches[match][42]
                    PlayerAServePointsWonSurface += (PrevMatches[match][44] + PrevMatches[match][45])
                    PlayerBServePointsSurface += PrevMatches[match][51]
                    PlayerBServePointsWonSurface += (PrevMatches[match][53] + PrevMatches[match][54])
                else:
                    PlayerAServePointsSurface += PrevMatches[match][51]
                    PlayerAServePointsWonSurface += (PrevMatches[match][53] + PrevMatches[match][54])
                    PlayerBServePointsSurface += PrevMatches[match][42]
                    PlayerBServePointsWonSurface += (PrevMatches[match][44] + PrevMatches[match][45])
            else:
                nonSurfaceMatchesCount += 1
                if (PrevMatches[match][8] == PlayerA):
                    PlayerAServePointsNS += PrevMatches[match][42]
                    PlayerAServePointsWonNS += (PrevMatches[match][44] + PrevMatches[match][45])
                    PlayerBServePointsNS += PrevMatches[match][51]
                    PlayerBServePointsWonNS += (PrevMatches[match][53] + PrevMatches[match][54])
                else:
                    PlayerAServePointsNS += PrevMatches[match][51]
                    PlayerAServePointsWonNS += (PrevMatches[match][53] + PrevMatches[match][54])
                    PlayerBServePointsNS += PrevMatches[match][42]
                    PlayerBServePointsWonNS += (PrevMatches[match][44] + PrevMatches[match][45])
    
    #print('Number of Previous Matches: ', len(PrevMatches))
    # Check if any matches were analysed:
    if (surfaceMatchesCount > 0):
        # Compute the proportion of service points won on the surface:
        PlayerAServicePropSurface = PlayerAServePointsWonSurface / PlayerAServePointsSurface
        PlayerBServicePropSurface = PlayerBServePointsWonSurface / PlayerBServePointsSurface
    else:
        PlayerAServicePropSurface = 0
        PlayerBServicePropSurface = 0

    if (nonSurfaceMatchesCount > 0):
        PlayerAServicePropNS = PlayerAServePointsWonNS / PlayerAServePointsNS
        PlayerBServicePropNS = PlayerBServePointsWonNS / PlayerBServePointsNS
    else:
        PlayerAServicePropNS = 0
        PlayerBServicePropNS = 0
        
    if ((surfaceMatchesCount > 0) and (nonSurfaceMatchesCount > 0)):
        PlayerAServiceProp = (1 - surface) * PlayerAServicePropSurface + surface * PlayerAServicePropNS
        PlayerBServiceProp = (1 - surface) * PlayerBServicePropSurface + surface * PlayerBServicePropNS
    else:
        PlayerAServiceProp = PlayerAServicePropSurface + PlayerAServicePropNS
        PlayerBServiceProp = PlayerBServicePropSurface + PlayerBServicePropNS

    return PlayerAServiceProp, PlayerBServiceProp

def ComputeSPWCommon(PlayerA, PrevMatchesCommOpps, CommonOpps, surface, surfaceOfMatch):    
    # Inputs:
    # - PlayerA = ID of both player A
    # - PrevMatchesCommOpps = A list of tuples / list of all previous matches between player A the common opponents
    # - CommonOpps = A list of the IDs of all common opponents
    # - surface = A hyperparameter corresponding to the weighting on matches played on the same surface
    # - surfaceOfMatch = The surface that the match will be played on (as an abbrev, e.g. C = Clay)

    # Sum up the service points played for each player:
    PlayerAServePointsSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAServePointsWonSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAServePointsNS = np.zeros(len(CommonOpps), dtype = int)
    PlayerAServePointsWonNS = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsWonSurface = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsNS = np.zeros(len(CommonOpps), dtype = int)
    PlayerAReturnPointsWonNS = np.zeros(len(CommonOpps), dtype = int)

    # Check how many matches are being analysed:
    surfaceMatchesCount = np.zeros(len(CommonOpps), dtype = float)
    nonSurfaceMatchesCount = np.zeros(len(CommonOpps), dtype = float)

    for match in range(len(PrevMatchesCommOpps)):
        # Make sure the match has statistics:
        if (PrevMatchesCommOpps[match][42] != None):
            if (surfaceOfMatch == PrevMatchesCommOpps[match][4]):
                if (PrevMatchesCommOpps[match][8] == PlayerA):
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][18])
                    PlayerAServePointsSurface[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAServePointsWonSurface[Opp] += (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45])
                    PlayerAReturnPointsSurface[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAReturnPointsWonSurface[Opp] += (PrevMatchesCommOpps[match][51] - (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54]))
                    surfaceMatchesCount[Opp] += 1
                else:
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][8])
                    PlayerAServePointsSurface[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAServePointsWonSurface[Opp] += (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54])
                    PlayerAReturnPointsSurface[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAReturnPointsWonSurface[Opp] += (PrevMatchesCommOpps[match][42] - (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45]))
                    surfaceMatchesCount[Opp] += 1
            else:
                if (PrevMatchesCommOpps[match][8] == PlayerA):
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][18])
                    PlayerAServePointsNS[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAServePointsWonNS[Opp] += (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45])
                    PlayerAReturnPointsNS[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAReturnPointsWonNS[Opp] += (PrevMatchesCommOpps[match][51] - (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54]))
                    nonSurfaceMatchesCount[Opp] += 1
                else:
                    # Find who the opponent was:
                    Opp = CommonOpps.index(PrevMatchesCommOpps[match][8])
                    PlayerAServePointsNS[Opp] += PrevMatchesCommOpps[match][51]
                    PlayerAServePointsWonNS[Opp] += (PrevMatchesCommOpps[match][53] + PrevMatchesCommOpps[match][54])
                    PlayerAReturnPointsNS[Opp] += PrevMatchesCommOpps[match][42]
                    PlayerAReturnPointsWonNS[Opp] += (PrevMatchesCommOpps[match][42] - (PrevMatchesCommOpps[match][44] + PrevMatchesCommOpps[match][45]))
                    nonSurfaceMatchesCount[Opp] += 1

    # Compute the proportion of service points won against each common opponent:
    SPWCommonOppPropsSurface = np.zeros(len(CommonOpps), dtype = float)
    RPWCommonOppPropsSurface = np.zeros(len(CommonOpps), dtype = float)
    SPWCommonOppPropsNS = np.zeros(len(CommonOpps), dtype = float)
    RPWCommonOppPropsNS = np.zeros(len(CommonOpps), dtype = float)
    SPWCommonOppProps = np.zeros(len(CommonOpps), dtype = float)
    RPWCommonOppProps = np.zeros(len(CommonOpps), dtype = float)
    #print('Number of Previous Common Matches: ', len(PrevMatchesCommOpps))

    for Opp in range(len(CommonOpps)):
        # Check if any matches were analysed for this common opponent:
        if (surfaceMatchesCount[Opp] > 0):
            SPWCommonOppPropsSurface[Opp] = PlayerAServePointsWonSurface[Opp] / PlayerAServePointsSurface[Opp]
            RPWCommonOppPropsSurface[Opp] = PlayerAReturnPointsWonSurface[Opp] / PlayerAReturnPointsSurface[Opp]
   
        if (nonSurfaceMatchesCount[Opp] > 0):
            SPWCommonOppPropsNS[Opp] = PlayerAServePointsWonNS[Opp] / PlayerAServePointsNS[Opp]
            RPWCommonOppPropsNS[Opp] = PlayerAReturnPointsWonNS[Opp] / PlayerAReturnPointsNS[Opp]
        
        # Check if the weighting is needed:
        if ((surfaceMatchesCount[Opp] > 0) and (nonSurfaceMatchesCount[Opp] > 0)):
            # Compute overall proportion:
            SPWCommonOppProps[Opp] = ((1 - surface) * (SPWCommonOppPropsSurface[Opp]) + surface * (SPWCommonOppPropsNS[Opp]))
            RPWCommonOppProps[Opp] = ((1 - surface) * (RPWCommonOppPropsSurface[Opp]) + surface * (RPWCommonOppPropsNS[Opp]))
        else:
            SPWCommonOppProps[Opp] = SPWCommonOppPropsSurface[Opp] + SPWCommonOppPropsNS[Opp]
            RPWCommonOppProps[Opp] = RPWCommonOppPropsSurface[Opp] + RPWCommonOppPropsNS[Opp]
    
    OverallSPWCommOpps = sum(SPWCommonOppProps) / len(CommonOpps)
    OverallRPWCommOpps = sum(RPWCommonOppProps) / len(CommonOpps)
    return [OverallSPWCommOpps, OverallRPWCommOpps]