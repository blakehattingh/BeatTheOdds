from pulp import *
import numpy as np

def CVaRModel(Pk, odds, betsConsidered, profile, alphas, betas):
    # Inputs:
    # - Pk: The probability of outcome 'k' occuring
    # - odds: a dictionary of odds with ALL bet types as keys
    #   - if not considered, then the values will be []
    #   - if there is a missing odd for a specific bet, this should be set to zero, e.g. no odds for 2-6 so set to 0
    # - betsConsidered: a list of booleans corresponding to the betting options we are interested in
    # - profile: The users risk profile, either "Risk-Averse, Risk-Neutral or Risk-Seeking"
    #   - This affects the number of alpha and beta values that should be inputted
    # - alphas and betas: parameters corresponding to the users risk profile 
    
    # Create the Zk matrix, the oddCoef vector and the list of available bets:
    [Zk, oddCoef, bettingOptions] = CreateZMatrix(betsConsidered, odds, Pk)

    # Set up information for the problem:
    Outcomes = ['2-0', '2-1', '0-2', '1-2']
    Pk = dict(zip(Outcomes, Pk))

    # Profile = Risk-Neutral:
    if (profile == 'Risk-Neutral'):
        return CVaRModelRN(bettingOptions, oddCoef, Zk)
    
    # Profile = Risk-Averse:
    elif (profile == 'Risk-Averse'):
        return CVaRModelRA(betas, alphas, bettingOptions, Outcomes, oddCoef, Pk, Zk)

    # Profile = Risk-Seeking:
    elif (profile == 'Risk-Seeking'):
        return CVaRModelRS(betas, alphas, bettingOptions, Outcomes, oddCoef, Pk, Zk)
    else:
        print('Not a suitable risk profile entered')

def CVaRModelRN(bettingOptions, oddCoef, Zk):
    # Create the Linear Problem:
    Problem = LpProblem("CVaR_Model", LpMaximize)

    # Create the variables that correspond to the betting options:
    Bets = LpVariable.dicts("Bets", bettingOptions, lowBound = 0, upBound = 1, cat = 'Continuous')

    # Add the objective function:
    Problem += (lpSum([oddCoef[bet] * Bets[bet] - Bets[bet] for bet in oddCoef.keys()]))

    # Using a budget of 1: (constraint bets)
    Problem += sum(Bets.values()) <= 1

    # Solve Model:
    Problem.solve(PULP_CBC_CMD(msg=0))

    # Return Zk matrix and the suggested bets:
    return [Zk, Problem.variables()[0:len(Bets)]]

def CVaRModelRA(betas, alphas, bettingOptions, Outcomes, oddCoef, Pk, Zk):
    # Create the parameters for the CVaR constraints:
    risks = {}
    count = 0
    for b in betas:
        risks[b] = alphas[count]
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
    
    # Add CVaR Loss constranits: (1 for each beta)
    for b in betas:
        Problem += (1. / b) * lpSum([Pk[k] * ((1. - b) * wkMatrix[b][k] + b * vkMatrix[b][k]) for k in Pk.keys()]) <= risks[b]

    # Using a budget of 1: (constraint bets)
    Problem += sum(Bets.values()) <= 1

    # Solve Model:
    Problem.solve(PULP_CBC_CMD(msg=0))

    # Return Zk matrix and the suggested bets:
    return [Zk, Problem.variables()[0:len(Bets)]]

