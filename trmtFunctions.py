"""This is a This Reminds Me of That Fuction libary
The idea is to put all the useful functions in one organized list
Then have a separte file that implements a command line interface"""


#setup
from py2neo import neo4j, node, rel, cypher
neo4j_url = raw_input('Enter url of neo4j:')
#for example:  http://localhost:7474/db/data/
graph_db = neo4j.GraphDatabaseService(neo4j_url)
thought_owner = raw_input('Enter your name, thinker:')



"""
List of functions:
- createThought
- getThought
- editThought
- deleteThought
- createRel
- getRel
- deleteRel
- showThoughts
- keywordSearch
- showRelated
- popularity
- textSnippit
- delRel
- repRel
- printQuery
"""
#create node
def createThought(value, thought_owner):
    result = graph_db.create(node(text=value, owner=thought_owner))
    print result
    return result

#read node
def getThought(nodeID):
    thought = graph_db.node(nodeID)
    return thought['text']

#update node
def editThought(nodeID, text):
    thought = graph_db.node(nodeID)
    thought['text'] = text
    return thought

#delete node
def deleteThought(nodeID):
    thought = graph_db.node(nodeID)
    thought.delete()
    print thought

#create relationship
def createRel(thisID, relType, thatID, thought_owner):
    this = graph_db.node(thisID)
    that = graph_db.node(thatID)
    #do a string transformation on relType
    #so that it's UPPERCASE with _ for spaces
    relationship = graph_db.create(
        rel(this, relType, that)
        )
    #nice output would be nicer
    return rel

#read relationship
def getRel(relID):
    rel = graph_db.relationship(relID)
    #if you print the rel variable you get some info
    #returning it just gives the url, not sure how useful this function is
    return rel

#edit relationship
#I think in the case of relationships you would just add a new one and delete the old one

#delete relationship
def deleteRel(relID):
    rel = graph_db.relationship(relID)
    rel.delete()
    print rel

def showThoughts(snippitLen=70):
    snippitLine = "="
    for i in range(1,snippitLen):
        snippitLine += "="
    query = 'START n=node(*) \
        WHERE HAS (n.text) \
        RETURN n \
        ORDER BY ID(n) DESC \
        LIMIT 17'
    data, metadata = cypher.execute(graph_db, query)
    print 'ID' + '\t' + 'Thought'
    print '====' + '\t' + snippitLine
    for row in data:
        print row[0]._id, '\t', textSnippit(row[0]._id, snippitLen)

def keywordSearch(keyword):
    query = 'START n=node(*) \
        WHERE HAS (n.text) and n.text =~ "(?i).*' + keyword + '.*" \
        RETURN n'
    data, metadata = cypher.execute(graph_db, query)
    for row in data:
        print row[0]._id, '\t', row[0]['text']
    
def showRelated(nodeID,snippitLen=30):
    print textSnippit(nodeID)
    print '========'
    #first print outgoing relationships
    queryOutgoing = 'START n=node(' + str(nodeID) + ') \
            MATCH (n)-[r]->(m) \
            RETURN m, type(r)'
    data, metadata = cypher.execute(graph_db, queryOutgoing)
    for row in data:
        print row[1], '->', row[0]['text'], '(' + str(row[0]._id) +')'
    print ''
    #next print incoming relationships
    queryOutgoing = 'START n=node(' + str(nodeID) + ') \
            MATCH (n)<-[r]-(m) \
            RETURN m, type(r)'
    data, metadata = cypher.execute(graph_db, queryOutgoing)
    for row in data:
        print '<-', row[1], row[0]['text'], '(' + str(row[0]._id) +')'
    

def popularity(snippitLen=30):
    """this function displays snippits of all the thoughts in your
    notebook in descending order based on the number of thoughts each
    thought is connected to"""
    snippitSpaces = " "
    for i in range(1,snippitLen):
        snippitSpaces += " "
    snippitLine = "="
    for i in range(1,snippitLen):
        snippitLine += "="
    query = 'START n=node(*) \
        MATCH (n)--(m) \
        WHERE HAS (n.text) \
        RETURN n, count(DISTINCT m) \
        ORDER BY count(DISTINCT m) DESC'
    data, metadata = cypher.execute(graph_db, query)
    print 'ID' + '\t' + 'Thought' + snippitSpaces[:-7] + '\t' + 'Count Linked'
    print '====' '\t' + snippitLine + '\t' + '============'
    for row in data:
        print row[0]._id, '\t', textSnippit(row[0]._id, snippitLen), '\t', row[1]

def textSnippit(nodeID, snippitLen = 64):
    """this function is for use when displaying lists of thoughts
    it gives you a snippit string based on the text value that is
    exactly the length you want - either by trimming or padding with spaces"""
    raw = graph_db.node(nodeID)['text']
    if len(raw) > snippitLen:
        snippit = raw[0:snippitLen]
    elif len(raw) < snippitLen:
        for i in range (0, snippitLen - len(raw)):
            raw = raw + " "
        snippit = raw
    else:
        snippit = raw
    return snippit

def delRel(nodeID, nodeID2):
    query = 'START n=node(' + str(nodeID) + '), m=node(' + str(nodeID2) + ') \
    MATCH (n)-[r]-(m) \
    DELETE r'
    data, metadata = cypher.execute(graph_db, query)

def repRel(nodeID, nodeID2, newRel):
    delRel(nodeID, nodeID2)
    createRel(nodeID, newRel, nodeID2)

def printQuery(query):
    data, metadata = cypher.execute(graph_db, query)
    for row in data:
        line = ''
        for col in row:
            line += str(col)
            line += '\t'
        print line[0:-1]
