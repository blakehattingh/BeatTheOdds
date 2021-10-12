import numpy as np
import matplotlib.pyplot as plt
import csv
import os

from numpy.lib.npyio import save

def ReadInFromCSV(fileName, header):
    data = []
    # Get location of file:
    THIS_FOLDER = os.path.abspath('CSVFiles')
    fileName = os.path.join(THIS_FOLDER, fileName)

    # Read in CSV file:
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if (header):     
                if line_count == 0:
                    line_count += 1
                else:
                    data.append(row)
                    line_count += 1
            else:
                data.append(row)
                line_count += 1
        csv_file.close()
    return data

def ReadInFromDict(fileName, keys):
    data= []
    # Get location of file:
    #THIS_FOLDER = os.path.abspath('\\CSVFiles')
    fileName = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\beliefprop\\ProjectDevelopmentCode\\CSVFiles\\ObjectiveValuesForCalibratedParametersRound2.csv'

    # Read in from the dictionary stored in a CSV file:
    with open(fileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            # check if row is empty line:
            if (row != []):
                innerDict = {}
                counter = 0
                for key in keys:
                    innerDict[key] = row[counter]
                    counter += 1
                data.append(innerDict)
        csv_file.close()
    return data

def PlotCalibrationRound1Results():
    # Read in the data from 'ObjectiveValuesForCalibratedParametersRound2.csv':
    file = 'ObjectiveValuesForCalibratedParametersRound2.csv'
    keys = ['Equation', 'Parameters', 'Objective Value']
    data = ReadInFromDict(file, keys)

    # Set up the figure:
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])

    # Get data in required format:
    equation1Values = []
    equation2Values = []
    equation3Values = []
    equation1Params = []
    equation2Params = []
    equation3Params = []
    for iter in data:
        if (iter['Equation'] == '1'):
            equation1Values.append(-1 * float(iter['Objective Value']))
            equation1Params.append(iter['Parameters'])
        elif (iter['Equation'] == '2'):
            equation2Values.append(-1 * float(iter['Objective Value']))
            equation2Params.append(iter['Parameters'])
        elif (iter['Equation'] == '3'):         
            equation3Values.append(-1 * float(iter['Objective Value']))
            equation3Params.append(iter['Parameters'])

    # Split data by what calibration set was used: (1st, 2nd... 6th)
    firstSet = [equation1Values[0], equation2Values[0], equation3Values[0]]
    secondSet = [equation1Values[1], equation2Values[1], equation3Values[1]]
    thirdSet = [equation1Values[2], equation2Values[2], equation3Values[2]]
    fourthSet = [equation1Values[3], equation2Values[3], equation3Values[3]]
    fifthSet = [equation1Values[4], equation2Values[4], equation3Values[4]]
    sixthSet = [equation1Values[5], equation2Values[5], equation3Values[5]]

    # Get locations of the groups (equations):
    locations = np.arange(3)
    width = 0.1

    # Plot the data:
    set1 = ax.bar(locations-2.5*width,firstSet, width, color='slateblue')
    set2 = ax.bar(locations-1.5*width,secondSet, width, color='navy')
    set3 = ax.bar(locations-0.5*width,thirdSet, width, color='cornflowerblue')
    set4 = ax.bar(locations+0.5*width,fourthSet, width, color='lightsteelblue')
    set5 = ax.bar(locations+1.5*width,fifthSet, width, color='lightsteelblue')
    set6 = ax.bar(locations+2.5*width,sixthSet, width, color='lightsteelblue')

    # Set up axis:
    ax.legend(labels = ['Best','2nd Best','Third Best','Fourth Best','Fifth Best','Sixth Best'], fontsize=20)
    ax.set_ylabel('Objective Value', fontsize=20)
    ax.set_xlabel('Equation Used', fontsize=20)
    ax.set_title('Test Performance for the Best 6 Calibrated Parameters', fontsize=20)
    ax.set_xticks(locations + width / 2)
    ax.set_xticklabels(('Equation 1','Equation 2','Equation 3'), fontsize=20)

    plt.show()
    # Plot the data:
    '''
    ax.bar(X[0:6], equation1Values, color = 'b')
    ax.bar(X[6:12], equation2Values, color = 'r')
    ax.bar(X[12:19], equation3Values, color = 'g')
    ax.set_title('Objective Values for the Best Calibrated Values')
    ax.set_ylabel('Objective Value - Match Stats')
    ax.legend(labels = ['Equation 1', 'Equation 2', 'Equation 3'])
    plt.show()
    '''

