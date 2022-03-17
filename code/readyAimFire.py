import os
import importlib
import numpy as np
import random

from sklearn.utils import shuffle

class AttrDict(dict): 
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

STRATEGY_FOLDER = "strats"
RESULTS_FILE = "results.txt"

# moveLabels = ["F","A","S"]
# F = fire at someone
# A = shoot in the air
# S = suicide


def getVisibleHistory(history, player, turn):
    historySoFar = history[:,:turn].copy()
    if player == 1:
        historySoFar = np.flip(historySoFar,0)
    return historySoFar

def getAlivePlayers(players):
    L = AttrDict()
    for p in players:
        p = players[p]
        if p.alive:
            L[p.id] = p
    return L

def getSanitizedPlayers(players):
    L = []
    for p in players:
        p = players[p]
        if p.alive:
            L.append(p.id)
    return L
    
def runGame(participants):
    allPlayers = AttrDict()
    
    for i in range(len(participants)):
        allPlayers[participants[i]] = AttrDict({
            "id":participants[i],
            "module": importlib.import_module(STRATEGY_FOLDER+"."+participants[i]),
            "memory": None,
            "alive": True,
            "attacks":[],
            "suicide":False,
            "turns":0,
            "kills":0,
            "win":False
        })
    
    players = allPlayers
    alive = len(players)
    history = []
    while alive > 1:
        # We initialize this round
        for p in players:
            p = players[p]
            p.attacks = []
            p.suicide = False
            p.turns += 1
            allPlayers[p.id].turns += 1
        round = {}

        # We add the moves of everyone
        sanitized = getSanitizedPlayers(players)
        for p in players:
            p = players[p]
            target, memory = p.module.strategy(history.copy(), sanitized.copy(), p.id, p.memory)
            p.memory = memory
            round[p.id] = target
            if target == p.id:
                p.suicide = True
            else:
                if target in players:
                    t = players[target]
                    t.attacks.append(p.id)

        # We kill people for free now
        for p in players:
            p = players[p]
            if p.suicide:
                if len(p.attacks) == 0: # Suicide without attacks
                    p.alive = False
                    p.kills += 1
                else: # Suicide and attacked (meaning the player will NOT die)
                    for e in p.attacks:
                        players[e].alive = False
                    p.kills += len(p.attacks)
            else:
                if len(p.attacks) > 0:  # Attacked without suicide
                    p.alive = False
                    for e in p.attacks:    
                        players[e].kills += 1  

        players = getAlivePlayers(players)
        alive = len(players)
        history.append(round)

    for p in players:
        p = players[p]
        allPlayers[p.id].turns += 1
        allPlayers[p.id].win = True
        
    return history, allPlayers

def playerScore(player):
    return 2*player.turns+4*int(player.win)+player.kills
    
def outputRoundResults(f, files, players, roundHistory):
    for p in files:
        f.write(f"{p} scored {playerScore(players[p])} : ")
        for h in roundHistory:
            if not p in h: break
            move = h[p]
            if move == p:
                f.write("S ")
            elif move != p:
                if move in players:
                    f.write(f"F[{move}] ")
                else:
                    f.write("A ")
        if players[p].win:
            f.write("Winner !")
        f.write("\n")
    f.write("\n")
    
def pad(stri, leng):
    result = stri
    for i in range(len(stri),leng):
        result = result+" "
    return result
    
def runFullPairingTournament(inFolder, outFile):
    print("Starting tournament, reading files from "+inFolder)
    scoreKeeper = {}
    STRATEGY_LIST = []
    for file in os.listdir(inFolder):
        if file.endswith(".py"):
            STRATEGY_LIST.append(file[:-3])
            
    for strategy in STRATEGY_LIST:
        scoreKeeper[strategy] = 0
        
    f = open(outFile,"w+")
    AMOUNT_OF_GAME = int(200-40*np.log(1-random.random())) # The games are a minimum of 200 turns long. The np.log here guarantees that every turn after the 200th has an equal (low) chance of being the final turn.
    
    for i in range(AMOUNT_OF_GAME):
        STRATEGY_LIST = shuffle(STRATEGY_LIST)
        LIST = random.sample(STRATEGY_LIST, int(len(STRATEGY_LIST)*0.75))
        roundHistory, players = runGame(LIST)
        f.write(f"Game {i} ({len(roundHistory)} rounds) :\n")
        outputRoundResults(f, LIST, players, roundHistory)
        for p in LIST:
            scoreKeeper[p] += playerScore(players[p])
        
    scoresNumpy = np.zeros(len(scoreKeeper))
    for i in range(len(STRATEGY_LIST)):
        scoresNumpy[i] = scoreKeeper[STRATEGY_LIST[i]]
    rankings = np.argsort(scoresNumpy)

    f.write("\n\nTOTAL SCORES\n")
    for rank in range(len(STRATEGY_LIST)):
        i = rankings[-1-rank]
        score = scoresNumpy[i]
        scorePer = score/AMOUNT_OF_GAME
        f.write("#"+str(rank+1)+": "+pad(STRATEGY_LIST[i]+":",16)+' %.3f'%score+'  (%.3f'%scorePer+" average)\n")
        
    f.flush()
    f.close()
    print("Done with everything! Results file written to "+RESULTS_FILE)
    
    
runFullPairingTournament(STRATEGY_FOLDER, RESULTS_FILE)
