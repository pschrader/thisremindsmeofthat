#setup
from py2neo import neo4j, node, rel
graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

#create node
def createThought(value):
    result = graph_db.create(node(text=value))
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
def createRel(thisID, relType, thatID):
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
