from crud import *
from py2neo import cypher

def showThoughts(snippitLen=30):
    snippitLine = "="
    for i in range(1,snippitLen):
        snippitLine += "="
    query = 'START n=node(*) \
        WHERE HAS (n.text) \
        RETURN n'
    data, metadata = cypher.execute(graph_db, query)
    print 'ID' + '\t' + 'Thought'
    print '====' + '\t' + snippitLine
    for row in data:
        print row[0]._id, '\t', textSnippit(row[0]._id, snippitLen)

def keywordSearch(keyword):
    query = 'START n=node(*) \
        WHERE n.text! =~ "(?i).*' + keyword + '.*" \
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

def textSnippit(nodeID, snippitLen = 32):
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



    
