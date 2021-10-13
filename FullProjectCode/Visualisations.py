from re import X
from matplotlib import use
import numpy as np
import pandas as pd
import seaborn as sns
from statistics import mean
import matplotlib.pyplot as plt
from InterpolatingDistributions import InterpolateDists
from EvaluatingPValues import ReadInData, ReadInGridDB, ExtractSetScores, ObjectiveMetricROI
from CVaRModel import RunCVaRModel, CVaRModelRSThreshold

def test80Matches(DB, matchesFileName):
    # Test the ROI as an objective on a full test set of 80 matches
    # Plots:
    # 1a) User's Balance vs Match Number ($10 Budget)
    # 1b) User's Balance vs Match Number (Budget = Balance)
    # 2) Distribution of ROIs across 80 matches
    # 3) Distribution of Amount Bet across 80 matches
    # All plots consider 3 standard risk-profiles

    # Save figures to:
    #plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'
    plotsFolder ='C:/Uni/4thYearProject/repo/BeatTheOdds/ProjectDevelopmentCode/VisualisationOutputs/'
    saveFigures = True

    # Which plots to make:
    plot1 = False
    plot2 = True
    plot3 = True
    
    # Read in the matches, odds, and respective Pa and Pb values:
    matches = ReadInData(matchesFileName, False)
    
    # Set up risk profile parameters:
    profiles = ['Very-Averse', 'Averse', 'Neutral']
    usersBalanceA = {}
    usersBalanceB = {}
    startingBal = 100.
    budgetA = 10.
    percentOfBal = 0.3
    matchROIs = {}
    amountBet = {}
    for profile in profiles:
        # Plot 1a and 1b:
        usersBalanceA[profile] = [startingBal]
        usersBalanceB[profile] = [startingBal]
        
        # Plot 2:
        matchROIs[profile] = []

        # Plot 3:
        amountBet[profile] = []

    # Construct varying possible risk profiles:
    betsConsidered = [1,1,1,0,0]
    betasAsFloats = [0.1, 0.2, 0.3]
    riskProfiles = {'Very-Averse': [0.6, 0.5, 0.4], 'Averse': [0.8, 0.7, 0.6], 'Neutral': [1., 1., 1.]}

    # Find the best bets to place:
    for profile in riskProfiles:
        if (profile == 'Neutral'):
            CVaRProfile = 'Risk-Neutral'
        else:
            CVaRProfile = 'Risk-Averse'
        
        # Set up starting balance:
        newBalA = startingBal
        newBalB = startingBal

        # Run the model on all matches in the data set:
        for match in matches:
            # Check if we can bet on the game:
            if (match[68] != '4'):
                # Compute the interpolated distributions:
                Dists = InterpolateDists(float(match[66]), float(match[67]), DB)

                # Extract the required match details:
                matchScore = [float(match[30]), float(match[31])]
                outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

                # Run CVaR model: (using generic risk profile)
                [Zk, suggestedBets, objVal] = RunCVaRModel(betsConsidered,Dists['Match Score'],CVaRProfile,riskProfiles[profile],
                betasAsFloats,[float(match[58]),float(match[59])],[float(match[63]),float(match[62]),float(match[60]),
                float(match[61])],[float(match[65]),float(match[64])],oddsSS=[],oddsNumGames=[])

                # "place" these bets and the compute the ROI:
                [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
                matchROIs[profile].append(ROI)
                amountBet[profile].append(spent)

                # Keep track of the users budget:
                if (startingBal == 0.):
                    newBalA += budgetA * (returns - spent)
                    if (newBalB > (budgetA / percentOfBal)):
                        newBalB += newBalB * percentOfBal * (returns - spent)
                    else:
                        newBalB += budgetA * (returns - spent)
                    usersBalanceA[profile].append(newBalA)
                    usersBalanceB[profile].append(newBalB)
                else:
                    # Budget = Fixed:
                    if (newBalA > budgetA):
                        newBalA += budgetA * (returns - spent)
                    else:
                        newBalA += newBalA * (returns - spent)
                    usersBalanceA[profile].append(newBalA)

                    # Budget = Entire Balance (above starting balance, otherwise $10):
                    if ((newBalB - startingBal) > (budgetA / percentOfBal)):
                        newBalB += (newBalB - startingBal) * percentOfBal * (returns - spent)
                    else:
                        newBalB += budgetA * (returns - spent) 
                    usersBalanceB[profile].append(newBalB)
            else:
                print('Do not bet')
                matchROIs[profile].append(0)
                # amountBet[profile].append(0)
                usersBalanceA[profile].append(newBalA)
                usersBalanceB[profile].append(newBalB)

    if (plot1):
        # Show how the users budget changes across the 80 matches, for 3 generic profiles:
        for profile in riskProfiles:
            plt.plot(list(range(0,len(matches)+1)), usersBalanceA[profile], label = '{} = [{}, {}, {}]'.format(profile,
            riskProfiles[profile][0],riskProfiles[profile][1],riskProfiles[profile][2]))
        
        # Set labels:
        plt.title('User\'s Balance \n (Betting Budget of ${})'.format(budgetA), fontsize = 14)
        plt.xlabel('Match Number', fontsize = 12)
        plt.ylabel('User\'s Balance', fontsize = 12)
        plt.legend()
        plt.grid()
        
        # Print final balances:
        for profile in riskProfiles:
            print('Final Balance for {} Profile: '.format(profile), usersBalanceA[profile][-1])
            print('Lowest Balance for {} Profile: '.format(profile), min(usersBalanceA[profile]))

        if (saveFigures):
            plt.savefig(plotsFolder+'Users Balance using $10 Budget (RA Profiles)')
            plt.clf()
        else:
            plt.show()
        
        # Show how the users budget changes across the 80 matches, for 3 generic profiles:
        for profile in riskProfiles:
            plt.plot(list(range(0,len(matches)+1)), usersBalanceB[profile], label = '{} = [{}, {}, {}]'.format(profile,
            riskProfiles[profile][0],riskProfiles[profile][1],riskProfiles[profile][2]))
        
        # Set labels:
        plt.title('User\'s Balance \n (Betting Budget is {}% of the User\'s Balance)'.format(percentOfBal*100),fontsize = 14)
        plt.xlabel('Match Number',fontsize = 12)
        plt.ylabel('User\'s Balance',fontsize = 12)
        plt.legend()
        plt.grid()
        
        # Print final balances:
        for profile in riskProfiles:
            print('Final Balance for {} Profile: '.format(profile), usersBalanceB[profile][-1])
            print('Best Balance for {} Profile: '.format(profile), max(usersBalanceB[profile]))

        if (saveFigures):
            plt.savefig(plotsFolder+'Users Balance using Budget =  30% Balance (RA Profiles)')
            plt.clf()
        else:
            plt.show()
    
    if (plot2):
        # Create distribution plot for ROIs:
        plt.hist([matchROIs['Very-Averse'],matchROIs['Averse'],matchROIs['Neutral']], 
        color=['blue','green','red'],edgecolor='black',label=['Very-Averse = [{}, {}, {}]'.format(riskProfiles['Very-Averse'][0],
        riskProfiles['Very-Averse'][1],riskProfiles['Very-Averse'][2]),'Averse = [{}, {}, {}]'.format(riskProfiles['Averse'][0],
        riskProfiles['Averse'][1],riskProfiles['Averse'][2]),'Neutral  [{}, {}, {}]'.format(riskProfiles['Neutral'][0],
        riskProfiles['Neutral'][1],riskProfiles['Neutral'][2])],bins = 8)
        plt.legend()
        plt.title('Distribution of ROIs for an Individual Match', fontsize = 14)
        plt.xlabel('Individual Match ROIs',fontsize = 11)
        plt.ylabel('Frequency over the 80 Matches',fontsize = 11)

        # Compute the average ROI for a match:
        for profile in riskProfiles:
            print(mean(matchROIs[profile]))

        if (saveFigures):
            plt.savefig(plotsFolder+'Distribution of Match ROIs (New CVaR)')
            plt.clf()
        else:
            plt.show()

        # Smoothed density plots:
        df = pd.DataFrame()
        listRPs = []
        listROIs = []
        for profile in profiles:
            for ROI in matchROIs[profile]:
                listRPs.append(profile)
                listROIs.append(ROI)   
        df["Risk Profile"] = listRPs
        df["Individual Match ROIs"] = listROIs
        
        dis1 =sns.displot(df, x = "Individual Match ROIs", hue = "Risk Profile", kind = "kde", fill = True, bw_adjust = 0.5)#.set(title = 'Smoothed Density Plots\n(Distribution of Match ROIs)')
        dis1.fig.suptitle('Smoothed Density Plots\n(Distribution of Match ROIs)')
        if (saveFigures):
            plt.savefig(plotsFolder+'Smoohted Density Plot of Match ROIs')
            plt.clf()
        else:
            plt.show()

    if (plot3):
        # Amount Bet:
        plt.hist([amountBet['Very-Averse'],amountBet['Averse']], 
        color=['blue','green'],edgecolor='black',label=['Very-Averse = [{}, {}, {}]'.format(riskProfiles['Very-Averse'][0],
        riskProfiles['Very-Averse'][1],riskProfiles['Very-Averse'][2]),'Averse = [{}, {}, {}]'.format(riskProfiles['Averse'][0],
        riskProfiles['Averse'][1],riskProfiles['Averse'][2])],bins = 10)
        plt.legend()
        plt.title('Distribution of Amount Bet', fontsize = 14)
        plt.xlabel('Amount Bet (as a proportion of your budget)', fontsize = 11)
        plt.ylabel('Frequency over the 80 Matches', fontsize = 11)

        # Compute the average ROI for a match:
        for profile in riskProfiles:
            print(mean(amountBet[profile]))

        if (saveFigures):
            plt.savefig(plotsFolder+'Distribution of Amount Bet (New CVaR)')
            plt.clf()
        else:
            plt.show()

        # Smoothed density plots:
        df = pd.DataFrame()
        listRPs = []
        listAmountBet = []
        for profile in profiles:
            if (profile != 'Risk-Neutral'):    
                for ROI in amountBet[profile]:
                    listRPs.append(profile)
                    listAmountBet.append(ROI)   
        df["Risk Profile"] = listRPs
        df["Amount Bet (as a proportion of users budget)"] = listAmountBet
        
        dis = sns.displot(df, x = "Amount Bet (as a proportion of users budget)", hue = "Risk Profile",stat="density", common_norm = False)#.set(title = 'Smoothed Density Plots\n(Distribution of Amount Bet)')
        dis.fig.suptitle('Distribution of Amount Bet')
        if (saveFigures):
            plt.savefig(plotsFolder+'Smoohted Density Plot of Amount Bet')
            plt.clf()
        else:
            plt.show()

def test80MatchesRS(DB, matchesFileName):
    # Test the ROI as an objective on a full test set of 80 matches using a Risk-Seeking profile
    # Plots:
    # 1) User's Balance vs Match Number ($10 Budget - 3 constant regret measures)
    # 2) User's Balance vs Match Number ($10 budget - 9 dynamically changing regret measures)
    # 3) Distribution of ROIs across 80 matches (3 constant regret measures)
    # 4) Distribution of ROIs across 80 matches (9 dynamically changing regret measures)
    # 5) Distribution of Minimum Feasible Regrets

    # Save figures to:
    # plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'
    plotsFolder ='C:/Uni/4thYearProject/repo/BeatTheOdds/ProjectDevelopmentCode/VisualisationOutputs/'
    saveFigures = True

    # Which plots to make:
    plot1 = False
    plot2 = True
    plot3 = False
    plot4 = True
    plot5 = False
    smoothed = True
    
    # Read in the matches, odds, and respective Pa and Pb values:
    matches = ReadInData(matchesFileName, False)
    
    # Set up risk profile parameters:
    startingBal = 100.
    budgetA = 10.
    usersBalanceA = {}
    matchROIs = {}

    # Construct varying possible risk profiles:
    betsConsidered = [1,1,1,0,0]
    beta = 0.2
    userInputs = [2, 3, 4, 5]
    userInputsDynamic = [0.5, 1.]

    # Find which profiles we are using:
    profiles = []
    if (plot1 or plot3):
        # Convert to strings:
        for i in range(len(userInputs)):
            profiles.append(str(userInputs[i]))
    elif (plot2 or plot4):
       # Convert to strings:
        for i in range(len(userInputsDynamic)):
            profiles.append(str(userInputsDynamic[i]))
    
    # Append the risk-neutral profile for comparison:
    profiles.append('Risk-Neutral')

    # Find the best bets to place:
    for regret in profiles:
        if (regret == 'Risk-Neutral'):
            CVaRProfile = 'Risk-Neutral'
        else:
            CVaRProfile = 'Risk-Seeking'

        # Set up starting balance:
        newBalA = startingBal
        usersBalanceA[regret] = [startingBal]

        # Set up variables:
        matchROIs[regret] = []
        minRegrets = []

        # Run the model on all matches in the data set:
        for match in matches:
            # Check if we can bet on the game:
            if (match[68] != '4'):
                # Compute the interpolated distributions:
                Dists = InterpolateDists(float(match[66]), float(match[67]), DB)

                # Extract the required match details:
                matchScore = [float(match[30]), float(match[31])]
                outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

                if (CVaRProfile == 'Risk-Seeking'):
                    if (plot1):
                        # Run CVaR model:
                        [Zk, suggestedBets, objVal, minRegret] = RunCVaRModel(betsConsidered,Dists['Match Score'],CVaRProfile,float(regret),
                        beta,[float(match[58]),float(match[59])],[float(match[63]),float(match[62]),float(match[60]),
                        float(match[61])],[float(match[65]),float(match[64])],oddsSS=[],oddsNumGames=[])
                    elif (plot2):
                        # Compute the minimum regret:
                        [Zk, suggestedBets, objVal, minRegret] = RunCVaRModel(betsConsidered,Dists['Match Score'],CVaRProfile,10.,
                        beta,[float(match[58]),float(match[59])],[float(match[63]),float(match[62]),float(match[60]),
                        float(match[61])],[float(match[65]),float(match[64])],oddsSS=[],oddsNumGames=[])

                        # Re-run the model dynamically changing the users input based of the minimum value:
                        dynamicallyChangingRegret = minRegret + float(regret)
                        [Zk, suggestedBets, objVal, minRegret2] = RunCVaRModel(betsConsidered,Dists['Match Score'],CVaRProfile,dynamicallyChangingRegret,
                        beta,[float(match[58]),float(match[59])],[float(match[63]),float(match[62]),float(match[60]),
                        float(match[61])],[float(match[65]),float(match[64])],oddsSS=[],oddsNumGames=[])
                else:
                    if (plot1):
                        # Run CVaR model:
                        [Zk, suggestedBets, objVal] = RunCVaRModel(betsConsidered,Dists['Match Score'],CVaRProfile,float(regret),
                        beta,[float(match[58]),float(match[59])],[float(match[63]),float(match[62]),float(match[60]),
                        float(match[61])],[float(match[65]),float(match[64])],oddsSS=[],oddsNumGames=[])
                    elif (plot2):
                        # Compute the minimum regret:
                        [Zk, suggestedBets, objVal] = RunCVaRModel(betsConsidered,Dists['Match Score'],CVaRProfile,10.,
                        beta,[float(match[58]),float(match[59])],[float(match[63]),float(match[62]),float(match[60]),
                        float(match[61])],[float(match[65]),float(match[64])],oddsSS=[],oddsNumGames=[])

                # "place" these bets and the compute the ROI:
                [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
                matchROIs[regret].append(ROI)

                # Keep track of the users budget:
                if (newBalA < budgetA):
                    newBalA += newBalA * (returns - spent)
                else:
                    newBalA += budgetA * (returns - spent)
                 
                usersBalanceA[regret].append(newBalA)
                matchROIs[regret].append(ROI)
                minRegrets.append(minRegret)
            else:
                print('Do not bet')
                matchROIs[regret].append(0)
                usersBalanceA[regret].append(newBalA)

    # Show how the users budget changes across the 80 matches:
    if (plot1 or plot2):
        colours = ['lightsteelblue', 'cornflowerblue', 'royalblue', 'mediumblue','blue', 'navy']
        count = 0
        for regret in profiles:
            if (regret == 'Risk-Neutral'):
                plt.plot(list(range(0,len(matches)+1)), usersBalanceA[regret], label = 'Risk-Neutral')
            else:
                plt.plot(list(range(0,len(matches)+1)), usersBalanceA[regret], label = 'Regret = {}'.format(regret))
            count += 1

        # Set labels:
        plt.title('User\'s Balance \n(Betting budget of ${})'.format(budgetA), fontsize = 14)
        plt.xlabel('Match Number', fontsize = 11)
        plt.ylabel('User\'s Balance', fontsize = 11)
        plt.legend()
        
        # Print final balances:
        for regret in profiles:
            print('Final Balance for {} Profile: '.format(regret), usersBalanceA[regret][-1])
            print('Lowest Balance for {} Profile: '.format(regret), min(usersBalanceA[regret]))

        if (saveFigures):
            plt.savefig(plotsFolder+'Users Balance (regret, $10 Budget)')
            plt.clf()
        else:
            plt.show()
    
    if (plot3):
        # Create distribution plot for ROIs:
        plt.hist([matchROIs['2'],matchROIs['3'],matchROIs['4']],color=['blue','green','red'],edgecolor='black',
        label=['2','3','4'], bins = 5)
        plt.legend()
        plt.title('Distirbution of ROIs across Risk Profiles', fontsize = 14)
        plt.xlabel('Individual Match ROIs',fontsize = 11)
        plt.ylabel('Frequency', fontsize = 11)

        # Compute the average ROI for a match:
        for profile in profiles:
            print(mean(matchROIs[profile]))

        if (saveFigures):
            plt.savefig(plotsFolder+'Distribution of Match ROIs (Regret)')
            plt.clf()
        else:
            plt.show()

    if (plot4):
        # Create distribution plot for ROIs:
        plt.hist([matchROIs['0.5'],matchROIs['1.0'],matchROIs['Risk-Neutral']],color=['blue','green','red'],
        edgecolor='black',label=['0.5','1','Neutral'], bins = 5)
        plt.legend()
        plt.title('Distribution of ROIs across Risk Profiles', fontsize = 14)
        plt.xlabel('Individual Match ROIs', fontsize = 11)
        plt.ylabel('Frequency', fontsize = 11)

        # Compute the average ROI for a match:
        for profile in profiles:
            print(mean(matchROIs[profile]))

        if (saveFigures):
            plt.savefig(plotsFolder+'Distribution of Match ROIs (Regret)')
            plt.clf()
        else:
            plt.show()

        # Smoothed density plots:
        if (smoothed):
            df = pd.DataFrame()
            listRPs = []
            listROIs = []
            for regret in profiles:
                for ROI in matchROIs[regret]:
                    if (regret == 'Risk-Neutral'):
                        listRPs.append(regret)
                    else:
                        listRPs.append('Regret = +{}'.format(regret))
                    listROIs.append(ROI)   
            df["Risk Profile"] = listRPs
            df["Individual Match ROIs"] = listROIs
            
            dis = sns.displot(df, x = "Individual Match ROIs", hue = "Risk Profile", kind = "kde", fill = True, bw_adjust =0.5)#.set(title = 'Smoothed Density Plots\n(Distribution of Match ROIs)')
            dis.fig.suptitle('Smoothed Density Plots\n(Distribution of Match ROIs)')
            if (saveFigures):
                plt.savefig(plotsFolder+'Smoohted Density Plot of Match ROIs (Regret)')
                plt.clf()
            else:
                plt.show()

    if (plot5):
        # Create distribution plot for the minimum regrets:
        plt.hist(minRegrets, edgecolor='black', bins = 5)
        plt.legend()
        plt.title('Distirbution of the Threshold for the Feasible Regret')
        plt.xlabel('Minimum Feasible Regret')
        plt.ylabel('Frequency')

        if (saveFigures):
            plt.savefig(plotsFolder+'Distribution of Minimum Regrets')
            plt.clf()
        else:
            plt.show()

def test25Matches(DB, matchesFileName):
    # Test the ROI as an objective on a small test manually gathered.
    # Test multiple matches that I have collected odds data and their Pa and Pb values for.

    # Plots:
    # 1) ROI vs A single alpha value changing for 3 generic risk profiles
    #       - 3 plots, one for each alpha value
    # 2) Distribution of the Payoff and Amount Bet for each generic risk profile
    #       - 2 distribution plots per risk profile

    # Save figures to:
    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'
    saveFigures = False

    # Which plots to make:
    plot1 = True
    plot2 = True
    plot1b = True

    # Which version of CVaR model are we using:
    cVaR = 1
    
    # Read in the matches, odds, and respective Pa and Pb values:
    matches = ReadInData(matchesFileName)
    
    # Iterate through the matches we have data for:
    profiles = ['Averse', 'Less-Averse', 'Neutral']
    betas = ['20%', '33%', '50%']
    overallROIs = {}
    amountBet = {}
    payOffs = {}
    usersBudget = {}
    startingBudget = 100.
    bettingAmount = 10.
    for beta in betas:
        overallROIs[beta] = {}
        for profile in profiles:
            # Plot 1:
            overallROIs[beta][profile] = []

            # Plot 2:
            amountBet[profile] = []
            payOffs[profile] = []

            # Plot 1b:
            usersBudget[profile] = []

    # Construct varying possible risk profiles:
    betsConsidered = [1,1,1,0,0]
    betasAsFloats = [0.2, 1./3., 0.5]
    N = 30
    alphaValues = {}
    if (cVaR == 1):
        riskProfiles = {'Averse': {'20%': 0.67, '33%': 0.59, '50%': 0.49}, 'Less-Averse': {'20%': 0.83, '33%': 0.8,
        '50%': 0.75}, 'Neutral': {'20%': 1., '33%': 1., '50%': 1.}}
        alphaValues = {}
        for beta in betas:
            alphaValues[beta] = {}
            for profile in riskProfiles:
                if (beta == '20%'):
                    alphaValues[beta][profile] = np.linspace(riskProfiles[profile]['33%'],1.,N)
                elif (beta == '33%'):
                    alphaValues[beta][profile] = np.linspace(riskProfiles[profile]['50%'],riskProfiles[profile]['20%'],N)
                else:
                    alphaValues[beta][profile] = np.linspace(0.4,riskProfiles[profile]['33%'],N)
    elif (cVaR == 3):
        riskProfiles = {'Risk-Averse': {'20%': 4.33, '33%': 3.75, '50%': 2.17}, 'Risk-Neutral': {'20%': 7.02, '33%': 7.47,
        '50%': 5.67}, 'Risk-Seeking': {'20%': 10.68, '33%': 12.31, '50%': 10.31}}
        alphaValues = {}
        for beta in betas:
            alphaValues[beta] = {}
            for profile in riskProfiles:
                if (beta == '20%'):
                    alphaValues[beta][profile] = np.linspace(riskProfiles[profile]['33%'],riskProfiles['Risk-Seeking'][beta],N)
                elif (beta == '33%'):
                    alphaValues[beta][profile] = np.linspace(riskProfiles[profile]['50%'],riskProfiles[profile]['20%'],N)
                else:
                    alphaValues[beta][profile] = np.linspace(1.,riskProfiles[profile]['33%'],N)

    # Find the best bets to place:
    if (plot1):
        for beta in betas:
            for profile in riskProfiles:
                if (profile == 'Neutral'):
                    CVaRProfile = 'Risk-Neutral'
                else:
                    CVaRProfile = 'Risk-Averse'

                # Iterate through possible alpha_3 values:
                for alpha in alphaValues[beta][profile]:
                    # Set up the other 2 alpha values:
                    alphasToUse = []
                    for value in riskProfiles[profile]:
                        if (value == beta):
                            alphasToUse.append(alpha)
                        else:
                            alphasToUse.append(riskProfiles[profile][value])

                    # Reset Spent and return counters:
                    amountSpent = 0.
                    amountReturned = 0.

                    # Run the model on all matches in the data set:
                    for match in matches:
                        # Compute the interpolated distributions:
                        Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

                        # Extract the required match details:
                        winner = 1
                        matchScore = [float(match[10]), float(match[11])]
                        setScores = ExtractSetScores(match[8])
                        outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

                        # Run CVaR model: (using generic risk profile)
                        [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],CVaRProfile, alphasToUse,
                        betasAsFloats,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
                        float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])

                        # "place" these bets and the computed the ROI:
                        [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
                        amountSpent += spent
                        amountReturned += returns
                    
                    # Compute the average ROI for this profile and alpha values:
                    overallROIs[beta][profile].append(((amountReturned - amountSpent) / amountSpent) * 100.)
    
    # Produce the Distribution of Amount Bet and Payoff for each Generic Risk Profile:
    if (plot2):
        for profile in riskProfiles:
            if (profile == 'Neutral'):
                CVaRProfile = 'Risk-Neutral'
            else:
                CVaRProfile = 'Risk-Averse'
                
            # Set up alphas to use:
            alphasToUse = [riskProfiles[profile]['20%'],riskProfiles[profile]['33%'],riskProfiles[profile]['50%']] 
            
            # Start the usersBudget at $x:
            budget = startingBudget
            usersBudget[profile].append(budget)

            # Run the model on all matches in the data set:
            for match in matches:
                # Compute the interpolated distributions:
                Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

                # Extract the required match details:
                winner = 1
                matchScore = [float(match[10]), float(match[11])]
                setScores = ExtractSetScores(match[8])
                outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

                # Run CVaR model:
                [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],CVaRProfile, alphasToUse,
                betasAsFloats,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
                float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])

                # "place" these bets and the computed the ROI:
                [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
                amountBet[profile].append(spent)
                payOffs[profile].append(returns - spent)

                # Keep track of the users budget:
                if (budget > bettingAmount):
                    budget += bettingAmount * (returns - spent)
                else:
                    budget += budget * (returns - spent)
                usersBudget[profile].append(budget)

    if (plot1):
        # Create a plot of the 3 sequences of ROIs, for all 3 risk-profiles:
        fig, axes = plt.subplots(1, 3,sharey=False, figsize = [20, 12])
        fig.suptitle('ROI as the Users Risk Profile Changes', fontsize = 25)
        counter = 0
        for beta in betas:
            for profile in overallROIs[beta]:
                axes[counter].plot(alphaValues[beta][profile], overallROIs[beta][profile], label = profile)
        
            # Set subplot labels:
            axes[counter].set_title('{} Quantile'.format(beta))
            axes[counter].set_xlabel('User Response for the {} Quantile'.format(beta))
            axes[counter].set_ylabel('ROI as a Percentage')
            axes[counter].legend(['Averse','Less-Averse','Neutral'])
            counter += 1
        
        if (saveFigures):
            plt.savefig(plotsFolder+'ROIvsRiskProfile 2 - All Profiles over 25 Matches')
            plt.clf()
        else:
            plt.show()
    
    if (plot2):
        # Create distribution plots:
        # Amount Bet:
        plt.hist([amountBet['Averse'],amountBet['Less-Averse'],amountBet['Neutral']], 
        color=['blue','green','red'],edgecolor='black',label=['Averse = [{}, {}, {}]'.format(riskProfiles['Averse']['20%'],
        riskProfiles['Averse']['33%'],riskProfiles['Averse']['50%']),'Less-Averse = [{}, {}, {}]'.format(riskProfiles['Less-Averse']['20%'],
        riskProfiles['Less-Averse']['33%'],riskProfiles['Less-Averse']['50%']),'Neutral  [{}, {}, {}]'.format(riskProfiles['Neutral']['20%'],
        riskProfiles['Neutral']['33%'],riskProfiles['Neutral']['50%'])],bins = 4)
        plt.legend()
        plt.xlabel('Amount Bet (as a proportion of your budget)')
        plt.ylabel('Frequency over the 25 Matches')
        if (saveFigures):
            plt.savefig(plotsFolder+'Distribution of Amount Bet 3 - All Profiles over 25 Matches')
            plt.clf()
        else:
            plt.show()

        # PayOffs:
        plt.hist([payOffs['Averse'],payOffs['Less-Averse'],payOffs['Neutral']], 
        color=['blue','green','red'],edgecolor='black',label=['Averse = [{}, {}, {}]'.format(riskProfiles['Averse']['20%'],
        riskProfiles['Averse']['33%'],riskProfiles['Averse']['50%']),'Less-Averse = [{}, {}, {}]'.format(riskProfiles['Less-Averse']['20%'],
        riskProfiles['Less-Averse']['33%'],riskProfiles['Less-Averse']['50%']),'Neutral  [{}, {}, {}]'.format(riskProfiles['Neutral']['20%'],
        riskProfiles['Neutral']['33%'],riskProfiles['Neutral']['50%'])],bins = 4)
        plt.legend()
        plt.xlabel('Payoff (irrespective of the amount bet)')
        plt.ylabel('Frequency over the 25 Matches')
        if (saveFigures):
            plt.savefig(plotsFolder+'Distribution of PayOffs 3 - All Profiles over 25 Matches')
            plt.clf()
        else:
            plt.show()
        
    if (plot1b):
        # Show how the users budget changes across the 25 matches, for 3 generic profiles:
        for profile in riskProfiles:
            plt.plot(list(range(0,len(matches)+1)), usersBudget[profile], label = '{} = [{}, {}, {}]'.format(profile,
            riskProfiles[profile]['20%'],riskProfiles[profile]['33%'],riskProfiles[profile]['50%']))
        
        # Set labels:
        plt.title('Users Budget over 25 Matches (betting budget of ${})'.format(bettingAmount))
        plt.xlabel('Match Number')
        plt.ylabel('Users Budget (Starting at ${})'.format(startingBudget))
        plt.legend()
        
        if (saveFigures):
            plt.savefig(plotsFolder+'Users Budget vs Risk Profile - Over 25 Matches')
            plt.clf()
        else:
            plt.show()

def test1Match(DB, matchesFileName):
    # Test the ROI on just a sinlge match for plotting purposes.
    # Plots:
    # 1) ROI vs A single alpha value changing for 3 generic risk profiles
    #       - 3 plots, one for each alpha value
    # 2) Suggested Bets made vs a single changing alpha value for 3 generic risk profiles
    #       - This creates 3x3 axis on a figure (each row is the standard risk profile and each column is the changing alpha value)
    # 2b) Suggested Bets made vs single changing alpha value for a single, standard risk-averse profile
    #       - ONLY contains 3 axes (simplified version of plot 2 for ease of explaining)
    # 3) Suggested Bets made vs single constraint profiles

    # Save figures to:
    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'
    saveFigures = True

    # Which plots to make:
    plot1 = False
    plot2 = False
    plot2b = True
    plot3 = False # Must do by itself

    # Set up required data storing structures:
    ROIs = {}
    ROIs['Very Averse'] = []
    ROIs['Averse'] = []
    ROIs['Neutral'] = []
    allROIs = {}

    # Add the beta keys to all the required dictionarys:
    betas = ['10%','20%','30%']
    betsMade = {}
    bets = {}
    betsToPlot = {}
    totalSpent = {}
    for beta in betas:
        # Plot 1:
        allROIs[beta] = {}
        
        totalSpent[beta] = {}
        betsMade[beta] = {}
        bets[beta] = {}
        betsToPlot[beta] = {}

        for profile in ROIs:
            totalSpent[beta][profile] = []
            betsMade[beta][profile] = {}
            bets[beta][profile] = {}
            betsToPlot[beta][profile] = {}
        
    # Read in data and extract ONLY the first match:
    match = ReadInData(matchesFileName)[0]

    # Construct varying possible risk profiles:
    betsConsidered = [1,1,1,0,0]
    betasAsFloats = [0.1, 0.2, 0.3]
    N = 50
    alphaValues = {}
    riskProfiles = {'Very Averse': {'10%': 0.8, '20%': 0.76, '30%': 0.67}, 'Averse': {'10%': 0.8, '20%': 0.6,
    '30%': 0.4}, 'Neutral': {'10%': 1., '20%': 1., '30%': 1.}}
    alphaValues = {}
    for beta in betas:
        alphaValues[beta] = {}
        for profile in riskProfiles:
            alphaValues[beta][profile] = np.linspace(0., 1., N)

    # Compute the interpolated distributions:
    Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

    # Extract the required match details:
    matchScore = [float(match[10]), float(match[11])]
    outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

    if (plot1 or plot2 or plot2b):
        # Find the best bets to place:
        for profile in riskProfiles:

            # Get the official name of the profile:
            if (profile == 'Neutral'):
                CVaRProfile = 'Risk-Neutral'
            else:
                CVaRProfile = 'Risk-Averse'

            # Iteratre through the different alpha values we can change:
            counter = 0
            for beta in allROIs:
                ROIs[profile] = []

                # Iterate through possible alpha values:
                for alpha in alphaValues[beta][profile]:
                    # Set up the other 2 alpha values:
                    alphasToUse = []
                    for value in riskProfiles[profile]:                     
                        if (value == beta):
                            alphasToUse.append(alpha)
                        else:
                            alphasToUse.append(riskProfiles[profile][value])

                    # Run CVaR model:
                    [Zk, suggestedBets, objVal] = RunCVaRModel(betsConsidered,Dists['Match Score'],CVaRProfile, alphasToUse,
                    betasAsFloats,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
                    float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])
                    
                    # Alpha Values used:
                    alphaVals = '{}, {}, {}'.format(round(alphasToUse[0],3), round(alphasToUse[1],3), 
                    round(alphasToUse[2],3))

                    # Store the bets made for this set of alpha values:
                    betsMade[beta][profile][alphaVals] = suggestedBets

                    # "place" these bets and the computed the ROI:
                    [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)

                    # Append it to the ROIS dictionary for this profile:
                    ROIs[profile].append(ROI)
                    totalSpent[beta][profile].append(round(spent,3))
                
                # Add to the overall dictionary of ROIs and amount Bet:
                allROIs[beta][profile] = ROIs[profile]
                counter += 1
    
    if (plot3):
        # Profile:
        CVaRProfile = 'Risk-Averse'
        betsMade = {}
        bets = {}
        betsToPlot = {}
           
        # Iteratre through the different alpha values we can change:
        counter = 0
        for beta in allROIs:
            betsMade[beta] = {}
            bets[beta] = {}
            betsToPlot[beta] = {}
            totalSpent[beta] = []

            # Iterate through possible alpha values:
            alphasToUse = [1.5, 1.5, 1.5]
            changingValues = np.linspace(0.,1.,50)
            for alpha in changingValues:
                # Set up the other 2 alpha values:
                alphasToUse[counter] = alpha

                # Run CVaR model:
                [Zk, suggestedBets, objVal] = RunCVaRModel(betsConsidered,Dists['Match Score'],CVaRProfile, alphasToUse,
                betasAsFloats,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
                float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])
                
                # Alpha Values used:
                alphaVals = '{}, {}, {}'.format(round(alphasToUse[0],3), round(alphasToUse[1],3), 
                round(alphasToUse[2],3))

                # Store the bets made for this set of alpha values:
                betsMade[beta][alphaVals] = suggestedBets

                # "place" these bets and the computed the ROI:
                [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)

                # Append it to the ROIS dictionary for this profile:
                totalSpent[beta].append(spent)
            counter += 1

    if (plot1):
        # Create a plot of the 3 sequences of ROIs:
        fig, axes = plt.subplots(1, 3,sharey=False, figsize = [20, 12])
        fig.suptitle('ROI as the Users Risk Profile Changes', fontsize = 25)
        counter = 0
        for beta in allROIs:
            for profile in ROIs:
                axes[counter].plot(alphaValues[beta][profile], allROIs[beta][profile], label = profile)

            # Set subplot labels:
            axes[counter].set_title('{} Quantile'.format(beta))
            axes[counter].set_xlabel('User Response for the {} Quantile'.format(beta))
            axes[counter].set_ylabel('ROI as a Percentage')
            axes[counter].legend(['Very Averse','Averse','Neutral'])
            counter += 1
        
        if (saveFigures):
            plt.savefig(plotsFolder+'ROI vs Risk Profiles 3 - All Profiles (Single Match)')
            plt.clf()
        else:
            plt.show()

    if (plot2):
        # Keep track of the betting options that were considered by each profile for this match:
        tol = 1e-06
        for beta in betsMade:
            for profile in betsMade[beta]:
                for bet in suggestedBets:
                    # Initially Set to zero:
                    bets[beta][profile][bet] = 0.
                    for alphas in betsMade[beta][profile]:
                        # Sum up the amount Bet on this specific bet over the changing alpha values:
                        bets[beta][profile][bet] += betsMade[beta][profile][alphas][bet]

        # Check which ones were actually considered:
        for beta in bets:
            for profile in bets[beta]:
                for bet in bets[beta][profile]:
                    if (bets[beta][profile][bet] > tol):
                        # Record these values for plotting:
                        betsToPlot[beta][profile][bet] = []
                        for alphas in betsMade[beta][profile]:
                            betsToPlot[beta][profile][bet].append(betsMade[beta][profile][alphas][bet])

        # Plot the bets:
        fig, axes = plt.subplots(3, 3,sharey=False, figsize = [12, 15])
        fig.suptitle('Amount Bet on Various Bets as the Users Risk Profile Changes', fontsize = 20)

        # Set up figure labels:
        fig.supxlabel('Response the Beta Quantile')
        fig.supylabel('The Generic Risk Profile Used')
        cols = ['{} Quantile Response'.format(beta) for beta in betas]
        rows = ['{}'.format(profile) for profile in riskProfiles]
        for ax, col in zip(axes[0], cols):
            ax.set_title(col)
        for ax, row in zip(axes[:,0], rows):
            ax.set_ylabel(row, rotation=90, size='large')

        # Plot the various lines:
        counter2 = 0
        for beta in betsToPlot:
            counter1 = 0
            for profile in betsToPlot[beta]:
                labels = []
                for plot in betsToPlot[beta][profile]:
                    axes[counter1, counter2].plot(alphaValues[beta][profile], betsToPlot[beta][profile][plot])
                    labels.append(plot)

                # Plot the total amount spent too:
                axes[counter1, counter2].plot(alphaValues[beta][profile], totalSpent[beta][profile])
                labels.append('Total Amount Spent')

                # Set subplot labels:
                axes[counter1,counter2].legend(labels, loc = "upper left")
                counter1 += 1
            counter2 += 1

        # fig.legend(labels, loc = (0.8,0.77))
        if (saveFigures):
            plt.savefig(plotsFolder+'Amount Bet 3 - All Risk Profiles')
            plt.clf()
        else:
            plt.show()
        
    if (plot2b):
        # Keep track of the betting options that were considered by each profile for this match:
        tol = 1e-06
        # Just considering a single standard profile:
        profile = 'Averse'
        for beta in betsMade:
            for bet in suggestedBets:
                # Initially Set to zero:
                bets[beta][profile][bet] = 0.
                for alphas in betsMade[beta][profile]:
                    # Sum up the amount Bet on this specific bet over the changing alpha values:
                    bets[beta][profile][bet] += betsMade[beta][profile][alphas][bet]

        # Check which ones were actually considered:
        for beta in bets:
            for bet in bets[beta][profile]:
                if (bets[beta][profile][bet] > tol):
                    # Record these values for plotting:
                    betsToPlot[beta][profile][bet] = []
                    for alphas in betsMade[beta][profile]:
                        betsToPlot[beta][profile][bet].append(betsMade[beta][profile][alphas][bet])

        # Plot the bets:
        fig, axes = plt.subplots(1, 3,sharey=True, figsize = [20, 8])
        fig.suptitle('Portfolio Analysis \n (All CVaR constraints considered)', fontsize = 22)

        # Set up figure labels:
        fig.supylabel('Proportion of Budget Bet \n over a Single Match', fontsize = 16)
        fig.supxlabel('Risk Profile Used ([$\u03B1_{0.1}$, $\u03B1_{0.2}$, $\u03B1_{0.3}$])', fontsize = 16)

        # Plot the various lines:
        counter = 0
        for beta in betsToPlot:
            labels = []
            for plot in betsToPlot[beta][profile]:
                axes[counter].plot(alphaValues[beta][profile], betsToPlot[beta][profile][plot])
                labels.append(plot)

            # Plot the total amount spent too:
            axes[counter].plot(alphaValues[beta][profile], totalSpent[beta][profile])
            labels.append('Total Amount Bet')

            # Set subplot labels:
            if (beta == '10%'):
                axes[counter].set_xlabel('[$\u03B1_{0.1}$, 0.6, 0.4]')
            elif (beta == '20%'):
                axes[counter].set_xlabel('[0.8, $\u03B1_{0.2}$, 0.4]')
            else:
                axes[counter].set_xlabel('[0.8, 0.6, $\u03B1_{0.3}$]')
            axes[counter].legend(labels, loc = "upper left")
            axes[counter].grid()
            counter += 1

        if (saveFigures):
            plt.savefig(plotsFolder+'Individual Bet Plots - All Constraints (New CVaR Model)')
            plt.clf()
        else:
            plt.show()
    
    if (plot3):
        # Keep track of the betting options that were considering for this match:
        tol = 1e-06
        bets[beta] = {}
        for beta in betsMade:
            for bet in suggestedBets:
                # Initially Set to zero:
                bets[beta][bet] = 0.
                for alphas in betsMade[beta]:
                    # Sum up the amount Bet on this specific bet over the changing alpha values:
                    bets[beta][bet] += betsMade[beta][alphas][bet]

        # Check which ones were actually considered:
        for beta in bets:
            for bet in bets[beta]:
                if (bets[beta][bet] > tol):
                    # Record these values for plotting:
                    betsToPlot[beta][bet] = []
                    for alphas in betsMade[beta]:
                        betsToPlot[beta][bet].append(betsMade[beta][alphas][bet])

        # Plot the bets:
        fig, axes = plt.subplots(1, 3,sharey=True, figsize = [20, 8])
        fig.suptitle('Portfolio Analysis \n (Isolating the CVaR Constraints)', fontsize = 24)

        # Set up figure labels:
        fig.supylabel('Proportion of Budget Bet \n over a Single Match', fontsize = 16)
        fig.supxlabel('Proportion of Budget the user is willing to lose in the Beta Quantile ($\u03B1_{\u03B2}$)', fontsize = 16)

        # Plot the various lines:
        counter = 0
        for beta in betsToPlot:
            labels = []
            for plot in betsToPlot[beta]:
                axes[counter].plot(changingValues, betsToPlot[beta][plot])
                labels.append(plot)

            # Plot the total amount spent too:
            axes[counter].plot(changingValues, totalSpent[beta])
            labels.append('Total Amount Bet')

            # Set subplot labels:
            axes[counter].set_xlabel('{} Quantile'.format(beta))
            axes[counter].legend(labels, loc = "upper left")
            axes[counter].grid()
            counter += 1

        # Print the distributions:
        print(Dists)

        if (saveFigures):
            plt.savefig(plotsFolder+'Individual Bet Plots - Isolating Constraints (New CVaR Model)')
            plt.clf()
        else:
            plt.show()

