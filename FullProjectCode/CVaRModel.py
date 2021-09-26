from pulp import *
import numpy as np

def CVaRModel(Pk, odds, betsConsidered, profile, alphasLoss, betasLoss, alphasRegret = [], betasRegret = []):
    # Inputs:
    # - Pk: The probability of outcome 'k' occuring
    # - odds: a dictionary of odds with ALL bet types as keys
    #   - if not considered, then the values will be []
    #   - if there is a missing odd for a specific bet, this should be set to zero, e.g. no odds for 2-6 so set to 0
    # - betsConsidered: a list of booleans corresponding to the betting options we are interested in
    # - profile: The users risk profile, either "Risk-Averse, Risk-Neutral or Risk-Seeking"
    #   - This affects the number of alpha and beta values that should be inputted
    # - alphas and betas: parameters corresponding to the users risk profile 
    #   - the Loss ones refer to averse or neutral profiles whereas the regret ones are for risk seeking profiles 
    
    # Create the Zk matrix, the oddCoef vector and the list of available bets:
    [Zk, oddCoef, bettingOptions] = CreateZMatrix(betsConsidered, odds, Pk)

    # Set up information for the problem:
    Outcomes = ['2-0', '2-1', '0-2', '1-2']
    Pk = dict(zip(Outcomes, Pk))

    # Set up the appropriate CVaR constraints to add to the model:
    risksLoss = {}
    count = 0

    # Create the parameters for the Loss CVaR constraints:
    for b in betasLoss:
        risksLoss[b] = alphasLoss[count]
        count += 1      

    # Create the Linear Problem:
    Problem = LpProblem("CVaR_Model", LpMaximize)

    # Create the variables that correspond to the betting options:
    Bets = LpVariable.dicts("Bets", bettingOptions, lowBound = 0, upBound = 1, cat = 'Continuous')

    # Create the nu variable:
    NuLoss = LpVariable.dicts("Nu", betasLoss, cat = 'Continuous')

    # Create the Wk and Vk variables: (Slacks & Surps)
    vkMatrixLoss = {}
    wkMatrixLoss = {}
    for b in betasLoss:
        vkMatrixLoss[b] = LpVariable.dicts(("Slacks_{}".format(b)), Outcomes, lowBound = 0, cat = 'Continuous')
        wkMatrixLoss[b] = LpVariable.dicts(("Surps_{}".format(b)), Outcomes, lowBound = 0, cat = 'Continuous')

    # Add the objective function:
    Problem += (lpSum([oddCoef[bet] * Bets[bet] - Bets[bet] for bet in oddCoef.keys()]))

    # Add constraints: (1 for each possible outcome and beta)
    for b in betasLoss:
        for k in Outcomes:
            Problem += sum(Bets[bet] * Zk[k][bet] for bet in Bets.keys()) == NuLoss[b] + vkMatrixLoss[b][k] - wkMatrixLoss[b][k]
    
    # Add CVaR Loss constranits: (1 for each beta)
    for b in betasLoss:
        Problem += (1. / b) * lpSum([Pk[k] * ((1. - b) * wkMatrixLoss[b][k] + b * vkMatrixLoss[b][k]) for k in Pk.keys()]) <= risksLoss[b] # * lpSum([oddCoef[bet] * Bets[bet] - Bets[bet] for bet in oddCoef.keys()])]

    # Add the risk constraints:
    if (profile == 'Risk-Seeking'):
        # Create the required variables:
        NuRegret = LpVariable.dicts("NuRegrets", betasRegret, cat = 'Continuous')

        # Create the Wk and Vk variables: (Slacks & Surps)
        vkMatrixRegret = {}
        wkMatrixRegret = {}
        for b in betasRegret:
            vkMatrixRegret[b] = LpVariable.dicts(("SlacksOnRegrets_{}".format(b)), Outcomes, lowBound = 0, cat = 'Continuous')
            wkMatrixRegret[b] = LpVariable.dicts(("SurpsOnRegrets_{}".format(b)), Outcomes, lowBound = 0, cat = 'Continuous')

        # Compute the regret measures:
        regretMeasures = ComputeRegretVector(Zk)

        # Create the parameters for the Regret constraints:
        risksRegret = {}
        count = 0
        for b in betasRegret:
            risksRegret[b] = alphasRegret[count]
            count += 1

        # Add constraints: (1 for each possible outcome and beta)
        for b in betasRegret:
            for k in Outcomes:
                Problem += (sum(Bets[bet] * Zk[k][bet] for bet in Bets.keys()) - regretMeasures[k]) == NuRegret[b] + vkMatrixRegret[b][k] - wkMatrixRegret[b][k]

        # Add CVaR Regret Measure constraints:
        for b in betasRegret:
            Problem += (1. / b) * lpSum([Pk[k] * ((1. - b) * wkMatrixRegret[b][k] + b * vkMatrixRegret[b][k]) for k in Pk.keys()]) <= risksRegret[b]

    # Using a budget of 1: (constraint bets)
    Problem += sum(Bets.values()) <= 1

    # Solve Model:
    # LpSolverDefault.msg = 1
    Problem.solve(PULP_CBC_CMD(msg=0))
    for var in Problem.variables():
        if ('Loss' in var.name):
            print(var.name, "=", var.varValue)
        if ('Bet' in var.name):
            print(var.name, "=", var.varValue) 

    # Compute LHS of Regret Constraints:
    for k in Pk.keys():
        print(sum(Bets[bet].varValue * Zk[k][bet] for bet in Bets.keys()) - regretMeasures[k])
    LHS1 = 0.
    LHS2 = 0.
    if (profile == 'Risk-Seeking'):
        for k in Pk.keys():
            # LHS1 += Pk[k] * ((1. - betasRegret[0]) * wkMatrixRegret[betasRegret[0]][k].varValue + betasRegret[0] * vkMatrixRegret[betasRegret[0]][k].varValue - regretMeasures[k])
            LHS2 += Pk[k] * ((1. - betasRegret[0]) * wkMatrixRegret[betasRegret[0]][k].varValue + betasRegret[0] * vkMatrixRegret[betasRegret[0]][k].varValue)
        # print(LHS1 / betasRegret[0])
        print(LHS2)
        print(LHS2 / betasRegret[0])
    else:
        for b in betasLoss:
            LHS1 = 0.
            for k in Pk.keys():
                LHS1 += Pk[k] * ((1. - b) * wkMatrixLoss[b][k].varValue + b * vkMatrixLoss[b][k].varValue)
            LHS1 = LHS1 / b
            print('{} Quantile, the Loss is {}'.format(b, LHS1))

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
                regretMeasures[outcome] = bestBetValue
    print(regretMeasures)
    return regretMeasures
    
