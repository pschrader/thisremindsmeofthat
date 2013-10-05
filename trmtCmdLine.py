"""command prompt interface for thisremindsmeofthat"""
from trmtFunctions import *
import string

def cmdLine():
    command = raw_input('enter command:')
    if command == 'end':
        return
    processCommand(command)
    cmdLine()


def getCmd(command):
    words = string.split(command, ' ')
    return words[0]

def getArgs(command):
    words = string.split(command, ' ')
    args = []
    for w in words:
        if w[0] == '-':
            args.append(w)
    return args

def getCmdPhrase(command):
    words = string.split(command, '"')
    if len(words) > 2:
        return words[-2]
    else:
        return False

def getIDs(command):
    words = string.split(command, ' ')
    ids = [int(s) for s in command.split() if s.isdigit()]
    return ids
            

def processCommand(command):
    commandWord = getCmd(command)
    args = getArgs(command)
    cmdPhrase = getCmdPhrase(command)
    ids = getIDs(command)

    if commandWord == 'add':
        createThought(cmdPhrase)
    if commandWord == 'ls':
        showThoughts()
    if commandWord == 'kwrd':
        keywordSearch(cmdPhrase)
    if commandWord == 'pop':
        popularity()
    if commandWord == 'trt': 
        createRel(ids[0], cmdPhrase, ids[1])
    if commandWord == 'sr':
        showRelated(ids[0])
    if commandWord == 'delrel':
        delRel(ids[0],ids[1])
    if commandWord == 'reprel':
        repRel(ids[0], ids[1], cmdPhrase)
    if commandWord == 'delnode':
        n = graph_db.node(ids[0])
        n.isolate()
        n.delete()
    if commandWord == 'delnodes':
        for iid in ids:
            nodeID = iid
            n = graph_db.node(nodeID)
            n.isolate()
            n.delete()
    if commandWord == 'edit':
        editThought(ids[0], cmdPhrase)
        thought = graph_db.node(ids[0])
        print thought._id, '\t', thought['text']
    if commandWord == 'pqry':
        printQuery( storedQueries[cmdPhrase] )
    if commandWord == 'lsqry':
        for key in storedQueries:
            print key
    
    return