def test1MatchRS(DB, matchesFileName):
     # Test the ROI on just a sinlge match using the Risk-Seeking model for plotting purposes.
    # Plots:
    # 1) ROI vs User Input changing
    # 2) Suggested Bets made vs User Input changing

    # Save figures to:
    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'
    saveFigures = True

    # Which plots to make:
    plot1 = False
    plot2 = True

    # Set up required data storing structures:
    ROIs = []

    # Add the beta keys to all the required dictionarys:
    betas = ['20%']
    betsMade = {}
    bets = {}
    betsToPlot = {}
    totalSpent = []

    # Read in data and extract ONLY the first match:
    match = ReadInData(matchesFileName, True)[0]

    # Construct varying possible risk profiles:
    betsConsidered = [1,1,1,0,0]
    beta = 0.2
    N = 50
    
    # Compute the threshold for minimum amount of regret:
    threshold = 2.526 + 0.2
    userInputs = np.linspace(threshold, 4., N)

    # Compute the interpolated distributions:
    Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

    # Extract the required match details:
    matchScore = [float(match[10]), float(match[11])]
    outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

    # Iteratre through the different alpha values we can change:
    for regret in userInputs:
        # Run CVaR model:
        [Zk, suggestedBets, objVal, minRegret] = RunCVaRModel(betsConsidered,Dists['Match Score'],'Risk-Seeking', regret,
        beta,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
        float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])
        
        # Alpha Values used:
        regret = round(regret,3)

        # Store the bets made for this set of alpha values:
        betsMade[regret] = suggestedBets

        # "place" these bets and the computed the ROI:
        [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)

        # Append it to the ROIS dictionary for this profile:
        ROIs.append(round(100 * objVal, 2))
        totalSpent.append(round(spent,3))
    
    if (plot1):
        # Plot the ROI as the user input changes:
        plt.plot(userInputs, ROIs)
        plt.axvline(x=2.526, color = 'red', linestyle = '--')
        plt.title('Expected ROI for a Risk-Seeking Profile')
        plt.xlabel('User\'s Regret Level ($\u03B1_{0.2}$)')
        plt.ylabel('Expected ROI')
        plt.legend(labels = ['Expected ROI', 'Minimum Amount of Regret Achievable'])
        plt.grid()

        if (saveFigures):
            plt.savefig(plotsFolder+'Expected ROI Regret Plot (Single match)')
            plt.clf()
        else:
            plt.show()
    
    if (plot2):
        # Keep track of the betting options that were considered by each profile for this match:
        tol = 1e-06
        for bet in suggestedBets:
            # Initially Set to zero:
            bets[bet] = 0.
            for regret in betsMade:
                # Sum up the amount Bet on this specific bet over the changing alpha values:
                bets[bet] += betsMade[regret][bet]

        # Check which ones were actually considered:
        for bet in bets:
            if (bets[bet] > tol):
                # Record these values for plotting:
                betsToPlot[bet] = []
                for regret in betsMade:
                    betsToPlot[bet].append(betsMade[regret][bet])

        # Plot the bets:
        labels = []
        for plot in betsToPlot:
            plt.plot(userInputs, betsToPlot[plot])
            labels.append(plot)

        # Plot the total amount spent too:
        plt.plot(userInputs, totalSpent)
        labels.append('Total Amount Bet')

        # Set up the labels:
        plt.title('Portfolio Analysis for a Risk-Seeking Profile')
        plt.xlabel('User\'s Regret Level ($\u03B1_{0.2}$)')
        plt.ylabel('Proportion of Budget Bet')
        plt.legend(labels = labels)

        if (saveFigures):
            plt.savefig(plotsFolder+'Amount Bet Regret Plot')
            plt.clf()
        else:
            plt.show()

