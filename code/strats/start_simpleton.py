#   THIS IS A DEFAULT AGENT 
# This strategy doesn't think (and doesn't even remember anything)
# It will always try to kill the first player it sees (even itself !)

def strategy(history, alivePlayers, whoami, memory):
    """
        history contains all previous rounds (key : id of player (shooter), value : id of player (target))
        alivePlayers is a list of all player ids
        whoami is your own id (to not kill yourself by mistake)
        memory is None by default and transferred over (if you set it to 1, it will be 1 in the next round)
        memory is NOT shared between games (subject to changes)
    """
        # Your code would be here but this strategy is dumb...
    """
        You must return an id of a player (if not : you shoot in the air)
        Memory must be set to something but can be anything (None included )
    """
    return alivePlayers[0], None