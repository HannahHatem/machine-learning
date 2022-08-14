from dungeon import DungeonProblem, DungeonState
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)

#TODO: Import any modules and write any functions you want to use


def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    coins = state.remaining_coins
    maxDist = 0
    exitDist = manhattan_distance(state.player, problem.layout.exit)

    if len(coins) == 0:
        return exitDist

    for coin in coins:
        # distance between palyer and the coin 
        manhDist = manhattan_distance(state.player, coin) +  manhattan_distance( coin, problem.layout.exit)
        #get the max dist tot he coin to explore less nodes
        if(  manhDist + exitDist > maxDist ):
            maxDist = manhDist + exitDist

    return maxDist
