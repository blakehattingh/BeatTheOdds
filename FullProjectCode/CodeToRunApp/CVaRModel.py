from pulp import *
import numpy as np

def CVaRModel(Pk, odds, betsConsidered, RHS, betas):
    # Inputs:
    # - Pk: The probability of outcome 'k' occuring
    # - odds: a dictionary of odds with ALL bet types as keys
    #   - if not considered, then the values will be []
    #   - if there is a missing odd for a specific bet, this should be set to zero, e.g. no odds for 2-6 so set to 0
    # - betsConsidered: a list of booleans corresponding to the betting options we are interested in
    # - RHS and betas are parameters corresponding to the users risk profile
    
    # Create the Zk matrix, the oddCoef vector and the list of available bets:
    [Zk, oddCoef, bettingOptions] = CreateZMatrix(betsConsidered, odds, Pk)

    # Set up information for the problem:
    Outcomes = ['2-0', '2-1', '0-2', '1-2']
    Pk = dict(zip(Outcomes, Pk))
    risks = {}
    count = 0
    for b in betas:
        risks[b] = RHS[count]
        count += 1

    # Create the Linear Problem:
    Problem = LpProblem("CVaR_Model", LpMaximize)

    # Create the variables that correspond to the betting options:
    Bets = LpVariable.dicts("Bets", bettingOptions, lowBound = 0, upBound = 1, cat = 'Continuous')

    # Create the nu variable:
    Nu = LpVariable.dicts("Nu", betas, cat = 'Continuous')

    # Create the Wk and Vk variables: (Slacks & Surps)
    vkMatrix = {}
    wkMatrix = {}
    for b in betas:
        vkMatrix[b] = LpVariable.dicts(("Slacks_{}".format(b)), Outcomes, lowBound = 0, cat = 'Continuous')
        wkMatrix[b] = LpVariable.dicts(("Surps_{}".format(b)), Outcomes, lowBound = 0, cat = 'Continuous')

    # Add the objective function:
    Problem += (lpSum([oddCoef[bet] * Bets[bet] - Bets[bet] for bet in oddCoef.keys()]))

    # Add constraints: (1 for each possible outcome and beta)
    for b in betas:
        for k in Outcomes:
            Problem += sum(Bets[bet] * Zk[k][bet] for bet in Bets.keys()) == Nu[b] + vkMatrix[b][k] - wkMatrix[b][k]
    
    # Add CVaR constranits: (1 for each beta)
    for b in betas:
        Problem += (1. / b) * lpSum([Pk[k] * ((1 - b) * wkMatrix[b][k] + b * vkMatrix[b][k]) for k in Pk.keys()]) <= risks[b] # alpha * lpSum([OddCoef[bet] * Bets[bet] - Bets[bet] for bet in OddCoef.keys()])

    # Using a budget of 1: (constraint bets)
    Problem += sum(Bets.values()) <= 1

    # Solve Model:
    # LpSolverDefault.msg = 1
    Problem.solve(PULP_CBC_CMD(msg=0))
    #for var in Problem.variables():
     #   print(var.name, "=", var.varValue)

    # Return Zk matrix and the suggested bets:
    return [Zk, Problem.variables()[0:len(Bets)], value(Problem.objective)]

def CreateZMatrix(betsConsidered, odds, probabilities):
    # Given a set of bets to consider and their corresponding odds, this function creates the "Payoff Matrix" (Z)
    # Inputs:
    # - betsConsidered = a list of booleans representing if we are considering the bet type or not
    # - odds = a dictionary of odds with ALL bet types as keys
    #   - if not considered, then the values will be []
    #   - if there is a missing odd for a specific bet, this should be set to zero, e.g. no odds for 2-6 so set to 0
    # - probabilities = probability distribution for the possible outcomes 

    # Payoff Matrix: (Z = a list of lists)
    # - Each list in Z corresponds to a possible outcome of the match (therefore there will always be 6 list for a 3-set match)
    # - Each element in each list corresponds to the payoff received, given that outcome, for that specific bet

    # Types of Possible Bets:
    # 1) Match Outcome (2 outcomes: AWins, BWins)
    # 2) Match Score (4 outcomes: 2-0, 2-1, 0-2, 1-2)
    # 3) Number of Sets (2 outcomes: 2, 3)
    # NOT being considered:
    # 4) Set Score (14 outcomes: 6-0, 6-1... 7-5, 7-6, 0-6, 1-6... 5-7, 6-7)
    # 5) Number of Games (10 outcomes: O/U 20.5, O/U 22.5, O/U 24.5, O/U 26.5, O/U 28.5)

    # Check the inputs:
    if (len(betsConsidered) != 3):
        raise ValueError('Length of First Input must be 3')
    
    # Create the list of betting options we are considering:
    options = {'Match Outcome': ['AWins','BWins'], 'Match Score': ['2-0','2-1','0-2','1-2'],
    'Number of Sets': ['2','3']}
    bettingOptions = []
    count = 0
    for option in options:
        if (betsConsidered[count]):        
            bettingOptions = bettingOptions + options[option]
        count += 1

    # Possible outcomes of a 3 set match:
    outcomes = ['2-0','2-1','0-2','1-2']
 
    # Create a dictionary showing which bets payout under which outcomes:
    paysOut = {'AWins':['2-0','2-1'], 'BWins':['0-2','1-2'], '2-0': ['2-0'], '2-1': ['2-1'], '0-2': ['0-2'],
    '1-2': ['1-2'], '2': ['2-0', '0-2'], '3': ['2-1','1-2']}

    # Create the Z matrix:
    Zk = {}
    for k in outcomes:
        Zk[k] = {}
        count = 0
        for bet in bettingOptions:
            if (k in paysOut[bet]):
                for option in odds:
                    if (bet in options[option]):
                        # Find the index of it:
                        ind = options[option].index(bet)
                        Zk[k][bet] = odds[option][ind]
            else:
                Zk[k][bet] = 0.            

    # Compute Odd Coefficients for Objective Function:
    oddCoef = {}
    for bet in bettingOptions:
        sumOdds = 0
        count = 0
        for k in outcomes:
            sumOdds += probabilities[count] * Zk[k][bet]
            count += 1
        oddCoef[bet] = sumOdds

    return [Zk, oddCoef, bettingOptions]

def RunCVaRModel(betsConsidered,probDist,RHS,betas,odds):
    # This function sets up the required data and runs the CVaR model, returning a set of bets to make.
    # Inputs:
    # - betsConsidered: A list of booleans of the bets we want to consider (Outcome, Score, #Sets, SS, #Games)
    # - probDist: A list of probabilities corresponding to the possible outcomes (currently 2-0, 2-1, 0-2, 1-2)
    # - RHS: A list of RHS values from the user about their risk profile
    # - betas: The beta parameters we are using in the CVaR model (Currently 0.2, 0.33, 0.5)
    # - odds: The odds for each type of bet in dictionary format

    # Run the CVaR model:
    [Zk, suggestedBets] = CVaRModel(probDist, odds, betsConsidered, RHS, betas)

    # Extract and store the values of the variables:
    bets = {}
    count = 0
    for bet in suggestedBets:
        # Remove variable name:
        betName = bet.name.split("_", 1)[1]

        # Check if underscore needs to be changed to a hyphen:
        if ('_' in betName):
            elements = list(betName)
            ind = elements.index('_')
            elements[ind] = '-'
            betName = ''.join(elements)

        bets[betName] = suggestedBets[count].varValue
        count += 1

    return [Zk, bets]
