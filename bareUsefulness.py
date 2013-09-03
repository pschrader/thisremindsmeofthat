from crud import *
from py2neo import cypher

def showThoughts():
    query = 'START n=node(*) RETURN n, n.name!'
    data, metadata = cypher.execute(graph_db, query)
    for row in data:
        print row[0]['text']

def popularity():
    """this function displays snippits of all the thoughts in your
    notebook in descending order based on the number of thoughts each
    thought is connected to"""
    query = 'START n=node(*) \
        MATCH (n)--(m) \
        WHERE HAS (n.text) \
        RETURN n, count(DISTINCT m) \
        ORDER BY count(DISTINCT m) DESC'
    data, metadata = cypher.execute(graph_db, query)
    for row in data:
        print row[0]._id, '\t', textSnippit(row[0]._id), '\t', row[1]

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



    
