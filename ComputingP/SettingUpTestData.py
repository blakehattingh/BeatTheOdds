from time import time
import numpy as np
from datetime import datetime, timedelta
import os, sys
import csv
from CalculatingP import try_parsing_date

# Add required folders to the system path:
currentPath = os.path.abspath(os.getcwd())

# Data Extraction Files:
sys.path.insert(0, currentPath + '\\BeatTheOdds\\DataExtraction')
#sys.path.insert(0, currentPath + '\DataExtraction')
from TestSetCollector import *

BLAKES_DIRECTORY = 'C:\\Uni\\4thYearProject\\repo\\BeatTheOdds\\CSVFiles\\'

def CreateTestDataSet(oddsCSVFiles, margin):
    # Set up a list of lists to store the odds for each match:
    oddsData = []

    # Read in Odds CSV Files:
    for file in oddsCSVFiles:
        # Create the directory for file:
        oddsData.append(ReadInOddsData(file))

    # Create a list to store the combination of odds and match stats:
    fullTestSet = []

    # Create a list to store potential matches:
    finalPotentialMatches = []

    # For each match with odds, try and find the corresponding match:
    for oddsMatch in oddsData:
        # Extract the margin dates:
        [afterDate, beforeDate] = ExtractDates(oddsMatch, margin)

        # Extract all matches played a within a week either side of the match of interest:
        potentialMatches = getPotentialMatches(afterDate, beforeDate)

        # Extract Player A's and B's names:
        [firstNamesA, lastNamesA, NumberOfNamesA] = ExtractNames(oddsMatch, 1)
        [firstNamesB, lastNamesB, NumberOfNamesB] = ExtractNames(oddsMatch, 2)

        # Search the potential matches for ones where player A played in:
        playerAMatches = []

        # Iterate through all possible combination of names:
        for last in lastNamesA:
            for first in firstNamesA:
                playerAMatches.append(FindAllMatchesWithThisPlayer(potentialMatches, last, first))

        # Search player A's matches for ones where player B played in:
        for last in lastNamesB:
            for first in firstNamesB:
                finalPotentialMatches.append(FindAllMatchesWithThisPlayer(playerAMatches, last, first))

        # Check how many matches are in the final list:
        if (len(finalPotentialMatches) == 1):
            # Append the odds data to the match:
            foundMatch = finalPotentialMatches[0].append(oddsMatch[3:11])
            fullTestSet = AppendOdds(foundMatch, oddsMatch, 8)
        else:
            print("Found multiple potential matches")
            print(finalPotentialMatches)

    return fullTestSet

def ReadInOddsData(file):
    fileName = os.path.join(BLAKES_DIRECTORY, file)
    #THIS_FOLDER = os.path.abspath('CSVFiles')
    #fileName = os.path.join(THIS_FOLDER, file)

    oddsData = []
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
    return oddsData

def ExtractDates(match, margin):
    # Extract the date string:
    [date, type] = try_parsing_date(match[0])
    
    # Compute the margin either side of the match date:
    beforeDate = date + timedelta(days = margin)
    afterDate = date - timedelta(days = margin)

    # Convert it to the required format for the database:
    beforeDate = beforeDate.strftime('%Y-%m-%d')
    afterDate = afterDate.strftime('%Y-%m-%d')

    return [afterDate, beforeDate]

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

def AppendOdds(match, oddsMatch, numOdds):
    # This function takes 2 corresponding lists, one with the match data and one with the odds and appends them
    # to each other.

    # Iterate through the odds:
    for i in range(numOdds):
        oddsString = oddsMatch[3 + i]
        
        # Extract the actual odd value:
        odds = oddsString.split()

        # If it is the only value, which it should be, convert it to a floating point:
        if (len(odds) == 1):
            odds = float(odds[0])
        else:
            raise ValueError('More than one value found')
        
        # Append it the match:
        match.append(odds)

    return match

def main():
    files = ['ATPHalle.csv']
    margin = 7

    '''
    # Read in the data:
    THIS_FOLDER = os.path.abspath('CSVFiles')
    fileName = os.path.join(THIS_FOLDER, files[0])
    oddsData = ReadInOddsData(fileName)

    # Test Append Odds function:
    print(AppendOdds([],oddsData[0], 8))
    '''
    
    # Run the function:
    testSet = CreateTestDataSet(files, margin)

    print(testSet)

if __name__ == "__main__":
    main()