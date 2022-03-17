#   THIS IS A DEFAULT AGENT 
# It will focus on one player for the all game (even itself !), if that player dies, it will change its target

# You can import default modules if you need to
import random

def pickRandom(alivePlayers, whoami):
    players = alivePlayers
    return players[random.randint(0,len(players)-1)]


def strategy(history, alivePlayers, whoami, memory):
    """
        history contains all previous rounds (key : id of player (shooter), value : id of player (target))
        alivePlayers is a list of all player ids
        whoami is your own id (to not kill yourself by mistake)
        memory is None by default and transferred over (if you set it to 1, it will be 1 in the next round)
        memory is NOT shared between games (subject to changes)
    """
    if memory is None:
        memory = pickRandom(alivePlayers, whoami)
    else:
        if memory in alivePlayers:
            return memory, None
        else:
            memory = pickRandom(alivePlayers, whoami)
    """
        You must return an id of a player (if not : you shoot in the air)
        Memory must be set to something but can be anything (None included )
    """
    return memory, None