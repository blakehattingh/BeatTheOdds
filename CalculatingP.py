def EvalEquation1(Pa, Pb):
    

def CalcPEquation1(Lamda, Age, Surface, PlayerA, PlayerB):
    # Compute SPW(A,B):

    # Compute SPW(B,A):

    # Compute SPW(A,C):

    # Compute SPW(B,C):

    # Compute P Values:
    Pa = (1  - Lamda) * spwAB + Lamda * spwAC
    Pb = (1  - Lamda) * spwBA + Lamda * spwBC

def ComputeSPW(PlayerA, PlayerB, Age, Surface):

def ComputeSPWCommon(PlayerA, CommonOpps, Age, Surface):
    # Compute the number of common opponents:
    N = len(CommonOpps)

    # Sum the service points won and the number of service points played:
    SvPtWon = 0
    SvPtPlayed = 0
    for Opp in CommonOpps:
        SvPtWon += x
        SvPtPlayed += y

    # Compute SPW:
    return spwAC = (SvPtWon / SvPtPlayer)


