from pulp import *
import numpy as np

def CVaRModel(Pk, Zk, lam, beta, BettingOptions):
    # Inputs:
    # - Pk: The probability of outcome 'k' occuring
    # - Zk: A matrix with each row corresponding to the possible outcomes (k outcomes) and the columns corresponding to all
    #       possible bets that can be made. If bet (column) j pays out under outcome (row) i, then Zk[i,j] = odds for bet j, 
    #       otherwise it is set to zero.
    # e.g. Let outcome be the Game Score = 3-0, then betting on:
    # 1. A to win
    # 2. Game Score to be 3-0
    # 3. Number of Points to be 3
    #   will all pay out.
    # - lam and beta are parameters corresponding to the users risk profile
    # - BettingOptions is a list of the names of possible bets
    
    # Set up information for the problem:
    Outcomes = ['3-0', '3-1', '3-2', '0-3', '1-3', '2-3']
    Odds = []
    for k in range(len(Outcomes)):
        OddDict = dict(zip(BettingOptions,Zk[k]))
        Odds.append(OddDict)
    Zk = dict(zip(Outcomes,Odds))
    Pk = dict(zip(Outcomes, Pk))

    # Compute Odd Coefficients for Objective Function:
    OddCoef = {}
    for Bet in BettingOptions:
        SumOdds = sum(Pk[key] * Zk.get(key).get(Bet) for key in Pk)
        OddCoef.update({Bet: SumOdds})

    # Create the Linear Problem:
    Problem = LpProblem("CVaR Model", LpMaximize)

    # Create the variables that correspond to the betting options:
    Bets = LpVariable.dicts("Bets", BettingOptions, lowBound = 0, upBound = 1, cat = 'Continuous')

    # Create the nu variable:
    Nu = LpVariable("Nu")

    # Create the Wk and Vk variables: (Slacks & Surps)
    Vk = LpVariable.dicts("Slacks", Outcomes, lowBound = 0, cat = 'Continuous')
    Wk = LpVariable.dicts("Surps", Outcomes, lowBound = 0, cat = 'Continuous')

    # Add the objective function:
    Problem += (lpSum([OddCoef[bet] * Bets[bet] for bet in OddCoef.keys()]) - lam * (lpSum([Pk[k] * ((1 - beta) * Wk[k] + beta * Vk[k]) for k in Pk.keys()])))

    # Add constraints: (1 for each possible outcome)
    for k in Outcomes:
        Problem += sum(Bets[Bet] * Zk[k].get(Bet) for Bet in Bets.keys()) == Nu + Vk[k] - Wk[k]
    
    # Using a budget of 1: (constraint bets)
    Problem += sum(Bets.values()) <= 1

    # Solve Model:
    Problem.solve()
    for var in Problem.variables():
        print(var.name, "=", var.varValue)