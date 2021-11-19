from pulp import *
import numpy as np

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
    return [Zk, Problem.variables()[0:len(Bets)], value(Problem.objective)]

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
            Problem += sum(Bets[bet] * Zk[k][bet] - Bets[bet] for bet in Bets.keys()) == Nu[b] + vkMatrix[b][k] - wkMatrix[b][k]
    
    # Add CVaR Loss constranits: (1 for each beta)
    for b in betas:
        Problem += lpSum(Pk[k] * (sum(Bets[bet] * Zk[k][bet] - Bets[bet] for bet in Bets.keys())) for k in Outcomes) - (1. / b) * lpSum([Pk[k] * ((1. - b) * wkMatrix[b][k] + b * vkMatrix[b][k]) for k in Pk.keys()]) >= -1 * risks[b]

    # Using a budget of 1: (constraint bets)
    Problem += sum(Bets.values()) <= 1

    # Solve Model:
    Problem.solve(PULP_CBC_CMD(msg=0))
    
    # Return Zk matrix and the suggested bets:
    return [Zk, Problem.variables()[0:len(Bets)], value(Problem.objective)]

def CVaRModelRS(beta, alpha, bettingOptions, Outcomes, oddCoef, Pk, Zk):
    # Create the parameters for the CVaR constraints:
    risks = {}
    risks = alpha

   # Compute the regret measures:
    regretMeasures = ComputeRegretVector(Zk)

    # Create the Linear Problem:
    Problem = LpProblem("CVaR_Model", LpMaximize)

    # Create the variables that correspond to the betting options:
    Bets = LpVariable.dicts("Bets", bettingOptions, lowBound = 0, upBound = 1, cat = 'Continuous')

    # Create the nu variable:
    Nu = LpVariable("Nu", cat = 'Continuous')

    # Create the Wk and Vk variables: (Slacks & Surps)
    vkMatrix = LpVariable.dicts(("Slacks"), Outcomes, lowBound = 0, cat = 'Continuous')
    wkMatrix = LpVariable.dicts(("Surps"), Outcomes, lowBound = 0, cat = 'Continuous')

    # Add the objective function:
    Problem += (lpSum([oddCoef[bet] * Bets[bet] - Bets[bet] for bet in oddCoef.keys()]))

    # Add constraints: (1 for each possible outcome and beta)
    for k in Outcomes:
        Problem += (sum(Bets[bet] * Zk[k][bet] - Bets[bet] for bet in Bets.keys()) - regretMeasures[k]) == Nu + vkMatrix[k] - wkMatrix[k]

    # Add CVaR Regret Measure constraints:
    Problem += lpSum(Pk[k] * (sum(Bets[bet] * Zk[k][bet] - Bets[bet] for bet in Bets.keys()) - regretMeasures[k]) for k in Outcomes) - (1. / beta) * lpSum([Pk[k] * ((1. - beta) * wkMatrix[k] + beta * vkMatrix[k]) for k in Pk.keys()]) >= -1. * risks

    # Using a budget of 1: (constraint bets)
    Problem += sum(Bets.values()) == 1

    # Solve Model:
    Problem.solve(PULP_CBC_CMD(msg=0))

    # Return Zk matrix and the suggested bets:
    return [Zk, Problem.variables()[0:len(Bets)],value(Problem.objective)]

def CVaRModelRSThreshold(beta, bettingOptions, Outcomes, Pk, Zk):
    # This function computes the minimum amount of regret possiblw  

   # Compute the regret measures:
    regretMeasures = ComputeRegretVector(Zk)

    # Create the Linear Problem:
    Problem = LpProblem("CVaR_Model", LpMaximize)

    # Create the variables that correspond to the betting options:
    Bets = LpVariable.dicts("Bets", bettingOptions, lowBound = 0, upBound = 1, cat = 'Continuous')

    # Create the nu variable:
    Nu = LpVariable("Nu", cat = 'Continuous')

    # Create the Wk and Vk variables: (Slacks & Surps)
    vkMatrix = LpVariable.dicts(("Slacks"), Outcomes, lowBound = 0, cat = 'Continuous')
    wkMatrix = LpVariable.dicts(("Surps"), Outcomes, lowBound = 0, cat = 'Continuous')

    # Add the objective function:
    Problem += lpSum(Pk[k] * (sum(Bets[bet] * Zk[k][bet] - Bets[bet] for bet in Bets.keys()) - regretMeasures[k]) for k in Outcomes) - (1. / beta) * lpSum([Pk[k] * ((1. - beta) * wkMatrix[k] + beta * vkMatrix[k]) for k in Pk.keys()])

    # Add constraints: (1 for each possible outcome)
    for k in Outcomes:
        Problem += (sum(Bets[bet] * Zk[k][bet] - Bets[bet] for bet in Bets.keys()) - regretMeasures[k]) == Nu + vkMatrix[k] - wkMatrix[k]

    # Using a budget of 1: (constraint bets)
    Problem += sum(Bets.values()) == 1

    # Solve Model:
    Problem.solve(PULP_CBC_CMD(msg=0))

    # Return the objective which finds the threshold for minimum regret possible:
    return value(Problem.objective)

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
    return regretMeasures