def CVaRModelRS(betas, alphas, bettingOptions, Outcomes, oddCoef, Pk, Zk):
    # Create the parameters for the CVaR constraints:
    risks = {}
    count = 0
    for b in betas:
        risks[b] = alphas[count]
        count += 1   

   # Compute the regret measures:
    regretMeasures = ComputeRegretVector(Zk)

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
            Problem += (sum(Bets[bet] * Zk[k][bet] - Bets[bet] for bet in Bets.keys()) - regretMeasures[k]) == Nu[b] + vkMatrix[b][k] - wkMatrix[b][k]

    # Add CVaR Regret Measure constraints:
    for b in betas:
        Problem += (lpSum([oddCoef[bet] * Bets[bet] - Bets[bet] for bet in oddCoef.keys()])) - (1. / b) * lpSum([Pk[k] * ((1. - b) * wkMatrix[b][k] + b * vkMatrix[b][k]) for k in Pk.keys()]) >= -1. * risks[b]

    # Using a budget of 1: (constraint bets)
    Problem += sum(Bets.values()) <= 1

    # Solve Model:
    Problem.solve(PULP_CBC_CMD(msg=0))

    for var in Problem.variables():
        if ('Bet' in var.name):
            print(var.name, "=", var.varValue)

    # Compute LHS of Regret Constraints:
    for k in Pk.keys():
        print(sum(Bets[bet].varValue * (Zk[k][bet] - 1.) for bet in Bets.keys()) - regretMeasures[k])
    
    # Compute Regret Metric:
    LHS2 = 0.
    for k in Pk.keys():
        # LHS1 += Pk[k] * ((1. - betasRegret[0]) * wkMatrixRegret[betasRegret[0]][k].varValue + betasRegret[0] * vkMatrixRegret[betasRegret[0]][k].varValue - regretMeasures[k])
        LHS2 += Pk[k] * ((1. - betas[0]) * wkMatrix[betas[0]][k].varValue + betas[0] * vkMatrix[betas[0]][k].varValue)
    LHS2 = LHS2 / betas[0]
    print((lpSum([oddCoef[bet] * Bets[bet].varValue - Bets[bet].varValue for bet in oddCoef.keys()])) - LHS2)

    # Return Zk matrix and the suggested bets:
    return [Zk, Problem.variables()[0:len(Bets)]]

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
    # 4) Set Score (14 outcomes: 6-0, 6-1... 7-5, 7-6, 0-6, 1-6... 5-7, 6-7)
    # 5) Number of Games (10 outcomes: O/U 20.5, O/U 22.5, O/U 24.5, O/U 26.5, O/U 28.5)

    # Check the inputs:
    if (len(betsConsidered) != 5):
        raise ValueError('Length of First Input must be 5')
    
    # Create the list of betting options we are considering:
    options = {'Match Outcome': ['AWins','BWins'], 'Match Score': ['2-0','2-1','0-2','1-2'],
    'Number of Sets': ['2 Sets','3 Sets'], 'Set Score': ['6-0','6-1','6-2','6-3','6-4','7-5','7-6','0-6','1-6','2-6',
    '3-6','4-6','5-7','6-7'], 'Number of Games': ['u20.5','o20.5','u22.5','o22.5','u24.5','o24.5','u26.5',
    'o26.5','u28.5','o28.5']}
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
    '1-2': ['1-2'], '2 Sets': ['2-0', '0-2'], '3 Sets': ['2-1','1-2'], '6-0': [], '6-1': [], '6-2': [], '6-3': [], 
    '6-4': [], '7-5': [], '7-6': [], '0-6': [], '1-6': [], '2-6': [], '3-6': [], '4-6': [], '5-7': [],
    '6-7': [], 'u20.5': [], 'o20.5': [], 'u22.5': [], 'o22.5': [], 'u24.5': [], 'o24.5': [], 'u26.5': [],
    'o26.5': [], 'u28.5': [], 'o28.5': []}

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

def ComputeRegretVector(Zk):
    # This function pre-computes the maximum amount that can be made for each outcome, given we are certain of
    # the outcome.

    # Iterate through the possible outcomes:
    regretMeasures = {}
    for outcome in Zk:
        # Find the best paying bet for this outcome:
        bestBetValue = 0.
        for bet in Zk[outcome]:
            if (Zk[outcome][bet] > bestBetValue):
                # Record this bet to take:
                bestBetValue = Zk[outcome][bet]

                # Compute the Regret measure:
                regretMeasures[outcome] = bestBetValue - 1.
    print(regretMeasures)
    return regretMeasures
    
def RunCVaRModel(betsConsidered,probDist,profile,RHS,betas,oddsMO,oddsMS,oddsNumSets,oddsSS=[],oddsNumGames=[]):
    # This function sets up the required data and runs the CVaR model, returning a set of bets to make.
    # Inputs:
    # - betsConsidered: A list of booleans of the bets we want to consider (Outcome, Score, #Sets, SS, #Games)
    # - probDist: A list of probabilities corresponding to the possible outcomes (currently 2-0, 2-1, 0-2, 1-2)
    # - profile: The users risk profile ('Risk-Averse', 'Risk-Neutral', 'Risk-Seeking')
    # - RHS: A list of RHS values from the user about their risk profile
    # - betas: The beta parameters we are using in the CVaR model for the constraints (Currently 0.2, 0.33, 0.5)
    # - odds--: The odds for each type of bet as a list e.g. [oddsAWins, oddsBWins]

    # Create odds dictionary:
    odds = {'Match Outcome': oddsMO, 'Match Score': oddsMS, 'Number of Sets': oddsNumSets,
    'Set Score': oddsSS, 'Number of Games': oddsNumGames}

    # Run the CVaR model:
    [Zk, suggestedBets] = CVaRModel(probDist, odds, betsConsidered, profile, RHS, betas)

    # Extract and store the values of the variables:
    bets = {}
    count = 0
    for bet in suggestedBets:
        # Remove variable name:
        betName = bet.name.split("_", 1)[1]

        # Check if underscore needs to be changed to a hyphen or whitespace (for sets):
        if ('_' in betName):                
            elements = list(betName)
            ind = elements.index('_')
            if ('Set' in betName):
                elements[ind] = ' '
            else:
                elements[ind] = '-'
            betName = ''.join(elements)

        bets[betName] = suggestedBets[count].varValue
        count += 1

    return [Zk, bets]
