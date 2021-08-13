from MarkovModel.TennisMatchNetwork1Efficient import TennisMatchNetwork1Efficient
from MarkovModel.TennisSetNetworkEfficient import TennisSetNetworkEfficient
from itertools import islice
from OtherFunctions.AdditionalFunctions import RemainingOdds, TieBreakerProbability, ComputeTBProbabilities, OddsComputer, RemainingOdds
from MarkovModel.loopybeliefprop import beliefpropagation, choose
from OtherFunctions.OMalleysEqns import TB, Matrices, Match3, Set
from OptimisationModel.CVaRModel import CVaRModel
from MarkovModel.RunMarkovModel import RunMarkovModel
import numpy as np
import csv
import matplotlib.pyplot as plt

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)


def main():
    '''
    Bets = ['AWins', 'BWins', '3-0', '3-1', '3-2', '0-3', '1-3', '2-3']
    Probabilities = [0.04470312, 0.10620195, 0.09589186, 0.10717187, 0.3687957, 0.37723549]
    Z = [[1.80,0,4.5,0,0,0,0,0],[1.80,0,0,3.2,0,0,0,0],[1.80,0,0,0,3.8,0,0,0],
    [0,2.06,0,0,0,12.0,0,0],[0,2.06,0,0,0,0,10.0,0],[0,2.06,0,0,0,0,0,9.0]]
    lam = 4.
    beta = 0.2
    CVaRModel(Probabilities, Z, lam, beta, Bets)
    '''

    # Comparing our model and O'Malley's Equations:
    P1S = 0.60
    P2S = 0.55
    Viscosity = 0.5
    '''
    # Implementation 1:
    [MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,1,Viscosity)
    print('Match Distribution: ', end = '')
    print(MatchDist)
    
    # Implementation 2:
    [MatchDist, MatchScoreDist, TotalNumGamesDist, AllSetScoresDist] = RunMarkovModel(P1S,P2S,3,7,2,Viscosity)
    print('Match Distribution: ', end = '')
    print(MatchDist)
    '''
    '''
    # Run a single set and compare to O'Malley:
    [nodes,dist,parents,outcomes,info] = TennisSetNetworkEfficient(P1S, P2S, InitServerDist = [1., 0.])
    [SetScoreDist1] = beliefpropagation(nodes,dist,parents,outcomes,info,100,0.001,['SetScore'])
    AWins = sum(SetScoreDist1[0:7])
    BWins = sum(SetScoreDist1[7:14])
    print(AWins, BWins)

    TwoNil = AWins * AWins
    TwoOne = AWins * BWins * AWins * 2
    print(TwoOne + TwoNil)
    '''

    # O'Malley's:
    #[A, B] = Matrices()
    #print(Set(P1S, 1. - P2S, A, B))

    CommOpps = [5216,3898,4913,5663,3900,4606,4742,5442,3786,3602,4053,4789,3720,2318,4541,3206,3344,3163,4868,3017,26577,2450,5201,4526,
    5220,27834,5763,3096,3084,6219,4752,4659,4544,644,2148,6409,2257,3656,5670,4570,5349,3888,4338,4467,3454,3103,4728,3498,6418,3507,4311,5070,
    5630,3990,3333,5918,3285,3835,4416,3484,2783,3632,4664,3781,6387,3852,3428,5543,3823,5131,5922,4585,4259,5515,4994,3292,5016,3917,
    3813,4068,4035,3758,5166,5159,6401,4122,4098,2179,4022,5210,4470,2839,4269,4229,4675,3582,11547,4019,3843,3808,3970,5055,4716,4214,
    3694,2845,2565,2720,6029,5565,5303,3909,34553,5655,4198,5324,4677,32067,3566,6044,4291,5088,6407,5034,3598,4794,5801,4180,4337,
    5978,4894,5902,4385,5539,4596,3722,3429,5057,5231,26006,4533,4654,4252,5438,6284,6364,3908,5986,2967,4619,3812,6031,5718,4499,3752,
    5046,26413,4921,4914,3794,3565,4225,5571,6057,33214,3893,4326,4879,5793,4592,11176,36221,5370,26010,5375,4493,3503,3110,5636,4331,
    3181,6214,4591,4974]

    print(len(CommOpps))

if __name__ == "__main__":
    main()
