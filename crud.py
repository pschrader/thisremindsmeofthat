#setup
from py2neo import neo4j, node, rel
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

#create node
def createThought(value):
    result = graph_db.create(node(text=value))
    return result

#read node
def readThought(nodeID):
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
