import psycopg2 as psy
import random
import pandas as pd
import numpy as np

def getSPWData(matchDetails, startOfDataCollection):
    # INPUTS: matchDetails = Keys P1FirstInitial, P1LastName, Date (%Y-%m-%d). age = int in years
    # OUTPUTS: matches between P1 & P2, P1 and common opponents, P2 and common opponents, common opponents IDs
    conn = psy.connect('dbname=tcb user=postgres password=12qwaszx host=localhost')
    cursor = conn.cursor()
    #p1ID,p2ID = getIds(matchDetails, cursor)
    p1ID = matchDetails[8]
    p2ID = matchDetails[18]
    p1vP2 = getP1vP2(startOfDataCollection,cursor,p1ID,p2ID, matchDetails[3])
    p1vCO = getPlayerVsCO(startOfDataCollection,cursor,p1ID,p2ID,matchDetails[3])
    p2vCO = getPlayerVsCO(startOfDataCollection,cursor,p2ID,p1ID,matchDetails[3])
    COIds = getCOs(p1vCO,p1ID,p2ID)
    return p1vP2,p1vCO,p2vCO,COIds

def getIds(matchDetails, cursor):
    P1FirstInit = matchDetails['P1FirstName']
    P1LastName = matchDetails['P1LastName']
    P2FirstInit = matchDetails['P2FirstName']
    P2LastName = matchDetails['P2LastName']
    queryP1 = "SELECT player_id FROM tcb.player WHERE UPPER(first_name) LIKE UPPER('"+P1FirstInit+"%') AND UPPER(last_name) = UPPER('"+P1LastName+"')"
    cursor.execute(queryP1)
    p1ID = cursor.fetchall()[0][0]
    queryP2 = "SELECT player_id FROM tcb.player WHERE UPPER(first_name) LIKE UPPER('"+P2FirstInit+"%') AND UPPER(last_name) = UPPER('"+P2LastName+"')"
    cursor.execute(queryP2)
    p2ID = cursor.fetchall()[0][0]
    return p1ID,p2ID

def getIdForName(firstName, lastName):
    conn = psy.connect('dbname=tcb user=postgres password=12qwaszx host=localhost')
    cursor = conn.cursor()
    query = "SELECT player_id FROM tcb.player WHERE UPPER(first_name) LIKE UPPER('"+firstName+"%') AND UPPER(last_name) = UPPER('"+lastName+"')"
    cursor.execute(query)
    response = cursor.fetchall()
    if (response == []):
        return False
    else:    
        id = response[0][0]
        return id

def getP1vP2(startOfDataCollection,cursor,p1ID,p2ID, dateOfTestMatch):
    
    query = f"select * from tcb.match m join tcb.match_stats s on \
        m.match_id = s.match_id where (m.date > '{startOfDataCollection}' AND m.date < '{dateOfTestMatch}') AND ((m.winner_id = {p1ID} OR m.winner_id = {p2ID}) AND (m.loser_id = {p1ID} OR m.loser_id = {p2ID})) AND m.outcome is NULL"
    cursor.execute(query)
    p1vP2Matches = cursor.fetchall()
    return p1vP2Matches

def getPlayerVsCO(startOfDataCollection,cursor,p1ID,p2ID, dateOfTestMatch):
    query = f'''select *
    from tcb.match k join tcb.match_stats s on 
    k.match_id = s.match_id
    where (k.date > '{startOfDataCollection}' AND k.date < '{dateOfTestMatch}') AND k.outcome is NULL AND winner_id = {p1ID} AND loser_id in ((select player_id
    from tcb.player 
    WHERE player_id in (SELECT loser_id from tcb.match as m Where 
							 ((m.winner_id = {p1ID}) 
							  AND NOT ((m.loser_id = {p2ID}) ) AND m.has_stats = 'true' AND m.outcome is NULL AND (m.date > '{startOfDataCollection}' AND m.date < '{dateOfTestMatch}')))
    union select player_id
    from tcb.player
    WHERE player_id in (SELECT winner_id from tcb.match as m Where 
							 ((m.loser_id = {p1ID}) 
							  AND NOT ((m.winner_id = {p2ID}) )AND m.has_stats = 'true' AND m.outcome is NULL AND (m.date > '{startOfDataCollection}' AND m.date < '{dateOfTestMatch}'))))
							  
    intersect 

    (select player_id
    from tcb.player
    WHERE player_id in (SELECT loser_id from tcb.match as m Where 
                                ((m.winner_id = {p2ID} ) 
                                AND NOT ( m.loser_id = {p1ID})AND m.has_stats = 'true' AND m.outcome is NULL AND (m.date > '{startOfDataCollection}' AND m.date < '{dateOfTestMatch}')))
            union select player_id
            from tcb.player
            where player_id in (SELECT winner_id from tcb.match as m Where 
                                ((m.loser_id = {p2ID} ) 
                                AND NOT ( m.winner_id = {p1ID})AND m.has_stats = 'true' AND m.outcome is NULL AND (m.date > '{startOfDataCollection}' AND m.date < '{dateOfTestMatch}')))))
                                
    union select * 
    from tcb.match k join tcb.match_stats s on 
    k.match_id = s.match_id
    where (k.date > '{startOfDataCollection}' AND k.date < '{dateOfTestMatch}') AND k.outcome is NULL AND loser_id = {p1ID} AND winner_id in ((select player_id
    from tcb.player
    WHERE player_id in (SELECT loser_id from tcb.match as m Where 
                                ((m.winner_id = {p1ID}) 
                                AND NOT ((m.loser_id = {p2ID}) )AND m.has_stats = 'true' AND m.outcome is NULL AND (m.date > '{startOfDataCollection}' AND m.date < '{dateOfTestMatch}')))
    union select player_id
    from tcb.player
    WHERE player_id in (SELECT winner_id from tcb.match as m Where 
                                ((m.loser_id = {p1ID}) 
                                AND NOT ((m.winner_id = {p2ID}) )AND m.has_stats = 'true' AND m.outcome is NULL AND (m.date > '{startOfDataCollection}' AND m.date < '{dateOfTestMatch}'))))
                                
    intersect 

    (select player_id
    from tcb.player
    WHERE player_id in (SELECT loser_id from tcb.match as m Where 
                                ((m.winner_id = {p2ID} ) 
                                AND NOT ( m.loser_id = {p1ID})AND m.has_stats = 'true' AND m.outcome is NULL AND (m.date > '{startOfDataCollection}' AND m.date < '{dateOfTestMatch}')))
            union select player_id
            from tcb.player
            where player_id in (SELECT winner_id from tcb.match as m Where 
                                ((m.loser_id = {p2ID} ) 
                                AND NOT ( m.winner_id = {p1ID})AND m.has_stats = 'true' AND m.outcome is NULL AND (m.date > '{startOfDataCollection}' AND m.date < '{dateOfTestMatch}')))))'''
    cursor.execute(query)
    playerVsCO = cursor.fetchall()
    return playerVsCO

def getCOs(p1vCO,p1ID,p2ID):
    commonOpsIDs = []
    for match in p1vCO:
        if((match[8] != p1ID) & (match[8] != p2ID) & (match[8] not in commonOpsIDs)):
            commonOpsIDs.append(match[8])
        if((match[18] != p1ID) & (match[18] != p2ID) & (match[18] not in commonOpsIDs)):
            commonOpsIDs.append(match[18])
    return commonOpsIDs

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