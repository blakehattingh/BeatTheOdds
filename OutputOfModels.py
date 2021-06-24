from RunMarkovModel import RunMarkovModel

def main():
    # This file runs each implementation, for each of the 3 scenarios and outputs each distribution as a plot.

    # Scenarios:
    P2S = 0.7
    P1S = [0.71, 0.75, 0.8]
    FirstToTBPoints = 7
    Viscosity = 0.5

    # Distributions:
    MatchDistributions3 = []
    NumberOfSetsDistributions3 = []
    TotalNumberOfGamesDistributions3 = []
    AllSetScoresDistributions3 = []
    MatchDistributions5 = []
    NumberOfSetsDistributions5 = []
    TotalNumberOfGamesDistributions5 = []
    AllSetScoresDistributions5 = []

    # Possible Outcomes:
    MatchOutcomes = ['Player 1 Wins', 'Player 2 Wins']
    NumberOfSetsOutcomes = [2,3,4,5]
    TotalNumberOfGamesOutcomes = list(range(18,66))
    AllSetScoreOutcomes = ["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]

    # First Implementation:
    Approach = 1
    for P1 in P1S:
        [MatchDist3, NumSetsDist3, TotalNumGamesDist3, AllSetScoresDist3] = RunMarkovModel(P1,P2S,3,FirstToTBPoints,Approach,Viscosity)
        [MatchDist5, NumSetsDist5, TotalNumGamesDist5, AllSetScoresDist5] = RunMarkovModel(P1,P2S,5,FirstToTBPoints,Approach,Viscosity)

        # Append distributions for each scenario:
        MatchDistributions3.append(MatchDist3)
        NumberOfSetsDistributions3.append(NumSetsDist3)
        TotalNumberOfGamesDistributions3.append(TotalNumGamesDist3)
        AllSetScoresDistributions3.append(AllSetScoresDist3)
        MatchDistributions5.append(MatchDist5)
        NumberOfSetsDistributions5.append(NumSetsDist5)
        TotalNumberOfGamesDistributions5.append(TotalNumGamesDist5)
        AllSetScoresDistributions5.append(AllSetScoresDist5)

if __name__ == "__main__":
    main()
    