def HighestPayingBet(Zk):
    # This function finds and returns the highest paying bet and the associated odds
    # Inputs:
    # Zk: The payoff matrix
     
    maxOdds = 0.
    for outcome in Zk:
        for bet in Zk[outcome]:
            if (Zk[outcome][bet] > maxOdds):
                maxOdds = Zk[outcome][bet]
                maxBet = bet
    
    return [maxBet, maxOdds]

def ExtractBets(suggestedBets):
    # This function takes in the suggested bets from the optimisation model and converts them to a usable form
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
    return bets

def makeOddsDict(oddsMO, oddsMS, oddsNumSets, oddsSS = [], oddsNumGames = []):
    # This function makes the odds dictioanry required for CVaR model
    return {'Match Outcome': oddsMO, 'Match Score': oddsMS, 'Number of Sets': oddsNumSets, 'Set Score': oddsSS, 'Number of Games': oddsNumGames}
    
def RunCVaRModel(betsConsidered,probDist,profile,RHS,betas,odds):
    # This function sets up the required data and runs the CVaR model, returning a set of bets to make.
    # Inputs:
    # - betsConsidered: A list of booleans of the bets we want to consider (Outcome, Score, #Sets, SS, #Games)
    # - probDist: A list of probabilities corresponding to the possible outcomes (currently 2-0, 2-1, 0-2, 1-2)
    # - profile: The users risk profile ('Risk-Averse', 'Risk-Neutral', 'Risk-Seeking')
    # - RHS: A list of RHS values from the user about their risk profile
    # - betas: The beta parameters we are using in the CVaR model for the constraints (Currently 0.1, 0.2, 0.3)
    # - odds: The odds for each type of bet as in a dictionary

    # Returns:
    # - Payoff matrix (Zk), suggested bets (bets) and the objective value of the model (expected payoff)
    # - If user is "risk-seeking", the minimum amount of regret feasible is also returned

    tol = 1e-6

    # Create the Zk matrix, the oddCoef vector and the list of available bets:
    [Zk, oddCoef, bettingOptions] = CreateZMatrix(betsConsidered, odds, probDist)

    # Set up information for the problem:
    outcomes = ['2-0', '2-1', '0-2', '1-2']
    Pk = dict(zip(outcomes, probDist))

    # Run the CVaR Model:

    # If user = 'Risk-Seeking', need to check the minimum threshold and the risk-neutral models actions:
    if (profile == 'Risk-Seeking'):
        # Find the highest paying bet:
        [maxBet, maxOdds] = HighestPayingBet(Zk)

        # Check if the risk-neutral model is already betting on the most "risky" option:
        [Zk, suggestedBets, objVal] = CVaRModelRN(bettingOptions, oddCoef, Zk)
        
        # Iterate through suggested bets to see if all the budget is on the most risky one:
        bets = ExtractBets(suggestedBets)
        for bet in bets:
            if (bets[bet] >= (1. - tol)):
               suggestedBet = bet
        
        # Check if this is the most risky:
        if (suggestedBet != maxBet):
            # Need to employ the risk-seekig model:

            # Check the threshold for the regret measure:
            minRegret = -1 * CVaRModelRSThreshold(betas, bettingOptions, outcomes, Pk, Zk)
            minThreshold = minRegret + 0.2

            # Compare it to the users input:
            if (minThreshold <= RHS):
                # Feasible value, continue with model:
                [Zk, suggestedBets, objVal] = CVaRModelRS(betas, RHS, bettingOptions, outcomes, oddCoef, Pk, Zk)
            else:
                # Not feasible, set users value to the threshold:
                [Zk, suggestedBets, objVal] = CVaRModelRS(betas, minThreshold, bettingOptions, outcomes, oddCoef, Pk, Zk)
            
            bets = ExtractBets(suggestedBets)
            return [Zk, bets, objVal, minRegret]
        else:
            # Use the same suggestion as the risk-neutral model
            return [Zk, bets, objVal, 0.]

    # Profile = Risk-Neutral:
    elif (profile == 'Risk-Neutral'):
        [Zk, suggestedBets, objVal] = CVaRModelRN(bettingOptions, oddCoef, Zk)
        bets = ExtractBets(suggestedBets)
        return [Zk, bets, objVal]

    # Profile = Risk-Averse:
    elif (profile == 'Risk-Averse'):
        [Zk, suggestedBets, objVal] = CVaRModelRA(betas, RHS, bettingOptions, outcomes, oddCoef, Pk, Zk)
        bets = ExtractBets(suggestedBets)
        return [Zk, bets, objVal]

