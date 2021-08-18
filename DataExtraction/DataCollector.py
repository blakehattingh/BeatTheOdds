import psycopg2 as psy

#INPUTS: matchDetails = Keys P1FirstInitial, P1LastName, Date (%Y-%m-%d). age = int in years
#OUTPUTS: matches between P1 & P2, P1 and common opponents, P2 and common opponents, common opponents IDs
def getSPWData(matchDetails, startOfDataCollection):
    conn = psy.connect('dbname=tcb user=postgres password=12qwaszx host=localhost')
    cursor = conn.cursor()
    #p1ID,p2ID = getIds(matchDetails, cursor)
    p1ID = matchDetails[8]
    p2ID = matchDetails[18]
    p1vP2 = getP1vP2(startOfDataCollection,cursor,p1ID,p2ID, matchDetails[3])
    p1vCO = getPlayerVsCO(startOfDataCollection,cursor,p1ID,p2ID,matchDetails[3])
    p2vCO = getPlayerVsCO(startOfDataCollection,cursor,p2ID,p1ID,matchDetails[3])
    COIds = getCOs(p1vCO,p1ID,p2ID)
    print(len(p1vP2))
    print(len(p1vCO))
    print(len(p2vCO))
    print(len(COIds))
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

def getP1vP2(startOfDataCollection,cursor,p1ID,p2ID, dateOfTestMatch):
    
    query = f"select * from tcb.match m join tcb.match_stats s on \
        m.match_id = s.match_id where (m.date > '{startOfDataCollection}' AND m.date < '{dateOfTestMatch}') AND ((m.winner_id = {p1ID} OR m.winner_id = {p2ID}) AND (m.loser_id = {p1ID} OR m.loser_id = {p2ID}))"
    cursor.execute(query)
    p1vP2Matches = cursor.fetchall()
    return p1vP2Matches

def getPlayerVsCO(startOfDataCollection,cursor,p1ID,p2ID, dateOfTestMatch):
    query = f'''select *
    from tcb.match k join tcb.match_stats s on 
    k.match_id = s.match_id
    where (k.date > '{startOfDataCollection}' AND k.date < '{dateOfTestMatch}') AND winner_id = {p1ID} AND loser_id in ((select player_id
    from tcb.player
    WHERE player_id in (SELECT loser_id from tcb.match as m Where 
							 ((m.winner_id = {p1ID}) 
							  AND NOT ((m.loser_id = {p2ID}) )))
    union select player_id
    from tcb.player
    WHERE player_id in (SELECT winner_id from tcb.match as m Where 
							 ((m.loser_id = {p1ID}) 
							  AND NOT ((m.winner_id = {p2ID}) ))))
							  
    intersect 

    (select player_id
    from tcb.player
    WHERE player_id in (SELECT loser_id from tcb.match as m Where 
                                ((m.winner_id = {p2ID} ) 
                                AND NOT ( m.loser_id = {p1ID})))
            union select player_id
            from tcb.player
            where player_id in (SELECT winner_id from tcb.match as m Where 
                                ((m.loser_id = {p2ID} ) 
                                AND NOT ( m.winner_id = {p1ID})))))
                                
    union select * 
    from tcb.match k join tcb.match_stats s on 
    k.match_id = s.match_id
    where (k.date > '{startOfDataCollection}' AND k.date < '{dateOfTestMatch}') AND loser_id = {p1ID} AND winner_id in ((select player_id
    from tcb.player
    WHERE player_id in (SELECT loser_id from tcb.match as m Where 
                                ((m.winner_id = {p1ID}) 
                                AND NOT ((m.loser_id = {p2ID}) )))
    union select player_id
    from tcb.player
    WHERE player_id in (SELECT winner_id from tcb.match as m Where 
                                ((m.loser_id = {p1ID}) 
                                AND NOT ((m.winner_id = {p2ID}) ))))
                                
    intersect 

    (select player_id
    from tcb.player
    WHERE player_id in (SELECT loser_id from tcb.match as m Where 
                                ((m.winner_id = {p2ID} ) 
                                AND NOT ( m.loser_id = {p1ID})))
            union select player_id
            from tcb.player
            where player_id in (SELECT winner_id from tcb.match as m Where 
                                ((m.loser_id = {p2ID} ) 
                                AND NOT ( m.winner_id = {p1ID})))))'''
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

def main():
    #matchDetails = {'P1FirstInitial': 'r', 'P1LastName': 'federer', 'P2FirstInitial': 'n', 'P2LastName': 'djokovic', 'Date': '10-08-2020'}
    getSPWData(matchDetails, '2018-01-01')


if __name__ == "__main__":
    main()
