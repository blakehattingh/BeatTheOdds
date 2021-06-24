from RunMarkovModel import RunMarkovModel

def main():
    # This file runs each implementation, for each of the 3 scenarios and outputs each distribution as a plot.

    # Scenarios:
    P2S = 0.7
    P1S = [0.71, 0.75, 0.8]
    FirstToTBPoints = 7
    Viscosity = 0.5

    # First Implementation:
    Approach = 1
    for P1 in P1S:
        [MatchDist3, NumSetsDist3, TotalNumGamesDist3, AllSetScoresDist3] = RunMarkovModel(P1,P2S,3,FirstToTBPoints,Approach,Viscosity)
        [MatchDist5, NumSetsDist5, TotalNumGamesDist5, AllSetScoresDist5] = RunMarkovModel(P1,P2S,5,FirstToTBPoints,Approach,Viscosity)

        # Append distributions for each scenario:
        MatchDistributions = [Matc]