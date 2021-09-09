import psycopg2 as psy
import random

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
              



def main():
    years = [2012,2014,2016,2018,2019]
    testYears = [2018, 2019]
    getTestMatchData(years)


if __name__ == "__main__":
    main()