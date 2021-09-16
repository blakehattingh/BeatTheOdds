import numpy as np
import os
import csv

BLAKES_DIRECTORY = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\'

def CreateTestDataSet(oddsCSVFiles, matchData):

    # Set up a list of lists to store the odds for each match:
    oddsData = []

    # Read in Odds CSV Files:
    for file in oddsCSVFiles:
        # Create the directory for file:
        fileName = os.path.join(BLAKES_DIRECTORY, file)

        # Open it, read in contents and append it to the list structure:
        with open(fileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    oddsData.append(row)
                    line_count += 1
            csv_file.close()

    # For each match with odds, try and find the corresponding match:
    for oddsMatch in oddsData:
        # Find column of Last Name In Match Data

        # Extract Player A's names:
        [firstNames, lastNames, NumberOfNames] = ExtractNames(oddsMatch, 1)

        # Search the database of matches:
        potentialMatches = []
        
        # Find all matches that player A played in:
        playerAMatches = []
        
        # Iterate through all possible combination of names:
        for last in lastNames:
            for first in firstNames:
                playerAMatches = FindAllMatchesWithThisPlayer(matchData, last, first)

            for i in range(NumberOfNames-1):
                if (lastNames[i] == match['Player As last name']):
                    potentialMatches.append(match)
                elif (lastNames[i] == match['Player Bs last name']):
                    potentialMatches.append(match)

                #

                    
                x =10

        
def ExtractNames(match, col):
    # Get the full name of the player of interest:
    stringName = match[col].lower()

    # Get rid of additional whitespaces in the name:
    stringName = ' '.join(stringName.split())

    # Split the string up by whitespace:
    names = stringName.split(' ')

    # Remove the last element as it is the abbreviation:
    names.pop()

    # Check how many names there are:
    numNames = len(names)
    if (numNames == 2):
        # First and Last name:
        firstName = names[0]
        lastName = names[1]
    elif(numNames == 3):
        # Either double first name or double last name:
        firstName = [[names[0]],[names[0]+ ' '+names[1]]]
        lastName = [[names[2]],[names[1]+ ' '+names[2]]]
    elif(numNames == 4):
        # Try all options:
        firstName = [[names[0]],[names[0]+' '+names[1]],[names[0]+' '+names[1]+' '+names[2]]]
        lastName = [[names[3]],[names[2]+' '+names[3]],[names[1]+' '+names[2]+' '+names[3]]]
    else:
        # Too many fucking names:
        print('Too many names to handle!')
    
    return [firstName, lastName, numNames]

def FindAllMatchesWithThisPlayer(matchData, lastName, firstName):
    # This function finds all matches that the specified player played in.
    # Inputs:
    # matchData: List of lists, each list is an individual match
    # lastName & firstName: The name of the player of interest

    playerMatches = []
    for match in matchData:
        if (match['Last Name Column'] == lastName):
            if (match['First name Col'] == firstName):
                playerMatches.append(match)
    
    return playerMatches