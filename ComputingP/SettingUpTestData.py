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
        colNumberLastName = 420

        # Search the database of matches:
        for match in matchData:
            # First look for last name of player A:
            if (oddsMatch[1]):
                x =10

        
def ExtractLastName(match, col):
    x = 10

def ExtractFirstName(match, col)