def plotS1InsamplePerformance(saveFig):
    # This method plots the in-sample performance of each of the equations. 
    # It plots the objective values against the calibrated parameters for the 6 best parameters of each equation.
    # The data values have been taken from the file 'FinalCalibratedParametersAllEquations.csv'
    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'

    # Hard-coded Data:
    alg1Obj = [1.705454545,1.698181818,1.694545455,1.690909091,1.687272727,1.687272727]
    alg2Obj = [1.854545455,1.84,1.825454545,1.818181818,1.807272727,1.8]
    alg3Obj = [1.883636364,1.858181818,1.847272727,1.836363636,1.832727273,1.825454545]

    plot1st =[alg1Obj[0],alg2Obj[0],alg3Obj[0]]
    plot2st =[alg1Obj[1],alg2Obj[1],alg3Obj[1]]
    plot3st =[alg1Obj[2],alg2Obj[2],alg3Obj[2]]
    plot4st =[alg1Obj[3],alg2Obj[3],alg3Obj[3]]
    plot5st =[alg1Obj[4],alg2Obj[4],alg3Obj[4]]
    plot6st =[alg1Obj[5],alg2Obj[5],alg3Obj[5]]

    alg1Params = ('[6.33,0.79,0.73]','[12,0.52,0.41]','[9.45,0.75,0.25]','[12,0.79,0.25]',
                '[8.8,0.25,0.50]','[12,0.82,0.65]')
    alg2Params = ['[6.3,0.25,0.75]','[6.33,0.26,0.24]','[6.48,0.25,0.49]',
                '[9.55,0.26,0.75]','[12,0.26,0.75]','[9.57,0.26,0.47]']
    alg3Params = ['[6.86,0.25,0.50,0.48]','[10.08,0.25,0.72,0.53]',
                '[6.53,0.27,0.75,0.67]','[10.10,0.25,0.50,0.49]',
                '[12,0.26,0.75,0.53]','[10.91,0.28,0.57,0.26]']

    pos  = list(range(6))
    width = 0.8

    #fig, ax = plt.subplots(figsize=(5,10))
    fig, ax = plt.subplots(1, 3,sharey=True, figsize = [12,8])
    fig.suptitle('Stage 1 In-Sample Performace', fontsize=14)
    plt.subplots_adjust(bottom=0.224)
    #plt.bar(pos,plot1st,width,alpha=0.5, color ='slateblue')
    #plt.bar(pos+width,plot2st,width,alpha=0.5, color ='navy')
    ax[0].bar(pos,alg1Obj,width,alpha=0.5, color ='mediumseagreen')
    ax[0].set_ylim(1.6, 1.9)
    ax[0].set_xticks(range(6))
    ax[0].tick_params(labelrotation=70)
    ax[0].set_xticklabels(alg1Params)
    ax[0].set_title('Equation 1', fontsize=12)
    ax[0].set_ylabel('Objective Function Value', fontsize=11)

    ax[1].bar(pos,alg2Obj,width,alpha=0.5, color ='royalblue')
    ax[1].set_xticks(range(6))
    ax[1].tick_params(labelrotation=70)
    ax[1].set_xticklabels(alg2Params)
    ax[1].set_title('Equation 2', fontsize=12)
    ax[1].set_xlabel('Calibrated Parameters', fontsize=11)

    ax[2].bar(pos,alg3Obj,width,alpha=0.5, color ='firebrick')
    ax[2].set_xticks(range(6))
    ax[2].tick_params(labelrotation=70)
    ax[2].set_xticklabels(alg3Params)
    ax[2].set_title('Equation 3', fontsize=12)

    if (saveFig):
        plt.savefig(plotsFolder+'Calibration Stage 1- InSample Performance')
        plt.clf()
    else:
        plt.show()

def plotAlgorithmProgress(fileName, saveFig):
    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'
    currentBestValues = []
    currentValues = []

    with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0 
            skipLines = [0,1,2,3,4,5,6,7,8,9]
            for row in csv_reader:
                if line_count in skipLines:
                    line_count += 1
                elif(line_count == 10):
                    currentBestValues = row
                    line_count += 1
                elif(line_count == 11):
                    currentValues = row
                    line_count+=1
            csv_file.close()

    # Convert to floats:
    for i in range(len(currentBestValues)):
        currentBestValues[i] = float(currentBestValues[i])
        currentValues[i] = float(currentValues[i])

    # Plot the values:
    iterations = list(range(1,len(currentBestValues)+1))
    plt.plot(iterations, currentBestValues , color = 'red', linestyle = '--', label = "Best Objective Value")
    plt.plot(iterations, currentValues, color = 'royalblue', label = "Current Objective Value")
    
    # Set up the labels:
    plt.title('Search Algorithm Progress', fontsize = 14)
    plt.xlabel('Iteration Number', fontsize = 11)
    plt.ylabel('Objective Function Value', fontsize = 11)
    plt.legend()

    if (saveFig):
        plt.savefig(plotsFolder+'Calibration Stage 1 - Algorthim Progress')
        plt.clf()
    else:
        plt.show()

