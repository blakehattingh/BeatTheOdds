import psycopg2 as psy
import random
import pandas as pd
import numpy as np

#years = list of years as integers eg. (2012,2014)
def getTestMatchData(years):
    conn = psy.connect('dbname=tcb user=postgres password=12qwaszx host=localhost')
    cursor = conn.cursor()
    clayMatchesByYears = []
    hardMatchesByYears = []
    grassMatchesByYears = []
    for year in years:
        upperB = year + 1
        queryClay = f"""select * from tcb.match m join tcb.match_stats s on 
            m.match_id = s.match_id where m.date >= '{year}-01-01' AND m.date < '{upperB}-01-01' AND m.best_of = 3 AND m.outcome is NULL AND m.surface = 'C'"""
        queryHard = f"""select * from tcb.match m join tcb.match_stats s on 
        m.match_id = s.match_id where m.date >= '{year}-01-01' AND m.date < '{upperB}-01-01' AND m.best_of = 3 AND m.outcome is NULL AND m.surface = 'H'"""
        queryGrass = f"""select * from tcb.match m join tcb.match_stats s on 
        m.match_id = s.match_id where m.date >= '{year}-01-01' AND m.date < '{upperB}-01-01' AND m.best_of = 3 AND m.outcome is NULL AND m.surface = 'G'"""
        cursor.execute(queryClay)
        clayMatchesByYears.append(cursor.fetchall())
        cursor.execute(queryHard)
        hardMatchesByYears.append(cursor.fetchall())
        cursor.execute(queryGrass)
        grassMatchesByYears.append(cursor.fetchall())
    sampledMatchesByYearClay = getRandomSamples(clayMatchesByYears,50)
    sampledMatchesByYearHard = getRandomSamples(hardMatchesByYears,50)
    sampledMatchesByYearGrass = getRandomSamples(grassMatchesByYears,50)

    sampledMatchesByYears = []
    for i in range(len(years)):
        matches = sampledMatchesByYearClay[i] + sampledMatchesByYearHard[i] + sampledMatchesByYearGrass[i]
        sampledMatchesByYears.append(matches)
    #print(sampledMatchesByYears)
    #print(len(sampledMatchesByYears))
    #print(len(sampledMatchesByYears[0]))
    return sampledMatchesByYears

def getSpecificMatches(matchIds):
    matches = []
    conn = psy.connect('dbname=tcb user=postgres password=12qwaszx host=localhost')
    cursor = conn.cursor()
    for matchId in matchIds:
        getMatchByIdQuery = f""" select * from tcb.match m join tcb.match_stats s on m.match_id = s.match_id where m.match_id = {matchId}"""
        cursor.execute(getMatchByIdQuery)
        matches.append(cursor.fetchall())
    return matches

def getCallibrationSet(startYear, endYear):
    endYear = endYear+1
    conn = psy.connect('dbname=tcb user=postgres password=12qwaszx host=localhost')
    cursor = conn.cursor()
    matchesBetweenYears = []
    query = f"""select * from tcb.match m join tcb.match_stats s on 
            m.match_id = s.match_id where m.date >= '{startYear}-01-01' AND m.date < '{endYear}-01-01' AND m.best_of = 3 AND m.outcome is NULL"""
    cursor.execute(query)
    matchesBetweenYears.append(cursor.fetchall())
    sampledMatchesBetweenYears = getRandomSamplesNotByYears(matchesBetweenYears, 400)
    threeHundredSet = sampledMatchesBetweenYears[:300]
    hundredSet = sampledMatchesBetweenYears[300:]
    dfThreeHun = pd.DataFrame(threeHundredSet)
    dfHun = pd.DataFrame(hundredSet)
    dfThreeHun.to_csv('threeHundredCalMatches.csv')
    dfHun.to_csv('hundredCalMatches.csv')


def getRandomSamplesNotByYears(matchesA, num):
    sampledMatches = []
    for matches in matchesA:
        length = len(matches)
        indices = random.sample(range(0,length-1),num)
        sampledMatches = []
        for index in indices:
            sampledMatches.append(matches[index])
    return sampledMatches

def getRandomSamples(matchesByYears, numMatches):
    sampledMatchesByYears = []

    for matches in matchesByYears:
        length = len(matches)
        indices = random.sample(range(0,length-1),numMatches)
        sampledMatches = []
        for index in indices:
            sampledMatches.append(matches[index])
        sampledMatchesByYears.append(sampledMatches)
    return sampledMatchesByYears
              
def getPotentialMatches(afterDate, beforeDate):
    # This function gets all matches between the two dates specified.
    conn = psy.connect('dbname=tcb user=postgres password=12qwaszx host=localhost')
    cursor = conn.cursor()
    potentialMatches = []

    # SQL Command:
    queryMatches = f"""select * from tcb.match m join tcb.match_stats s on m.match_id = s.match_id where m.date >= 
    '{afterDate}' AND m.date < '{beforeDate}' AND m.best_of = 3 AND m.outcome is NULL"""
    cursor.execute(queryMatches)
    #potentialMatches.append(cursor.fetchall())
    potentialMatches = cursor.fetchall()
        
    return potentialMatches

def main():
    years = [2012,2014,2016,2018,2019]
    testYears = [2018, 2019]
    #getTestMatchData(years)
    getCallibrationSet(2015,2020)


if __name__ == "__main__":
    main()