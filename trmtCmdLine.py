"""command prompt interface for thisremindsmeofthat"""
from bareUsefulness import *
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

    if commandWord == 'add':
        createThought(cmdPhrase)
    if commandWord == 'la':
        showThoughts()
    if commandWord == 'kwrd':
        keywordSearch(cmdPhrase)
    if commandWord == 'pop':
        popularity()
    if commandWord == 'trt':
        ids = getIDs(command)
        createRel(ids[0], cmdPhrase, ids[1])
    if commandWord == 'sr':
        ids = getIDs(command)
        showRelated(ids[0])
    
    return