def plotS2OutOfSamplePerformance(saveFig):
    # This method plots the out-of-sample performance of each of the equations. 
    # It plots the objective values against the calibrated parameters for the 6 best parameters of each equation.
    # The data values have been taken from the file 'ObjectiveValyesForCalibratedParametersRound2.csv'

    plotsFolder = 'C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\ModelPlots\\'

    # Hard-coded Data:
    alg1Obj = [1.818181818,1.863636364,1.988095238,1.897727273,1.852272727,1.875]
    alg2Obj = [1.964705882,2.090909091,1.880952381,1.916666667,2,1.97752809]
    alg3Obj = [2.023255814,1.966292135,2.011764706,2.045454545,1.904761905,1.869047619]

    alg1Params = ('(4.02, 0.75, 0.76)','(4.2, 0.68, 0.53)','(2.1, 0.48, 0.8)',
                    '(3.98, 0.26, 0.74)','(4.06, 0.26, 0.48)','(4.03, 0.51, 0.76)')
    alg2Params = ['(2.21, 0.47, 0.76)','(4.13, 0.24, 0.78)','(2.11, 0.78, 0.78)',
                '(2.11, 0.26, 0.74)','(6.3, 0.25, 0.75)','(6.33, 0.26, 0.24)']
    alg3Params = ['(2.23, 0.51, 0.76, 0.46)','(6.86, 0.25, 0.5, 0.49)','(2.22, 0.78, 0.78, 0.75)',
                '(4.13, 0.24, 0.81, 0.5)','(2.16, 0.26, 0.74, 0.5)','(2.14, 0.81, 0.74, 0.51)']

    pos  = list(range(6))
    width = 0.8

    #fig, ax = plt.subplots(figsize=(5,10))
    fig, ax = plt.subplots(1, 3,sharey=True, figsize = [12, 8])
    fig.suptitle('Stage 2 Out-Of-Sample Performance', fontsize=14)
    plt.subplots_adjust(bottom=0.224)
    #plt.bar(pos,plot1st,width,alpha=0.5, color ='slateblue')
    #plt.bar(pos+width,plot2st,width,alpha=0.5, color ='navy')
    ax[0].bar(pos,alg1Obj,width,alpha=0.5, color ='mediumseagreen')
    ax[0].set_ylim(1.6, 2.1)
    ax[0].set_xticks(range(6))
    ax[0].tick_params(labelrotation=70)
    ax[0].set_xticklabels(alg1Params)
    ax[0].set_title('Equation 1', fontsize=12)
    ax[0].set_ylabel('Objective Value', fontsize=11)

    ax[1].bar(pos,alg2Obj,width,alpha=0.5, color ='royalblue')
    ax[1].set_xticks(range(6))
    ax[1].tick_params(labelrotation=70)
    ax[1].set_xticklabels(alg2Params)
    ax[1].set_title('Equation 2', fontsize=12)
    ax[1].set_xlabel('Calibrated Parameters', fontsize=11)

    ax[2].bar(pos,alg3Obj,width,alpha=0.5, color ='firebrick')
    ax[2].set_xticks(range(6))
    ax[2].tick_params(labelrotation=70)
    ax[2].set_xticklabels(alg3Params)
    ax[2].set_title('Equation 3', fontsize=12)

    if (saveFig):
        plt.savefig(plotsFolder+'Calibration Stage 1 - OutOfSample Performances')
        plt.clf()
    else:
        plt.show()

def main():
    # Plot 1 - Search algorithm progress:
    plotAlgorithmProgress('C:\\Users\\campb\\OneDrive\\Documents\\University_ENGSCI\\4th Year\\ResearchProject\\beliefprop\\ProjectDevelopmentCode\\CSVFiles\\CalibratedPlottingDataRound2.csv', True)
    
    # Plot 2 - In-Sample Performance:
    plotS1InsamplePerformance(True)

    # Plot 3 - Out-of-Sample Performance:
    plotS2OutOfSamplePerformance(True)
    
if __name__ == "__main__":
    main()