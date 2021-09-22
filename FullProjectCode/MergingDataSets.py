import os
import csv
from datetime import datetime, timedelta
from time import strftime
from HelperFunctions import try_parsing_date
from DataExtractionFromDB import getPotentialMatches, getIdForName

def CreateTestDataSet(oddsCSVFiles, margin):
    # Set up a list of lists to store the odds for each match:
    oddsData = []

    # Read in Odds CSV Files:
    for file in oddsCSVFiles:
        # Create the directory for file:
        oddsData.append(ReadInOddsData(file))

    # Create a list to store the combination of odds and match stats:
    fullTestSet = []

    # For each match with odds, try and find the corresponding match:
    for tournament in oddsData:
        print(len(tournament))
        numCollected = 0
        #reset tournament
        tournamentId = False
        for oddsMatch in tournament:
            # Create a list to store potential matches:
            finalPotentialMatches = []
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
                    #get ID for player
                    playerAId = getIdForName(first, last)
                    if(playerAId):
                        playerAMatchesForThisName = FindAllMatchesWithThisPlayer(potentialMatches, playerAId)
                        for i in playerAMatchesForThisName:
                            playerAMatches.append(i)


            # Search player A's matches for ones where player B played in:
            if (len(playerAMatches) > 0 ):
                for last in lastNamesB:
                    for first in firstNamesB:
                        #get ID for player
                        playerBId = getIdForName(first, last)
                        if(playerBId):
                            playerBMatchesForThisName = FindAllMatchesWithThisPlayer(playerAMatches, playerBId)
                            for i in playerBMatchesForThisName:
                                finalPotentialMatches.append(i)

            # Check how many matches are in the final list:
            if (len(finalPotentialMatches) == 1):
                # Append the odds data to the match
                fullMatch = AppendOdds(finalPotentialMatches[0], oddsMatch, 8)
                fullTestSet.append(fullMatch)
                numCollected+=1
                if(not tournamentId):
                    tournamentId = fullMatch[1]
                #print(fullTestSet)
            elif (len(finalPotentialMatches) > 1):
                matchId = finalPotentialMatches[0][0]
                counter = 0
                for i in finalPotentialMatches:
                    if(matchId == i[0]):
                        counter += 1
                if(counter == len(finalPotentialMatches)):
                    fullMatch = AppendOdds(finalPotentialMatches[0], oddsMatch, 8)
                    fullTestSet.append(fullMatch)
                    numCollected+= 1
                    if(not tournamentId):
                        tournamentId = fullMatch[1]
                    #print(fullTestSet)
                else:
                    tournamentCounter = 0
                    tempMatch =[]
                    for i in finalPotentialMatches:
                        if(i[1] == tournamentId):
                            tournamentCounter += 1
                            tempMatch = i
                    if (tournamentCounter == 1):
                        fullMatch = AppendOdds(tempMatch, oddsMatch, 8)
                        fullTestSet.append(fullMatch)
                        numCollected+= 1
                    else:    
                        print("Found multiple potential matches")
                        print(lastNamesA, lastNamesB)
                        print(finalPotentialMatches)
            else:
                print("no matches found")
        print(numCollected)

    return fullTestSet

def ReadInOddsData(file):
    # Get the directory for CSV files:
    fileName = os.path.join('\\CSVFiles', file)

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
    stringName = match[col]

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
        firstName = [names[0]]
        lastName = [names[1]]
    elif(numNames == 3):
        # Either double first name or double last name:
        firstName = [names[0],names[0]+ ' '+names[1]]
        lastName = [names[2],names[1]+ ' '+names[2]]
    elif(numNames == 4):
        # Try all options:
        firstName = [names[0],names[0]+' '+names[1],names[0]+' '+names[1]+' '+names[2]]
        lastName = [names[3],names[2]+' '+names[3],names[1]+' '+names[2]+' '+names[3]]
    else:
        # Too many fucking names:
        print('Too many names to handle!')
    
    return [firstName, lastName, numNames]

def FindAllMatchesWithThisPlayer(matchData, playerID):
    # This function finds all matches that the specified player played in.
    # Inputs:
    # matchData: List of lists, each list is an individual match
    # playerID: The ID of the player of interest

    playerMatches = []
    for match in matchData:
        if (match[8] == playerID):
            playerMatches.append(match)
        elif (match[18] == playerID):
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
        match = list(match)
        match.append(odds)

    return match

def WriteToCSV(testSet, file):
    # Write the test data to a CSV file:
    fileName = os.path.join('\\CSVFiles', file)
    with open(fileName, mode = 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in testSet:
            writer.writerow(row)
        csv_file.close()
