from re import X
import numpy as np
import matplotlib.pyplot as plt
from InterpolatingDistributions import InterpolateDists
from EvaluatingPValues import ReadInData, ReadInGridDB, ExtractSetScores, ObjectiveMetricROI
from CVaRModel import RunCVaRModel

def test25Matches(DB, matchesFileName):
    # Test the ROI as an objective on a small test manually gathered.
    # Test multiple matches that I have collected odds data and their Pa and Pb values for.

    # Plots:
    # 1) ROI vs A single alpha value changing for 3 generic risk profiles
    #       - 3 plots, one for each alpha value
    # 2) Distribution of the Payoff and Amount betted for each generic risk profile
    #       - 2 distribution plots per risk profile

    # Save figures to:
    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'
    saveFigures = True

    # Which plots to make:
    plot1 = False
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
    amountBetted = {}
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
            amountBetted[profile] = []
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
                        [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],alphasToUse,
                        betasAsFloats,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
                        float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])

                        # "place" these bets and the computed the ROI:
                        [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
                        amountSpent += spent
                        amountReturned += returns
                    
                    # Compute the average ROI for this profile and alpha values:
                    overallROIs[beta][profile].append(((amountReturned - amountSpent) / amountSpent) * 100.)
    
    # Produce the Distribution of Amount Betted and Payoff for each Generic Risk Profile:
    if (plot2):
        for profile in riskProfiles:
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
                [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],alphasToUse,
                betasAsFloats,[float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
                float(match[23])],[float(match[24]),float(match[25])],oddsSS=[],oddsNumGames=[])

                # "place" these bets and the computed the ROI:
                [ROI, spent, returns] = ObjectiveMetricROI(outcome, Zk, suggestedBets)
                amountBetted[profile].append(spent)
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
        # Amount Betted:
        plt.hist([amountBetted['Averse'],amountBetted['Less-Averse'],amountBetted['Neutral']], 
        color=['blue','green','red'],edgecolor='black',label=['Averse = [{}, {}, {}]'.format(riskProfiles['Averse']['20%'],
        riskProfiles['Averse']['33%'],riskProfiles['Averse']['50%']),'Less-Averse = [{}, {}, {}]'.format(riskProfiles['Less-Averse']['20%'],
        riskProfiles['Less-Averse']['33%'],riskProfiles['Less-Averse']['50%']),'Neutral  [{}, {}, {}]'.format(riskProfiles['Neutral']['20%'],
        riskProfiles['Neutral']['33%'],riskProfiles['Neutral']['50%'])],bins = 4)
        plt.legend()
        plt.xlabel('Amount Betted (as a proportion of your budget)')
        plt.ylabel('Frequency over the 25 Matches')
        if (saveFigures):
            plt.savefig(plotsFolder+'Distribution of Amount Betted 3 - All Profiles over 25 Matches')
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
        plt.xlabel('Payoff (irrespective of the amount betted)')
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

    # Save figures to:
    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'
    saveFigures = True

    # Which plots to make:
    plot1 = True
    plot2 = True

    # Which version of CVaR model are we using:
    cVaR = 1

    # Set up required data storing structures:
    ROIs = {}
    ROIs['Very Averse'] = []
    ROIs['Averse'] = []
    ROIs['Less-Averse'] = []
    allROIs = {}

    # Add the beta keys to all the required dictionarys:
    betas = ['20%','33%','50%']
    betsMade = {}
    bets = {}
    betsToPlot = {}
    totalSpent = {}
    for beta in betas:
        # Plot 1:
        allROIs[beta] = {}

        # For plot 2:
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
    betasAsFloats = [0.2, 0.33, 0.5]
    N = 30
    alphaValues = {}
    if (cVaR == 1):
        riskProfiles = {'Very Averse': {'20%': 0.5, '33%': 0.4, '50%': 0.25}, 'Averse': {'20%': 0.7, '33%': 0.6,
        '50%': 0.5}, 'Less-Averse': {'20%': 0.8, '33%': 0.7, '50%': 0.6}}
        alphaValues = {}
        for beta in betas:
            alphaValues[beta] = {}
            for profile in riskProfiles:
                if (beta == '20%'):
                    alphaValues[beta][profile] = np.linspace(riskProfiles[profile]['33%'],1.,N)
                elif (beta == '33%'):
                    alphaValues[beta][profile] = np.linspace(riskProfiles[profile]['50%'],riskProfiles[profile]['20%'],N)
                else:
                    alphaValues[beta][profile] = np.linspace(0.2,riskProfiles[profile]['33%'],N)
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

    # Compute the interpolated distributions:
    Dists = InterpolateDists(float(match[26]), float(match[27]), DB)

    # Extract the required match details:
    winner = 1
    matchScore = [float(match[10]), float(match[11])]
    setScores = ExtractSetScores(match[8])
    outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

    # Find the best bets to place:
    for profile in riskProfiles:
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
                [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],profile, alphasToUse,
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
                totalSpent[beta][profile].append(spent)
            
            # Add to the overall dictionary of ROIs and amount betted:
            allROIs[beta][profile] = ROIs[profile]
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
            axes[counter].legend(['Very Averse','Averse','Less-Averse'])
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
                        # Sum up the amount betted on this specific bet over the changing alpha values:
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
        fig.suptitle('Amount Betted on Various Bets as the Users Risk Profile Changes', fontsize = 20)

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
                # axes[counter1,counter2].legend(labels, loc = "upper left")
                counter1 += 1
            counter2 += 1

        fig.legend(labels, loc = (0.8,0.77))
        if (saveFigures):
            plt.savefig(plotsFolder+'Amount Betted 3 - All Risk Profiles')
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
    amountBetted = 0.
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
        amountBetted = 0.
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
            
            # Append to the dictionary storing the amount betted:
            amountBetted += spent
            amountReturned += returns
        
        # Compute the OverallROI for this specific risk profile:
        overallROI.append(((amountReturned - amountBetted) / amountBetted) * 100.)

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
    amountBetted = {}
    payOff = {}
    for avProfile in avRiskProfiles:
        amountBetted[avProfile] = []
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
            
            # Append to the dictionary storing the amount betted:
            amountBetted[avProfile].append(spent)
            payOff[avProfile].append(ROI)
    
    # Plot the distribution of payoffs and amount betted:
    plt.hist([amountBetted['Risk-Averse'],amountBetted['Risk-Neutral'],amountBetted['Risk-Seeking']], 
    color=['blue','green','red'],edgecolor='black',label=['Risk-Averse','Risk-Neutral','Risk-Seeking'],bins = 4)
    plt.legend()
    plt.xlabel('Amount Betted (as a proportion of your budget)')
    plt.ylabel('Frequency over the 25 Matches')
    if (saveFigures):
        plt.savefig(plotsFolder+'Distribution of Amount Betted 2 - All Profiles over 25 Matches')
        plt.clf()
    else:
        plt.show()

    # PayOffs:
    plt.hist([payOff['Risk-Averse'],payOff['Risk-Neutral'],payOff['Risk-Seeking']], 
    color=['blue','green','red'],edgecolor='black',label=['Risk-Averse','Risk-Neutral','Risk-Seeking'],bins = 4)
    plt.legend()
    plt.xlabel('Payoff (irrespective of the amount betted)')
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
    amountBetted = []
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
        
        # Append to the dictionary storing the amount betted:
        amountBetted.append(spent)    

    # Keep track of the betting options that were considered by each profile for this match:
    tol = 1e-06
    for bet in suggestedBets:
        # Initially Set to zero:
        bets[bet] = 0.
        for profile in betsMade:
            # Sum up the amount betted on this specific bet over the changing alpha values:
            bets[bet] += betsMade[profile][bet]

    # Check which ones were actually considered:
    for bet in bets:
        if (bets[bet] > tol):
            # Record these values for plotting:
            betsToPlot[bet] = []
            for profile in betsMade:
                betsToPlot[bet].append(betsMade[profile][bet])

    # Plot the amount betted on the various bets against the risk metric:
    for bet in betsToPlot:
        plt.plot(riskMetrics, betsToPlot[bet], label = bet)

    # Also plot the amount betted overall:
    plt.plot(riskMetrics, amountBetted, label = 'Total Amount Betted')

    # Set up labels and titles:
    plt.xlabel('Risk Metric of the Profile Used')
    plt.ylabel('Amount Betted')
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
    winner = 1
    matchScore = [float(match[10]), float(match[11])]
    setScores = ExtractSetScores(match[8])
    outcome = '{}-{}'.format(int(matchScore[0]),int(matchScore[1]))

    # Set up the risk parameters:
    profile = 'Risk-Seeking'
    betsConsidered = [1,1,1,0,0]
    #betas = [0.2, 0.33, 0.5]
    #alphas = [0.8, 0.6, 0.4]
    betas = [0.2]
    alphas = [0.5]

    # Run CVaR model:
    
    [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],profile, alphas,betas,
    [float(match[18]),float(match[19])],[float(match[20]),float(match[21]),float(match[22]),
    float(match[23])],[float(match[24]),float(match[25])])
    '''
    [Zk, suggestedBets] = RunCVaRModel(betsConsidered,Dists['Match Score'],profile,alphas,betas,[1.5,1.5],[2.,2.,2.,2.],[1.2, 1.2])
    '''
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
    testRegretConstraints(DB, '2018_19MatchesWithOdds.csv')

if __name__ == "__main__":
    main()