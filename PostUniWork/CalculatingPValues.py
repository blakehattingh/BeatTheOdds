import numpy as np
            
def CalcPEquation2(hyperparameters, MatchData, PrevMatches, PrevMatchesCommA, PrevMatchesCommB, CommonOpps):
    # This function takes in a match, extracts who is playing, when the match is/was played, and what surface it is/was played on
    # It then computes the P values for both players.
    # Inputs:
    # - hyperparameters: a list of the 3 hyperparameters to use (age, surface, weighting)
    # - MatchData: Data on a single match to be predicted on
    # - PrevMatches: The previous matches between the players playing in the match
    # - PrevMatchesCommA / B: The matches between player A / B and the common opponents
    # - CommonOpps: A list of common opponent IDs

    # Returns:
    # - Pa and Pb
    # - Boolean relating to if we can predict or not with the P values

    # Extract required info:
    surfaceOfMatch = MatchData[4]
    PlayerA = int(MatchData[8])
    PlayerB = int(MatchData[18])
   
    # See how many matches have been played between A and B:
    numMatches = len(PrevMatches)

    # Check if we have sufficient historical data to make predictions:
    if (numMatches == 0):
        if (len(CommonOpps) == 0):
            # We have no data to use to compute P, thus do NOT compute it:
            return [0.5,0.5,False]
        else:
            # Compute SPW(A,C) and SPW(B,C):
            [spwAC, rpwAC] = ComputeSPWCommon(PlayerA, PrevMatchesCommA, CommonOpps, hyperparameters[1], surfaceOfMatch) 
            [spwBC, rpwBC] = ComputeSPWCommon(PlayerB, PrevMatchesCommB, CommonOpps, hyperparameters[1], surfaceOfMatch)

            # Compute PaS and PbS:
            PaS = spwAC
            PbS = spwBC

            # Compute PaR and PbR:
            PaR = rpwAC
            PbR = rpwBC

            # Compute P:
            Pa = PaS / (PaS + PbR)
            Pb = PbS / (PbS + PaR)
    else:
        if (len(CommonOpps) == 0):
            # No common opponents, but they have played before: (rare occurence)
            # Compute SPW(A,B) and SPW(B, A):
            [spwAB, spwBA] = ComputeSPW(PlayerA, PrevMatches, hyperparameters[1], surfaceOfMatch)

            # Compute RPW(A,B) and RPW(B,A)
            rpwAB = 1. - spwBA
            rpwBA = 1. - spwAB       

            # Compute PaS and PbS:
            PaS = spwAB
            PbS = spwBA

            # Compute PaR and PbR:
            PaR = rpwAB
            PbR = rpwBA

            # Compute P
            Pa = PaS / (PaS + PbR)
            Pb = PbS / (PbS + PaR)
        else:
            # Compute SPW(A,B) and SPW(B, A):
            [spwAB, spwBA] = ComputeSPW(PlayerA, PrevMatches, hyperparameters[1], surfaceOfMatch)

            # Compute RPW(A,B) and RPW(B,A)
            rpwAB = 1. - spwBA
            rpwBA = 1. - spwAB

            # Compute SPW(A,C) and SPW(B,C):
            [spwAC, rpwAC] = ComputeSPWCommon(PlayerA, PrevMatchesCommA, CommonOpps, hyperparameters[1], surfaceOfMatch) 
            [spwBC, rpwBC] = ComputeSPWCommon(PlayerB, PrevMatchesCommB, CommonOpps, hyperparameters[1], surfaceOfMatch)

            # Compute PaS and PbS:
            PaS = (1  - hyperparameters[2]) * spwAB + hyperparameters[2] * spwAC
            PbS = (1  - hyperparameters[2]) * spwBA + hyperparameters[2] * spwBC

            # Compute PaR and PbR:
            PaR = (1  - hyperparameters[2]) * rpwAB + hyperparameters[2] * rpwAC
            PbR = (1  - hyperparameters[2]) * rpwBA + hyperparameters[2] * rpwBC

            # Compute P:
            Pa = PaS / (PaS + PbR)
            Pb = PbS / (PbS + PaR)             
    return [Pa, Pb, True]

def ComputeSPW(PlayerA, PrevMatches, surface, surfaceOfMatch):
    # This function computes the proportion of service points won by each player against the other player historically
    # It applies the surface weighting parameter during this calculation.
    # Inputs:
    # - surface: A hyperparameter corresponding to the weighting on matches played on the same surface
    # - PlayerA: ID of the first player of interest (the 2nd players ID is not needed) 
    # - PrevMatches: A list of tuples of all previous matches between player A and player B
    # - surfaceOfMatch: The surface that the match will be played on (as an abbrev, e.g. C = Clay)

    # Returns:
    # - SPW(A,B) and SPW(B, A)

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
        '''PrevMatches[match][8] = float(PrevMatches[match][8])
        PrevMatches[match][18] = float(PrevMatches[match][18])
        PrevMatches[match][42] = float(PrevMatches[match][42])
        PrevMatches[match][44] = float(PrevMatches[match][44])
        PrevMatches[match][45] = float(PrevMatches[match][45])
        PrevMatches[match][51] = float(PrevMatches[match][51])
        PrevMatches[match][52] = float(PrevMatches[match][52])
        PrevMatches[match][53] = float(PrevMatches[match][53])
        PrevMatches[match][54] = float(PrevMatches[match][54])'''
        
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
    # This function computes the proportion of service points won by a player against each common opponent, historically
    # It applies the surface weighting parameter during this calculation.
    # Inputs:
    # - PlayerA = ID of Player of interest
    # - PrevMatchesCommOpps = A list of tuples of all previous matches between player A the common opponents
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
        '''
        PrevMatchesCommOpps[match][8] = float(PrevMatchesCommOpps[match][8])
        PrevMatchesCommOpps[match][18] = float(PrevMatchesCommOpps[match][18])
        PrevMatchesCommOpps[match][42] = float(PrevMatchesCommOpps[match][42])
        PrevMatchesCommOpps[match][44] = float(PrevMatchesCommOpps[match][44])
        PrevMatchesCommOpps[match][45] = float(PrevMatchesCommOpps[match][45])
        PrevMatchesCommOpps[match][51] = float(PrevMatchesCommOpps[match][51])
        PrevMatchesCommOpps[match][52] = float(PrevMatchesCommOpps[match][52])
        PrevMatchesCommOpps[match][53] = float(PrevMatchesCommOpps[match][53])
        PrevMatchesCommOpps[match][54] = float(PrevMatchesCommOpps[match][54])
        '''
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

    numOpps = 0
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

        # Compute the actual number of common opponents:
        if ((surfaceMatchesCount[Opp] + nonSurfaceMatchesCount[Opp]) > 0):
            numOpps += 1

    OverallSPWCommOpps = sum(SPWCommonOppProps) / numOpps
    OverallRPWCommOpps = sum(RPWCommonOppProps) / numOpps
    return [OverallSPWCommOpps, OverallRPWCommOpps]