 # Import the required functions:
from loopybeliefprop import choose
from AdditionalFunctions import combine_recursion
 
def TennisMatchNetwork2(P1S, P2S, P1TB, P2TB, FirstToSets, Mode):
    # Specify the names of the nodes in the Bayesian network
    if (FirstToSets == 3):
        if (Mode == 'Simple'):
            nodes=['ServerOdd','ServerEven','Set','NumGames','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11',
            'G12','TB','ServerOdd2','ServerEven2','Set2','NumGames2','S2G1','S2G2','S2G3','S2G4','S2G5','S2G6','S2G7',
            'S2G8','S2G9','S2G10','S2G11', 'S2G12','S2TB','ServerOdd3','ServerEven3','Set3','NumGames3','S3G1','S3G2',
            'S3G3','S3G4','S3G5','S3G6','S3G7','S3G8','S3G9','S3G10','S3G11','S3G12','S3TB','Match']
        else:
            nodes=['ServerOdd','ServerEven','Set','NumGames','SetScore','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11',
            'G12','TB','ServerOdd2','ServerEven2','Set2','NumGames2','SetScore2','S2G1','S2G2','S2G3','S2G4','S2G5','S2G6','S2G7',
            'S2G8','S2G9','S2G10','S2G11', 'S2G12','S2TB','ServerOdd3','ServerEven3','Set3','NumGames3','SetScore3', 'S3G1','S3G2',
            'S3G3','S3G4','S3G5','S3G6','S3G7','S3G8','S3G9','S3G10','S3G11','S3G12','S3TB','Match','TotalNumGames','AllSetScores']
    elif (FirstToSets == 5):
        if (Mode == 'Simple'):
            nodes=['ServerOdd','ServerEven','Set','NumGames','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11',
            'G12','TB','ServerOdd2','ServerEven2','Set2','NumGames2','S2G1','S2G2','S2G3','S2G4','S2G5','S2G6','S2G7',
            'S2G8','S2G9','S2G10','S2G11', 'S2G12','S2TB','ServerOdd3','ServerEven3','Set3','NumGames3', 'S3G1','S3G2',
            'S3G3','S3G4','S3G5','S3G6','S3G7','S3G8','S3G9','S3G10','S3G11','S3G12','S3TB','ServerOdd4','ServerEven4','Set4',
            'NumGames4', 'S4G1','S4G2','S4G3','S4G4','S4G5','S4G6','S4G7','S4G8','S4G9','S4G10','S4G11','S4G12','S4TB', 
            'ServerOdd5','ServerEven5','Set5','NumGames5', 'S5G1','S5G2','S5G3','S5G4','S5G5','S5G6','S5G7','S5G8','S5G9',
            'S5G10','S5G11','S5G12','S5TB','Match']     
        else: 
            nodes=['ServerOdd','ServerEven','Set','NumGames','SetScore','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11',
            'G12','TB','ServerOdd2','ServerEven2','Set2','NumGames2','SetScore2','S2G1','S2G2','S2G3','S2G4','S2G5','S2G6','S2G7',
            'S2G8','S2G9','S2G10','S2G11', 'S2G12','S2TB','ServerOdd3','ServerEven3','Set3','NumGames3','SetScore3', 'S3G1','S3G2',
            'S3G3','S3G4','S3G5','S3G6','S3G7','S3G8','S3G9','S3G10','S3G11','S3G12','S3TB','ServerOdd4','ServerEven4','Set4',
            'NumGames4','SetScore4', 'S4G1','S4G2','S4G3','S4G4','S4G5','S4G6','S4G7','S4G8','S4G9','S4G10','S4G11','S4G12','S4TB', 
            'ServerOdd5','ServerEven5','Set5','NumGames5','SetScore5', 'S5G1','S5G2','S5G3','S5G4','S5G5','S5G6','S5G7','S5G8','S5G9',
            'S5G10','S5G11','S5G12','S5TB','Match','TotalNumGames','AllSetScores'] 

    # Defining parent nodes:
    parents={}
    parents['ServerEven']=['ServerOdd']
    parents['G1']=['ServerOdd']
    parents['G2']=['ServerEven']
    parents['G3']=['ServerOdd']
    parents['G4']=['ServerEven']
    parents['G5']=['ServerOdd']
    parents['G6']=['ServerEven']
    parents['G7']=['ServerOdd']
    parents['G8']=['ServerEven']
    parents['G9']=['ServerOdd']
    parents['G10']=['ServerEven']
    parents['G11']=['ServerOdd']
    parents['G12']=['ServerEven']
    parents['TB']=['ServerOdd']
    parents['Set']=['G1', 'G2', 'G3', 'G4','G5','G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'TB']
    parents['NumGames']=['G1', 'G2', 'G3', 'G4','G5','G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'TB']

    if (Mode == 'Complex'):
        parents['SetScore']=['G1', 'G2', 'G3', 'G4','G5','G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'TB']
        parents['SetScore2']=['S2G1', 'S2G2', 'S2G3', 'S2G4','S2G5','S2G6', 'S2G7', 'S2G8', 'S2G9', 'S2G10', 'S2G11', 'S2G12', 'S2TB']
        parents['SetScore3']=['S3G1','S3G2','S3G3','S3G4','S3G5','S3G6','S3G7','S3G8','S3G9','S3G10','S3G11','S3G12','S3TB']

    parents['ServerEven2']=['ServerOdd2']
    parents['S2G1']=['ServerOdd2']
    parents['S2G2']=['ServerEven2']
    parents['S2G3']=['ServerOdd2']
    parents['S2G4']=['ServerEven2']
    parents['S2G5']=['ServerOdd2']
    parents['S2G6']=['ServerEven2']
    parents['S2G7']=['ServerOdd2']
    parents['S2G8']=['ServerEven2']
    parents['S2G9']=['ServerOdd2']
    parents['S2G10']=['ServerEven2']
    parents['S2G11']=['ServerOdd2']
    parents['S2G12']=['ServerEven2']
    parents['S2TB']=['ServerOdd2']
    parents['Set2']=['S2G1', 'S2G2', 'S2G3', 'S2G4','S2G5','S2G6', 'S2G7', 'S2G8', 'S2G9', 'S2G10', 'S2G11', 'S2G12', 'S2TB']
    parents['NumGames2']=['S2G1', 'S2G2', 'S2G3', 'S2G4','S2G5','S2G6', 'S2G7', 'S2G8', 'S2G9', 'S2G10', 'S2G11', 'S2G12', 'S2TB']
    parents['ServerEven3']=['ServerOdd3']
    parents['S3G1']=['ServerOdd3']
    parents['S3G2']=['ServerEven3']
    parents['S3G3']=['ServerOdd3']
    parents['S3G4']=['ServerEven3']
    parents['S3G5']=['ServerOdd3']
    parents['S3G6']=['ServerEven3']
    parents['S3G7']=['ServerOdd3']
    parents['S3G8']=['ServerEven3']
    parents['S3G9']=['ServerOdd3']
    parents['S3G10']=['ServerEven3']
    parents['S3G11']=['ServerOdd3']
    parents['S3G12']=['ServerEven3']
    parents['S3TB']=['ServerOdd3']
    parents['Set3']=['S3G1','S3G2','S3G3','S3G4','S3G5','S3G6','S3G7','S3G8','S3G9','S3G10','S3G11','S3G12','S3TB']
    parents['NumGames3']=['S3G1','S3G2','S3G3','S3G4','S3G5','S3G6','S3G7','S3G8','S3G9','S3G10','S3G11','S3G12','S3TB']
    
    # Set up links between sets:
    parents['ServerOdd2'] = ['ServerOdd','NumGames']
    parents['ServerOdd3'] = ['ServerOdd2','NumGames2']

    if (FirstToSets == 3):
        # Set up the links to the match nodes:
        parents['Match'] = ['Set', 'Set2', 'Set3']
        if (Mode == 'Complex'):
            parents['TotalNumGames'] = ['NumGames', 'NumGames2', 'NumGames3']
            parents['AllSetScores'] = ['SetScore', 'SetScore2', 'SetScore3']

    # If match is best of 5 sets:
    if (FirstToSets == 5):
        parents['ServerEven4']=['ServerOdd4']
        parents['S4G1']=['ServerOdd4']
        parents['S4G2']=['ServerEven4']
        parents['S4G3']=['ServerOdd4']
        parents['S4G4']=['ServerEven4']
        parents['S4G5']=['ServerOdd4']
        parents['S4G6']=['ServerEven4']
        parents['S4G7']=['ServerOdd4']
        parents['S4G8']=['ServerEven4']
        parents['S4G9']=['ServerOdd4']
        parents['S4G10']=['ServerEven4']
        parents['S4G11']=['ServerOdd4']
        parents['S4G12']=['ServerEven4']
        parents['S4TB']=['ServerOdd4']
        parents['Set4']=['S4G1','S4G2','S4G3','S4G4','S4G5','S4G6','S4G7','S4G8','S4G9','S4G10','S4G11','S4G12','S4TB']
        parents['NumGames4']=['S4G1','S4G2','S4G3','S4G4','S4G5','S4G6','S4G7','S4G8','S4G9','S4G10','S4G11','S4G12','S4TB']

        if (Mode == 'Complex'):
            parents['SetScore4']=['S4G1','S4G2','S4G3','S4G4','S4G5','S4G6','S4G7','S4G8','S4G9','S4G10','S4G11','S4G12','S4TB']
            parents['SetScore5']=['S5G1','S5G2','S5G3','S5G4','S5G5','S5G6','S5G7','S5G8','S5G9','S5G10','S5G11','S5G12','S5TB']

        parents['ServerEven5']=['ServerOdd5']
        parents['S5G1']=['ServerOdd5']
        parents['S5G2']=['ServerEven5']
        parents['S5G3']=['ServerOdd5']
        parents['S5G4']=['ServerEven5']
        parents['S5G5']=['ServerOdd5']
        parents['S5G6']=['ServerEven5']
        parents['S5G7']=['ServerOdd5']
        parents['S5G8']=['ServerEven5']
        parents['S5G9']=['ServerOdd5']
        parents['S5G10']=['ServerEven5']
        parents['S5G11']=['ServerOdd5']
        parents['S5G12']=['ServerEven5']
        parents['S5TB']=['ServerOdd5']
        parents['Set5']=['S5G1','S5G2','S5G3','S5G4','S5G5','S5G6','S5G7','S5G8','S5G9','S5G10','S5G11','S5G12','S5TB']
        parents['NumGames5']=['S5G1','S5G2','S5G3','S5G4','S5G5','S5G6','S5G7','S5G8','S5G9','S5G10','S5G11','S5G12','S5TB']

        # Set up links between sets:
        parents['ServerOdd4'] = ['ServerOdd3','NumGames3']
        parents['ServerOdd5'] = ['ServerOdd4','NumGames4']

        # Set up the links to the match nodes:
        parents['Match'] = ['Set', 'Set2', 'Set3', 'Set4', 'Set5']

        if (Mode == 'Complex'):
            parents['TotalNumGames'] = ['NumGames', 'NumGames2', 'NumGames3', 'NumGames4', 'NumGames5']
            parents['AllSetScores'] = ['SetScore', 'SetScore2', 'SetScore3', 'SetScore4', 'SetScore5']

    # Set up the possible outcomes for each node:
    outcomes={}
    outcomes['ServerOdd']=["P1Serves","P2Serves"]
    outcomes['ServerEven']=["P1Serves","P2Serves"]
    outcomes['G1']=[1,2]
    outcomes['G2']=[1,2]
    outcomes['G3']=[1,2]
    outcomes['G4']=[1,2]
    outcomes['G5']=[1,2]
    outcomes['G6']=[1,2]
    outcomes['G7']=[1,2]
    outcomes['G8']=[1,2]
    outcomes['G9']=[1,2]
    outcomes['G10']=[1,2]
    outcomes['G11']=[1,2]
    outcomes['G12']=[1,2]
    outcomes['TB']=[1,2]
    outcomes['Set']=[1,2]
    outcomes['NumGames']=[6,7,8,9,10,12,13]

    if (Mode == 'Complex'):
        outcomes['SetScore']=["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]
        outcomes['SetScore2']=["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]
        outcomes['SetScore3']=["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]

    outcomes['ServerOdd2']=["P1Serves","P2Serves"]
    outcomes['ServerEven2']=["P1Serves","P2Serves"]
    outcomes['S2G1']=[1,2]
    outcomes['S2G2']=[1,2]
    outcomes['S2G3']=[1,2]
    outcomes['S2G4']=[1,2]
    outcomes['S2G5']=[1,2]
    outcomes['S2G6']=[1,2]
    outcomes['S2G7']=[1,2]
    outcomes['S2G8']=[1,2]
    outcomes['S2G9']=[1,2]
    outcomes['S2G10']=[1,2]
    outcomes['S2G11']=[1,2]
    outcomes['S2G12']=[1,2]
    outcomes['S2TB']=[1,2]
    outcomes['Set2']=[1,2]
    outcomes['NumGames2']=[6,7,8,9,10,12,13]
    outcomes['ServerOdd3']=["P1Serves","P2Serves"]
    outcomes['ServerEven3']=["P1Serves","P2Serves"]
    outcomes['S3G1']=[1,2]
    outcomes['S3G2']=[1,2]
    outcomes['S3G3']=[1,2]
    outcomes['S3G4']=[1,2]
    outcomes['S3G5']=[1,2]
    outcomes['S3G6']=[1,2]
    outcomes['S3G7']=[1,2]
    outcomes['S3G8']=[1,2]
    outcomes['S3G9']=[1,2]
    outcomes['S3G10']=[1,2]
    outcomes['S3G11']=[1,2]
    outcomes['S3G12']=[1,2]
    outcomes['S3TB']=[1,2]
    outcomes['Set3']=[1,2]
    outcomes['NumGames3']=[6,7,8,9,10,12,13]

    # outcomes for match nodes:
    outcomes['Match'] = [1,2]

    if (Mode == 'Complex'):
        outcomes['TotalNumGames'] = [list(range(18, 66))]
        outcomes['AllSetScores'] = ["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]

    if (FirstToSets == 5):
        outcomes['ServerOdd4']=["P1Serves","P2Serves"]
        outcomes['ServerEven4']=["P1Serves","P2Serves"]
        outcomes['S4G1']=[1,2]
        outcomes['S4G2']=[1,2]
        outcomes['S4G3']=[1,2]
        outcomes['S4G4']=[1,2]
        outcomes['S4G5']=[1,2]
        outcomes['S4G6']=[1,2]
        outcomes['S4G7']=[1,2]
        outcomes['S4G8']=[1,2]
        outcomes['S4G9']=[1,2]
        outcomes['S4G10']=[1,2]
        outcomes['S4G11']=[1,2]
        outcomes['S4G12']=[1,2]
        outcomes['S4TB']=[1,2]
        outcomes['Set4']=[1,2]
        outcomes['NumGames4']=[6,7,8,9,10,12,13]

        if (Mode == 'Complex'):
            outcomes['SetScore4']=["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]
            outcomes['SetScore5']=["6-0","6-1","6-2","6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]

        outcomes['ServerOdd5']=["P1Serves","P2Serves"]
        outcomes['ServerEven5']=["P1Serves","P2Serves"]
        outcomes['S5G1']=[1,2]
        outcomes['S5G2']=[1,2]
        outcomes['S5G3']=[1,2]
        outcomes['S5G4']=[1,2]
        outcomes['S5G5']=[1,2]
        outcomes['S5G6']=[1,2]
        outcomes['S5G7']=[1,2]
        outcomes['S5G8']=[1,2]
        outcomes['S5G9']=[1,2]
        outcomes['S5G10']=[1,2]
        outcomes['S5G11']=[1,2]
        outcomes['S5G12']=[1,2]
        outcomes['S5TB']=[1,2]
        outcomes['Set5']=[1,2]
        outcomes['NumGames5']=[6,7,8,9,10,12,13]

    # Compute the probability of winning a game on serve from the on-serve point probabilities:
    P1G = pow(P1S, 2) / (pow(P1S, 2) + pow((1-P1S), 2))
    P2G = pow(P2S, 2) / (pow(P2S, 2) + pow((1-P2S), 2))

    # Equal chance of each player serving the first game: (Can update if the toss has been done)
    dist={}
    dist['ServerOdd'] = [0.5,0.5]
    dist['ServerEven'] = {}
    dist['ServerEven']["P1Serves"] = [0.,1.]
    dist['ServerEven']["P2Serves"] = [1.,0.]
    dist['ServerEven2'] = {}
    dist['ServerEven2']["P1Serves"] = [0.,1.]
    dist['ServerEven2']["P2Serves"] = [1.,0.]
    dist['ServerEven3'] = {}
    dist['ServerEven3']["P1Serves"] = [0.,1.]
    dist['ServerEven3']["P2Serves"] = [1.,0.]
    dist['ServerOdd2'] = {}
    dist['ServerOdd3'] = {}
    if (FirstToSets == 5):
        dist['ServerEven4'] = {}
        dist['ServerEven4']["P1Serves"] = [0.,1.]
        dist['ServerEven4']["P2Serves"] = [1.,0.]
        dist['ServerEven5'] = {}
        dist['ServerEven5']["P1Serves"] = [0.,1.]
        dist['ServerEven5']["P2Serves"] = [1.,0.]
        dist['ServerOdd4'] = {}
        dist['ServerOdd5'] = {}

    for i in outcomes["NumGames"]:
        if (i % 2 == 0):
            dist['ServerOdd2']["P1Serves",i] = [1., 0.]
            dist['ServerOdd2']["P2Serves",i] = [0., 1.]
            dist['ServerOdd3']["P1Serves",i] = [1., 0.]
            dist['ServerOdd3']["P2Serves",i] = [0., 1.]
            if (FirstToSets == 5):
                dist['ServerOdd4']["P1Serves",i] = [1., 0.]
                dist['ServerOdd4']["P2Serves",i] = [0., 1.]
                dist['ServerOdd5']["P1Serves",i] = [1., 0.]
                dist['ServerOdd5']["P2Serves",i] = [0., 1.]
        else:
            dist['ServerOdd2']["P1Serves",i] = [0., 1.]
            dist['ServerOdd2']["P2Serves",i] = [1., 0.]
            dist['ServerOdd3']["P1Serves",i] = [0., 1.]
            dist['ServerOdd3']["P2Serves",i] = [1., 0.]
            if (FirstToSets == 5):
                dist['ServerOdd4']["P1Serves",i] = [0., 1.]
                dist['ServerOdd4']["P2Serves",i] = [1., 0.]
                dist['ServerOdd5']["P1Serves",i] = [0., 1.]
                dist['ServerOdd5']["P2Serves",i] = [1., 0.]

    # Set up dictionaries for each game:
    dist['G1']={}
    dist['G2']={}
    dist['G3']={}
    dist['G4']={}
    dist['G5']={}
    dist['G6']={}
    dist['G7']={}
    dist['G8']={}
    dist['G9']={}
    dist['G10']={}
    dist['G11']={}
    dist['G12']={}
    dist['TB']={}
    dist['S2G1']={}
    dist['S2G2']={}
    dist['S2G3']={}
    dist['S2G4']={}
    dist['S2G5']={}
    dist['S2G6']={}
    dist['S2G7']={}
    dist['S2G8']={}
    dist['S2G9']={}
    dist['S2G10']={}
    dist['S2G11']={}
    dist['S2G12']={}
    dist['S2TB']={}
    dist['S3G1']={}
    dist['S3G2']={}
    dist['S3G3']={}
    dist['S3G4']={}
    dist['S3G5']={}
    dist['S3G6']={}
    dist['S3G7']={}
    dist['S3G8']={}
    dist['S3G9']={}
    dist['S3G10']={}
    dist['S3G11']={}
    dist['S3G12']={}
    dist['S3TB']={}
    if (FirstToSets == 5):
        dist['S4G1']={}
        dist['S4G2']={}
        dist['S4G3']={}
        dist['S4G4']={}
        dist['S4G5']={}
        dist['S4G6']={}
        dist['S4G7']={}
        dist['S4G8']={}
        dist['S4G9']={}
        dist['S4G10']={}
        dist['S4G11']={}
        dist['S4G12']={}
        dist['S4TB']={}
        dist['S5G1']={}
        dist['S5G2']={}
        dist['S5G3']={}
        dist['S5G4']={}
        dist['S5G5']={}
        dist['S5G6']={}
        dist['S5G7']={}
        dist['S5G8']={}
        dist['S5G9']={}
        dist['S5G10']={}
        dist['S5G11']={}
        dist['S5G12']={}
        dist['S5TB']={}       

    # Define the probabilities for each game, given the server:
    # Player 1 serving:
    dist['G1']["P1Serves"]=[P1G,1.-P1G]
    dist['G2']["P1Serves"]=[P1G,1.-P1G]
    dist['G3']["P1Serves"]=[P1G,1.-P1G]
    dist['G4']["P1Serves"]=[P1G,1.-P1G]
    dist['G5']["P1Serves"]=[P1G,1.-P1G]
    dist['G6']["P1Serves"]=[P1G,1.-P1G]
    dist['G7']["P1Serves"]=[P1G,1.-P1G]
    dist['G8']["P1Serves"]=[P1G,1.-P1G]
    dist['G9']["P1Serves"]=[P1G,1.-P1G]
    dist['G10']["P1Serves"]=[P1G,1.-P1G]
    dist['G11']["P1Serves"]=[P1G,1.-P1G]
    dist['G12']["P1Serves"]=[P1G,1.-P1G]
    dist['TB']["P1Serves"]=[P1TB,1.-P1TB]

    # Player 2 serving:
    dist['G1']["P2Serves"]=[1.-P2G,P2G]
    dist['G2']["P2Serves"]=[1.-P2G,P2G]
    dist['G3']["P2Serves"]=[1.-P2G,P2G]
    dist['G4']["P2Serves"]=[1.-P2G,P2G]
    dist['G5']["P2Serves"]=[1.-P2G,P2G]
    dist['G6']["P2Serves"]=[1.-P2G,P2G]
    dist['G7']["P2Serves"]=[1.-P2G,P2G]
    dist['G8']["P2Serves"]=[1.-P2G,P2G]
    dist['G9']["P2Serves"]=[1.-P2G,P2G]
    dist['G10']["P2Serves"]=[1.-P2G,P2G]
    dist['G11']["P2Serves"]=[1.-P2G,P2G]
    dist['G12']["P2Serves"]=[1.-P2G,P2G]
    dist['TB']["P2Serves"]=[1.-P2TB,P2TB]

    # Player 1 serving:
    dist['S2G1']["P1Serves"]=[P1G,1.-P1G]
    dist['S2G2']["P1Serves"]=[P1G,1.-P1G]
    dist['S2G3']["P1Serves"]=[P1G,1.-P1G]
    dist['S2G4']["P1Serves"]=[P1G,1.-P1G]
    dist['S2G5']["P1Serves"]=[P1G,1.-P1G]
    dist['S2G6']["P1Serves"]=[P1G,1.-P1G]
    dist['S2G7']["P1Serves"]=[P1G,1.-P1G]
    dist['S2G8']["P1Serves"]=[P1G,1.-P1G]
    dist['S2G9']["P1Serves"]=[P1G,1.-P1G]
    dist['S2G10']["P1Serves"]=[P1G,1.-P1G]
    dist['S2G11']["P1Serves"]=[P1G,1.-P1G]
    dist['S2G12']["P1Serves"]=[P1G,1.-P1G]
    dist['S2TB']["P1Serves"]=[P1TB,1.-P1TB]

    # Player 2 serving:
    dist['S2G1']["P2Serves"]=[1.-P2G,P2G]
    dist['S2G2']["P2Serves"]=[1.-P2G,P2G]
    dist['S2G3']["P2Serves"]=[1.-P2G,P2G]
    dist['S2G4']["P2Serves"]=[1.-P2G,P2G]
    dist['S2G5']["P2Serves"]=[1.-P2G,P2G]
    dist['S2G6']["P2Serves"]=[1.-P2G,P2G]
    dist['S2G7']["P2Serves"]=[1.-P2G,P2G]
    dist['S2G8']["P2Serves"]=[1.-P2G,P2G]
    dist['S2G9']["P2Serves"]=[1.-P2G,P2G]
    dist['S2G10']["P2Serves"]=[1.-P2G,P2G]
    dist['S2G11']["P2Serves"]=[1.-P2G,P2G]
    dist['S2G12']["P2Serves"]=[1.-P2G,P2G]
    dist['S2TB']["P2Serves"]=[1.-P2TB,P2TB]

    # Player 1 serving:
    dist['S3G1']["P1Serves"]=[P1G,1.-P1G]
    dist['S3G2']["P1Serves"]=[P1G,1.-P1G]
    dist['S3G3']["P1Serves"]=[P1G,1.-P1G]
    dist['S3G4']["P1Serves"]=[P1G,1.-P1G]
    dist['S3G5']["P1Serves"]=[P1G,1.-P1G]
    dist['S3G6']["P1Serves"]=[P1G,1.-P1G]
    dist['S3G7']["P1Serves"]=[P1G,1.-P1G]
    dist['S3G8']["P1Serves"]=[P1G,1.-P1G]
    dist['S3G9']["P1Serves"]=[P1G,1.-P1G]
    dist['S3G10']["P1Serves"]=[P1G,1.-P1G]
    dist['S3G11']["P1Serves"]=[P1G,1.-P1G]
    dist['S3G12']["P1Serves"]=[P1G,1.-P1G]
    dist['S3TB']["P1Serves"]=[P1TB,1.-P1TB]

    # Player 2 serving:
    dist['S3G1']["P2Serves"]=[1.-P2G,P2G]
    dist['S3G2']["P2Serves"]=[1.-P2G,P2G]
    dist['S3G3']["P2Serves"]=[1.-P2G,P2G]
    dist['S3G4']["P2Serves"]=[1.-P2G,P2G]
    dist['S3G5']["P2Serves"]=[1.-P2G,P2G]
    dist['S3G6']["P2Serves"]=[1.-P2G,P2G]
    dist['S3G7']["P2Serves"]=[1.-P2G,P2G]
    dist['S3G8']["P2Serves"]=[1.-P2G,P2G]
    dist['S3G9']["P2Serves"]=[1.-P2G,P2G]
    dist['S3G10']["P2Serves"]=[1.-P2G,P2G]
    dist['S3G11']["P2Serves"]=[1.-P2G,P2G]
    dist['S3G12']["P2Serves"]=[1.-P2G,P2G]
    dist['S3TB']["P2Serves"]=[1.-P2TB,P2TB]

    if (FirstToSets == 5):
        # Player 1 serving:
        dist['S4G1']["P1Serves"]=[P1G,1.-P1G]
        dist['S4G2']["P1Serves"]=[P1G,1.-P1G]
        dist['S4G3']["P1Serves"]=[P1G,1.-P1G]
        dist['S4G4']["P1Serves"]=[P1G,1.-P1G]
        dist['S4G5']["P1Serves"]=[P1G,1.-P1G]
        dist['S4G6']["P1Serves"]=[P1G,1.-P1G]
        dist['S4G7']["P1Serves"]=[P1G,1.-P1G]
        dist['S4G8']["P1Serves"]=[P1G,1.-P1G]
        dist['S4G9']["P1Serves"]=[P1G,1.-P1G]
        dist['S4G10']["P1Serves"]=[P1G,1.-P1G]
        dist['S4G11']["P1Serves"]=[P1G,1.-P1G]
        dist['S4G12']["P1Serves"]=[P1G,1.-P1G]
        dist['S4TB']["P1Serves"]=[P1TB,1.-P1TB]

        # Player 2 serving:
        dist['S4G1']["P2Serves"]=[1.-P2G,P2G]
        dist['S4G2']["P2Serves"]=[1.-P2G,P2G]
        dist['S4G3']["P2Serves"]=[1.-P2G,P2G]
        dist['S4G4']["P2Serves"]=[1.-P2G,P2G]
        dist['S4G5']["P2Serves"]=[1.-P2G,P2G]
        dist['S4G6']["P2Serves"]=[1.-P2G,P2G]
        dist['S4G7']["P2Serves"]=[1.-P2G,P2G]
        dist['S4G8']["P2Serves"]=[1.-P2G,P2G]
        dist['S4G9']["P2Serves"]=[1.-P2G,P2G]
        dist['S4G10']["P2Serves"]=[1.-P2G,P2G]
        dist['S4G11']["P2Serves"]=[1.-P2G,P2G]
        dist['S4G12']["P2Serves"]=[1.-P2G,P2G]
        dist['S4TB']["P2Serves"]=[1.-P2TB,P2TB]

        # Player 1 serving:
        dist['S5G1']["P1Serves"]=[P1G,1.-P1G]
        dist['S5G2']["P1Serves"]=[P1G,1.-P1G]
        dist['S5G3']["P1Serves"]=[P1G,1.-P1G]
        dist['S5G4']["P1Serves"]=[P1G,1.-P1G]
        dist['S5G5']["P1Serves"]=[P1G,1.-P1G]
        dist['S5G6']["P1Serves"]=[P1G,1.-P1G]
        dist['S5G7']["P1Serves"]=[P1G,1.-P1G]
        dist['S5G8']["P1Serves"]=[P1G,1.-P1G]
        dist['S5G9']["P1Serves"]=[P1G,1.-P1G]
        dist['S5G10']["P1Serves"]=[P1G,1.-P1G]
        dist['S5G11']["P1Serves"]=[P1G,1.-P1G]
        dist['S5G12']["P1Serves"]=[P1G,1.-P1G]
        dist['S5TB']["P1Serves"]=[P1TB,1.-P1TB]

        # Player 2 serving:
        dist['S5G1']["P2Serves"]=[1.-P2G,P2G]
        dist['S5G2']["P2Serves"]=[1.-P2G,P2G]
        dist['S5G3']["P2Serves"]=[1.-P2G,P2G]
        dist['S5G4']["P2Serves"]=[1.-P2G,P2G]
        dist['S5G5']["P2Serves"]=[1.-P2G,P2G]
        dist['S5G6']["P2Serves"]=[1.-P2G,P2G]
        dist['S5G7']["P2Serves"]=[1.-P2G,P2G]
        dist['S5G8']["P2Serves"]=[1.-P2G,P2G]
        dist['S5G9']["P2Serves"]=[1.-P2G,P2G]
        dist['S5G10']["P2Serves"]=[1.-P2G,P2G]
        dist['S5G11']["P2Serves"]=[1.-P2G,P2G]
        dist['S5G12']["P2Serves"]=[1.-P2G,P2G]
        dist['S5TB']["P2Serves"]=[1.-P2TB,P2TB]

    # Define the possible outcomes of the set, given a sequence of outcomes from all 12 games and the TB:
    dist['Set']={}
    dist['NumGames']={}
    dist['Set'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1.,0.]
    dist['NumGames'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0.]
    dist['Set2']={}
    dist['NumGames2']={}
    dist['Set2'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1.,0.]
    dist['NumGames2'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0.]
    dist['Set3']={}
    dist['NumGames3']={}
    dist['Set3'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1.,0.]
    dist['NumGames3'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0.]

    if (Mode == 'Complex'):
        dist['SetScore']={}
        dist['SetScore'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
        dist['SetScore2']={}
        dist['SetScore2'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
        dist['SetScore3']={}
        dist['SetScore3'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]

    if (FirstToSets == 5):
        dist['Set4']={}
        dist['NumGames4']={}
        dist['Set4'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1.,0.]
        dist['NumGames4'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0.]
        dist['Set5']={}
        dist['NumGames5']={}
        dist['Set5'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1.,0.]
        dist['NumGames5'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0.]

        if (Mode == 'Complex'):
            dist['SetScore4']={}
            dist['SetScore4'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
            dist['SetScore5']={}
            dist['SetScore5'][1,1,1,1,1,1,1,1,1,1,1,1,1] = [1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]

    # Possible Set Scores and Number of Games:
    SetScores = [[6,0],[6,1],[6,2],[6,3],[6,4],[7,5],[7,6],[0,6],[1,6],[2,6],[3,6],[4,6],[5,7],[6,7]]
    NumberOfGames = [6,7,8,9,10,12,13]

    for i in range(1,14):
        Seqs = combine_recursion(13,i)

        for j in Seqs:
            # Reset Sequences and distributions:
            InitialSeq = [1,1,1,1,1,1,1,1,1,1,1,1,1]
            SetScoresDist = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
            NumGamesDist = [0., 0., 0., 0., 0., 0., 0.]

            # Place the '2's in each possible combination:
            for games in j:
                InitialSeq[games-1] = 2

            # Assign the correct winner:
            Sequence = tuple(InitialSeq)

            # Set Outcome:

            # Case 1: (i (Player 2 wins) < 6)
            if (i < 6):
                # Player 1 wins:
                dist['Set'][Sequence] = [1.,0.]
                dist['Set2'][Sequence] = [1.,0.]
                dist['Set3'][Sequence] = [1.,0.]
                if (FirstToSets == 5):
                    dist['Set4'][Sequence] = [1.,0.]
                    dist['Set5'][Sequence] = [1.,0.]
      
            # Case 2: (i > 7):
            elif (i > 7):
                # Player 2 wins:
                dist['Set'][Sequence] = [0.,1.]
                dist['Set2'][Sequence] = [0.,1.]
                dist['Set3'][Sequence] = [0.,1.]
                if (FirstToSets == 5):
                    dist['Set4'][Sequence] = [0.,1.]
                    dist['Set5'][Sequence] = [0.,1.]

            # Case 3: (i = 6 or 7)
            else:
                # Check the first 12 games to see if a tie-breaker was required:
                First12 = Sequence[:-1]
                P2Wins = First12.count(2)
                if (P2Wins > 5):
                    # Player 2 wins:
                    dist['Set'][Sequence] = [0.,1.]
                    dist['Set2'][Sequence] = [0.,1.]
                    dist['Set3'][Sequence] = [0.,1.]
                    if (FirstToSets == 5):
                        dist['Set4'][Sequence] = [0.,1.]
                        dist['Set5'][Sequence] = [0.,1.]
                else:
                    # Player 1 wins:
                    dist['Set'][Sequence] = [1.,0.]
                    dist['Set2'][Sequence] = [1.,0.]
                    dist['Set3'][Sequence] = [1.,0.]
                    if (FirstToSets == 5):
                        dist['Set4'][Sequence] = [1.,0.]
                        dist['Set5'][Sequence] = [1.,0.]
                
                # Check if a tie-breaker was needed:
                if (P2Wins == 6):
                    # Check who won the TB:
                    if (Sequence[-1] == 2):
                        # Player 2 won the TB and therefore the set too:
                        dist['Set'][Sequence] = [0.,1.]
                        dist['Set2'][Sequence] = [0.,1.]
                        dist['Set3'][Sequence] = [0.,1.]
                        if (FirstToSets == 5):
                            dist['Set4'][Sequence] = [0.,1.]
                            dist['Set5'][Sequence] = [0.,1.]
                    else:
                        # Player 1 wins:
                        dist['Set'][Sequence] = [1.,0.] 
                        dist['Set2'][Sequence] = [1.,0.]
                        dist['Set3'][Sequence] = [1.,0.]
                        if (FirstToSets == 5):
                            dist['Set4'][Sequence] = [1.,0.]
                            dist['Set5'][Sequence] = [1.,0.] 

            # Compute the set score and number of games in the set:
            Game = 0
            iGames = 0
            jGames = 0
            # Case 1: Set did not go beyond 10 games
            if (i <= 4 or i > 8):
                while (iGames < 6 and jGames < 6):
                    if (InitialSeq[Game] == 1):
                        iGames = iGames + 1
                    else:
                        jGames = jGames + 1
                    Game = Game + 1
                
                # Compute score and number of games:
                SetScore = [iGames, jGames]
                NumGames = sum(SetScore)

                # Find the index corresponding to this outcome:
                IndexSS = SetScores.index(SetScore)
                IndexNG = NumberOfGames.index(NumGames)

                # Assign the correct outcome to the respective leaf node:
                SetScoresDist[IndexSS] = 1.
                NumGamesDist[IndexNG] = 1.
                dist['NumGames'][Sequence] = NumGamesDist
                dist['NumGames2'][Sequence] = NumGamesDist
                dist['NumGames3'][Sequence] = NumGamesDist
                if (Mode == 'Complex'):
                    dist['SetScore'][Sequence] = SetScoresDist
                    dist['SetScore2'][Sequence] = SetScoresDist
                    dist['SetScore3'][Sequence] = SetScoresDist 

                if (FirstToSets == 5):
                    dist['NumGames4'][Sequence] = NumGamesDist
                    dist['NumGames5'][Sequence] = NumGamesDist
                    if (Mode == 'Complex'):
                        dist['SetScore4'][Sequence] = SetScoresDist
                        dist['SetScore5'][Sequence] = SetScoresDist

            else: # Case 2:
                # Check if the game went beyond 10 games:
                First10Games = InitialSeq[0:10]
                if (First10Games.count(1) == 5):
                    # Set went to 10+ games
                    while (iGames < 7 and jGames < 7):
                        if (InitialSeq[Game] == 1):
                            iGames = iGames + 1
                        else:
                            jGames = jGames + 1
                        Game = Game + 1

                    # Compute score and number of games:
                    SetScore = [iGames, jGames]
                    NumGames = sum(SetScore)

                    # Find the index corresponding to this outcome:
                    IndexSS = SetScores.index(SetScore)
                    IndexNG = NumberOfGames.index(NumGames)

                    # Assign the correct outcome to the respective leaf node:
                    SetScoresDist[IndexSS] = 1.
                    NumGamesDist[IndexNG] = 1.
                    dist['NumGames'][Sequence] = NumGamesDist 
                    dist['NumGames2'][Sequence] = NumGamesDist
                    dist['NumGames3'][Sequence] = NumGamesDist
                    if (Mode == 'Complex'):
                        dist['SetScore'][Sequence] = SetScoresDist
                        dist['SetScore2'][Sequence] = SetScoresDist
                        dist['SetScore3'][Sequence] = SetScoresDist

                    if (FirstToSets == 5):
                        dist['NumGames4'][Sequence] = NumGamesDist
                        dist['NumGames5'][Sequence] = NumGamesDist 
                        if (Mode == 'Complex'):
                            dist['SetScore4'][Sequence] = SetScoresDist
                            dist['SetScore5'][Sequence] = SetScoresDist 

                else: 
                    # Set went to 10- games
                    while (iGames < 6 and jGames < 6):
                        if (InitialSeq[Game] == 1):
                            iGames = iGames + 1
                        else:
                            jGames = jGames + 1
                        Game = Game + 1

                    # Compute score and number of games:
                    SetScore = [iGames, jGames]
                    NumGames = sum(SetScore)

                    # Find the index corresponding to this outcome:
                    IndexSS = SetScores.index(SetScore)
                    IndexNG = NumberOfGames.index(NumGames)

                    # Assign the correct outcome to the respective leaf node:
                    SetScoresDist[IndexSS] = 1.
                    NumGamesDist[IndexNG] = 1.
                    dist['NumGames'][Sequence] = NumGamesDist 
                    dist['NumGames2'][Sequence] = NumGamesDist
                    dist['NumGames3'][Sequence] = NumGamesDist
                    if (Mode == 'Complex'):
                        dist['SetScore'][Sequence] = SetScoresDist
                        dist['SetScore2'][Sequence] = SetScoresDist
                        dist['SetScore3'][Sequence] = SetScoresDist

                    if (FirstToSets == 5):
                        dist['NumGames4'][Sequence] = NumGamesDist
                        dist['NumGames5'][Sequence] = NumGamesDist
                        if (Mode == 'Complex'):
                            dist['SetScore4'][Sequence] = SetScoresDist
                            dist['SetScore5'][Sequence] = SetScoresDist
    
    # Match node distributions:
    dist['Match']={}
    if (FirstToSets == 3):
        dist['Match'][1,1,1] = [1.,0.]
        dist['Match'][1,1,2] = [1.,0.]
        dist['Match'][1,2,1] = [1.,0.]
        dist['Match'][1,2,2] = [0.,1.]
        dist['Match'][2,1,1] = [1.,0.]
        dist['Match'][2,1,2] = [0.,1.]
        dist['Match'][2,2,1] = [0.,1.]
        dist['Match'][2,2,2] = [0.,1.]
    else:
        # Number of matches = 5:  
        dist['Match'][1,1,1,1,1] = [1.,0.]     
        for i in range(1,6):
            Seqs = combine_recursion(5,i)

            for j in Seqs:
                # Reset Sequences and distributions:
                InitialSeq = [1,1,1,1,1]

                # Place the '2's in each possible combination:
                for games in j:
                    InitialSeq[games-1] = 2

                # Assign the correct winner:
                Sequence = tuple(InitialSeq)

                # Set Outcome:
                if (i < 3):
                    dist['Match'][Sequence] = [1.,0.]
                else:
                    dist['Match'][Sequence] = [0.,1.]
    
    # All Set Score distributions: 
    if (Mode == 'Complex'):
        dist['AllSetScores'] = {}
        SetScores = ["6-0","6-1","6-2", "6-3","6-4","7-5","7-6","0-6","1-6","2-6","3-6","4-6","5-7","6-7"]
        for Set in outcomes['SetScore']:
                for Set2 in outcomes['SetScore']:
                        for Set3 in outcomes['SetScore']:
                            if (FirstToSets == 3):
                                SetScoresDist = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
                                # Find the index of each set score:
                                indices = [SetScores.index(Set), SetScores.index(Set2), SetScores.index(Set3)]
                                # Update distribution:
                                for ind in indices:
                                    SetScoresDist[ind] = SetScoresDist[ind] + 1./3.                         
                                dist['AllSetScores'][Set, Set2, Set3] = SetScoresDist
                            elif (FirstToSets == 5):
                                for Set4 in outcomes['SetScore']:
                                    for Set5 in outcomes['SetScore']:
                                        SetScoresDist = [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
                                        # Find the index of each set score:
                                        indices = [SetScores.index(Set), SetScores.index(Set2), SetScores.index(Set3), SetScores.index(Set4), SetScores.index(Set5)]
                                        # Update distribution:
                                        for ind in indices:
                                            SetScoresDist[ind] = SetScoresDist[ind] + 1./2.                        
                                        dist['AllSetScores'][Set, Set2, Set3, Set4, Set5] = SetScoresDist

        # Total Number of Games distributions:
        dist['TotalNumGames'] = {}
        for Games in outcomes['NumGames']:
                for Games2 in outcomes['NumGames']:
                        for Games3 in outcomes['NumGames']:
                            if (FirstToSets == 3):
                                NumberOfGamesdist = [0.] * len(outcomes['TotalNumGames'][0])
                                TotalGames = Games + Games2 + Games3
                                index = outcomes['TotalNumGames'][0].index(TotalGames)
                                # Update distribution:
                                NumberOfGamesdist[index] = 1.                         
                                dist['TotalNumGames'][Games, Games2, Games3] = NumberOfGamesdist
                            elif (FirstToSets == 5):
                                for Games4 in outcomes['NumGames']:
                                    for Games5 in outcomes['NumGames']:
                                        NumberOfGamesdist = [0.] * len(outcomes['TotalNumGames'])
                                        TotalGames = Games + Games2 + Games3 + Games4 + Games5
                                        index = outcomes['TotalNumGames'][0].index(TotalGames)
                                        # Update distribution:
                                        NumberOfGamesdist[index] = 1.                         
                                        dist['TotalNumGames'][Games, Games2, Games3, Games4, Games5] = NumberOfGamesdist
              
    # Set up initial information:
    info={}
    for i in nodes:
        info[i] = choose(outcomes[i], "NotSure")
    
    return(nodes, dist, parents, outcomes, info)