def RunCVaRModel(betsConsidered,probDist,profile,RHSLoss,betasLoss,oddsMO,oddsMS,oddsNumSets,oddsSS=[],oddsNumGames=[],RHSRegret=[],betasRegret=[]):
    # This function sets up the required data and runs the CVaR model, returning a set of bets to make.
    # Inputs:
    # - betsConsidered: A list of booleans of the bets we want to consider (Outcome, Score, #Sets, SS, #Games)
    # - probDist: A list of probabilities corresponding to the possible outcomes (currently 2-0, 2-1, 0-2, 1-2)
    # - profile: The users risk profile ('Risk-Averse', 'Risk-Neutral', 'Risk-Seeking')
    # - RHSLoss: A list of RHS values from the user about their willingness to lose money
    # - betasLoss: The beta parameters we are using in the CVaR model for the loss constraints (Currently 0.2, 0.33, 0.5)
    # - odds--: The odds for each type of bet as a list e.g. [oddsAWins, oddsBWins]
    # - RHSRegret: The responses from the user about how much they are willing to "regret"
    # - betasRegret: The corresponding beta quantiles for the RHSRegret values

    # Create odds dictionary:
    odds = {'Match Outcome': oddsMO, 'Match Score': oddsMS, 'Number of Sets': oddsNumSets,
    'Set Score': oddsSS, 'Number of Games': oddsNumGames}

    # Run the CVaR model:
    [Zk, suggestedBets] = CVaRModel(probDist, odds, betsConsidered, profile, RHSLoss, betasLoss, RHSRegret, betasRegret)

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