def testNewCVaRConstraints25Matches(DB, matchesFileName):
    # Playing around with the risk profile parameters to understand the new constraints.
    
    # Save figures to:
    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'
    saveFigures = False

    # Set up initial risk profile:
    riskProfile = [5., 3., 2.]
    betasAsFloats = [0.2, 0.33, 0.5]
    riskMetrics = []
    avRiskProfiles = {}
    avRiskProfiles['Risk-Averse'] = [7.47, 4.48, 5.23]
    avRiskProfiles['Risk-Neutral'] = [28., 18.2, 8.07]
    avRiskProfiles['Risk-Seeking'] = [64.29, 35.14, 10.93]

    # Set up structures to store info:
    overallROI = []
    amountBet = 0.
    amountReturned = 0.
    betsConsidered = [1,1,1,0,0]
    N = 100
    alphaIncs = [(95. - 5.) / N, (57. - 3.) / N, (18. - 2.) / N]

    # Read in data:
    matches = ReadInData(matchesFileName)

    # Run the model, incrementally making the risk profile more open to risk:
    for i in range(N):
        # Compute new risk Profile:
        risk = 0.
        for j in range(len(riskProfile)):
            riskProfile[j] += alphaIncs[j]

            # Compute the Risk metric:
            risk += betasAsFloats[j] * riskProfile[j]
        riskMetrics.append(risk)

        # Reset metrics:
        amountBet = 0.
        amountReturned = 0.

        # Look at all 25 matches:
        for match in matches:
            # Compute the interpolated distributions:
            Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

            # Extract the required match details:
            winner = 1
            matchScore = [float(match[10]), float(match[11])]
            setScores = ExtractSetScores(match[8])
            outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

            # Run the CVaR Model with this profile
            [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],riskProfile,
            betasAsFloats,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
            float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])

            # "place" these bets and the computed the ROI:
            [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
            
            # Append to the dictionary storing the amount Bet:
            amountBet += spent
            amountReturned += returns
        
        # Compute the OverallROI for this specific risk profile:
        overallROI.append(((amountReturned - amountBet) / amountBet) * 100.)

    # Plot the overallROI against the Risk Metric:
    plt.plot(riskMetrics, overallROI)

    # Set up labels and titles:
    plt.xlabel('Risk Metric of the Profile Used')
    plt.ylabel('Overall ROI over 25 Matches')

    if (saveFigures):
        plt.savefig(plotsFolder+'Overall ROI vs Risk Metric (All 25 Matches, 3rd Constraints)')
        plt.clf()
    else:
        plt.show()

    # Look at all 25 matches for the average risk profile:
    amountBet = {}
    payOff = {}
    for avProfile in avRiskProfiles:
        amountBet[avProfile] = []
        payOff[avProfile] = []
        for match in matches:
            # Compute the interpolated distributions:
            Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

            # Extract the required match details:
            winner = 1
            matchScore = [float(match[10]), float(match[11])]
            setScores = ExtractSetScores(match[8])
            outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

            # Run the CVaR Model with this profile
            [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],avRiskProfiles[avProfile],
            betasAsFloats,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
            float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])

            # "place" these bets and the computed the ROI:
            [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
            
            # Append to the dictionary storing the amount Bet:
            amountBet[avProfile].append(spent)
            payOff[avProfile].append(ROI)
    
    # Plot the distribution of payoffs and amount Bet:
    plt.hist([amountBet['Risk-Averse'],amountBet['Risk-Neutral'],amountBet['Risk-Seeking']], 
    color=['blue','green','red'],edgecolor='black',label=['Risk-Averse','Risk-Neutral','Risk-Seeking'],bins = 4)
    plt.legend()
    plt.xlabel('Amount Bet (as a proportion of your budget)')
    plt.ylabel('Frequency over the 25 Matches')
    if (saveFigures):
        plt.savefig(plotsFolder+'Distribution of Amount Bet 2 - All Profiles over 25 Matches')
        plt.clf()
    else:
        plt.show()

    # PayOffs:
    plt.hist([payOff['Risk-Averse'],payOff['Risk-Neutral'],payOff['Risk-Seeking']], 
    color=['blue','green','red'],edgecolor='black',label=['Risk-Averse','Risk-Neutral','Risk-Seeking'],bins = 4)
    plt.legend()
    plt.xlabel('Payoff (irrespective of the amount Bet)')
    plt.ylabel('Frequency over the 25 Matches')
    if (saveFigures):
        plt.savefig(plotsFolder+'Distribution of PayOffs 2 - All Profiles over 25 Matches')
        plt.clf()
    else:
        plt.show()
    
def testNewCVaRConstraints1Match(DB, matchesFileName):
    # Playing around with the risk profile parameters to understand the new constraints.
    
    # Save figures to:
    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'
    saveFigures = False

    # Set up initial risk profile:
    riskProfile = [5.]#, 3., 2.]
    betasAsFloats = [0.2]#, 0.33, 0.5]
    riskMetrics = []

    # Set up structures to store info:
    betsMade = {}
    bets = {}
    betsToPlot = {}
    amountBet = []
    betsConsidered = [1,1,1,0,0]
    N = 100
    alphaIncs = [(18. - 2.) / N]#, (57. - 3.) / N, (18. - 2.) / N]

    # Read in data:
    match = ReadInData(matchesFileName)[0]

    # Compute the interpolated distributions:
    Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

    # Extract the required match details:
    winner = 1
    matchScore = [float(match[10]), float(match[11])]
    setScores = ExtractSetScores(match[8])
    outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

    # Run the model, incrementally making the risk profile more open to risk:
    for i in range(N):
        # Compute new risk Profile:
        risk = 0.
        for j in range(len(riskProfile)):
            riskProfile[j] += alphaIncs[j]

            # Compute the Risk metric:
            risk += betasAsFloats[j] * riskProfile[j]
        riskMetrics.append(risk)

        # Run the CVaR Model with this profile
        [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],riskProfile,
        betasAsFloats,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
        float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])

        # Store the bets placed:
        betsMade[risk] = suggestedBets

        # "place" these bets and the computed the ROI:
        [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
        
        # Append to the dictionary storing the amount Bet:
        amountBet.append(spent)    

    # Keep track of the betting options that were considered by each profile for this match:
    tol = 1e-06
    for bet in suggestedBets:
        # Initially Set to zero:
        bets[bet] = 0.
        for profile in betsMade:
            # Sum up the amount Bet on this specific bet over the changing alpha values:
            bets[bet] += betsMade[profile][bet]

    # Check which ones were actually considered:
    for bet in bets:
        if (bets[bet] > tol):
            # Record these values for plotting:
            betsToPlot[bet] = []
            for profile in betsMade:
                betsToPlot[bet].append(betsMade[profile][bet])

    # Plot the amount Bet on the various bets against the risk metric:
    for bet in betsToPlot:
        plt.plot(riskMetrics, betsToPlot[bet], label = bet)

    # Also plot the amount Bet overall:
    plt.plot(riskMetrics, amountBet, label = 'Total Amount Bet')

    # Set up labels and titles:
    plt.xlabel('Risk Metric of the Profile Used')
    plt.ylabel('Amount Bet')
    plt.legend()

    if (saveFigures):
        plt.savefig(plotsFolder+'Overall ROI vs Risk Metric (All 25 Matches, 3rd Constraints)')
        plt.clf()
    else:
        plt.show()

def testRegretConstraints(DB, matchesFileName):
    # Test the Regret Measure constraints in the CVaR model.

    # Read in data and extract ONLY the first match:
    match = ReadInData(matchesFileName)[0]

    # Compute the interpolated distributions:
    Dists = InterpolateDists(float(match[26]), float(match[27]), DB)
    print(Dists)

    # Extract the required match details:
    matchScore = [float(match[10]), float(match[11])]
    outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

    # Set up the risk parameters:
    # profile = 'Risk-Seeking'
    profile = 'Risk-Averse'
    betsConsidered = [1,1,1,0,0]
    #betas = 0.2
    # alphas = 2.5
    betas = [0.1, 0.2, 0.30]
    alphas = [1.5,1.5,0.17]

    # Run CVaR model:
    
    [Zk, suggestedBets, objVal] = RunCVaRModel(betsConsidered,Dists['Match Score'],profile,alphas,betas,
    [float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
    float(match[23])],[float(match[24]),float(match[25])])
   
    # "place" these bets and the computed the ROI:
    [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
    print(suggestedBets)
    print(spent)
    print(returns)
  
def main():
    #outcome = '2-0'
    #zk = {'2-0':{'bet 1':2.2,'bet 2': 0.,'bet 3': 1.6,'bet 4': 0.}, '2-1':{'bet 1':2.2,'bet 2': 0.,'bet 3': 0.,'bet 4': 1.8},
    #'0-2':{'bet 1':0.,'bet 2':1.8,'bet 3': 1.6,'bet 4': 0.},'1-2':{'bet 1':0.,'bet 2':1.8,'bet 3':0.,'bet 4':1.8}}
    #bets = {'bet 1':2.5,'bet 2': 3.2,'bet 3': 0.,'bet 4': 1.2} 
    #print(ObjectiveMetricROI(outcome, zk, bets))
    
    # Test for CVaR Model:
    DB = ReadInGridDB('ModelDistributions2.csv')
    #testRegretConstraints(DB, '2018_19MatchesWithOdds.csv')
    test80Matches(DB, 'testSetForCalibrationWithROIWithManualyAddedDataWithPValues.csv')
    #test1MatchRS(DB, '2018_19MatchesWithOdds.csv')

if __name__ == "__main__":
    main()