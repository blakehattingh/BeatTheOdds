import numpy as np
import matplotlib.pyplot as plt
import csv
import os

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
    THIS_FOLDER = os.path.abspath('CSVFiles')
    fileName = os.path.join(THIS_FOLDER, fileName)

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

def main():
    # Plot the calibration results:
    PlotCalibrationRound1Results()

if __name__ == "__main__":
    main()
