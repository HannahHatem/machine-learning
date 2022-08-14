from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use
import math

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the tree value and the best action
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: ADD YOUR CODE HERE
    
    def max_value(state: S, maxDepth: int = -1) -> Tuple[float, A]:
        agent = game.get_turn(state)
        terminal, values = game.is_terminal(state)
        if terminal: return values[agent], None
        if maxDepth ==0: return heuristic(game, state, 0),None  # if our tree has depth limit we traverse until that certain depth and return the heuristic
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        agent = game.get_turn(actions_states[0][1])
        if agent == 0: #if the agent is the only one left in the game we keep maximizing until the game ends
            value, _, action =  max( (max_value(state,maxDepth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
        else:
            value, _, action =  max( (min_value(state,maxDepth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
        return value, action

    def min_value(state: S, maxDepth: int = -1) -> Tuple[float, A]:
        agent = game.get_turn(state)
        terminal, values = game.is_terminal(state)
        if terminal: return values[agent], None
        if maxDepth ==0: return heuristic(game, state, 0), None
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        agent = game.get_turn(actions_states[0][1])
        if agent == 0:
            value, _,action = min( (max_value(state,maxDepth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
        else: #if we have multiple monsters then we try to minimize their minimum value
            value, _, action =  min( (min_value(state,maxDepth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
        return value, action 

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None
    if game.agent_count == 1: #check if we have only one agent in the game from the beginning
        value, _, action =  max( (max_value(state,max_depth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
    else:
        value, _, action =  max( (min_value(state,max_depth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
    
    return value, action

# Apply Alpha Beta pruning and return the tree value and the best action
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha: float = -math.inf, beta: float = math.inf) -> Tuple[float, A]:
    #TODO: ADD YOUR CODE HERE
    
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None
    if max_depth == 0 : return heuristic(game, state, 0),None

    resultedaction = None
    if agent == 0:
        value = -99999
        for action, state in actions_states:
            ans = alphabeta(game, state,heuristic, max_depth-1,alpha, beta)[0]
            if value < ans: # we need the action that changed value not the last action we iterated on which is always None in Dungeon game
                resultedaction=action 
            value = max(ans, value)
            if value >= beta: return value, resultedaction
            alpha = max(alpha, value)
    else:
        value = 99999
        for action, state in actions_states: 
            ans = alphabeta(game, state,heuristic, max_depth-1,alpha, beta)[0]
            if value > ans: # we need the action that changed value not the last action we iterated on which is always None in Dungeon game
                resultedaction=action
            value = min(ans, value)
            if value <= alpha: return value, resultedaction
            beta = min(beta, value)
 
    return value, resultedaction


# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
def negamax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: ADD YOUR CODE HERE
    def max_value(state: S, maxDepth: int = -1) -> Tuple[float, A]:
        agent = game.get_turn(state)
        terminal, values = game.is_terminal(state)
        if terminal: return values[agent], None
        if maxDepth ==0: return heuristic(game, state, 0),None
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        agent = game.get_turn(actions_states[0][1])
        if agent == 0: #if the agent is the only one left in the game we keep maximizing until the game ends
            value, _, action =  max( (max_value(state,maxDepth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
        else:
            value, _, action =  max( (min_value(state,maxDepth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
        return value, action

    def min_value(state: S, maxDepth: int = -1) -> Tuple[float, A]:
        agent = game.get_turn(state)
        terminal, values = game.is_terminal(state)
        if terminal: return values[agent], None
        if maxDepth ==0: return heuristic(game, state, 0), None
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        if agent == game.agent_count-1:
            value, _,action = max((- max_value(state,maxDepth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
            value = -value
        else: #if we have multiple monsters then we try to minimize their minimum value
            value, _, action =  max(( -min_value(state,maxDepth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
            value = -value
        return value, action 

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None
    if  game.agent_count == 1:#check if we have only one agent in the game from the beginning
        value, _, action =  max((max_value(state,max_depth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
    else:
        value, _, action =  max((min_value(state,max_depth-1)[0], -index, action) for index, (action , state) in enumerate(actions_states))
       
    return value, action

# Apply Expectimax search and return the tree value and the best action
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: ADD YOUR CODE HERE
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    agent = game.get_turn(state)
    terminal, values = game.is_terminal(state)
    if terminal: return values[0], None
    if max_depth == 0 : return heuristic(game, state, 0),None

    resultedaction = None
    if agent == 0: # Here we try to maximize the value for agent 0, similar to minimax algorithim
        value = -99999
        for action, state in actions_states:
            ans = expectimax(game, state,heuristic, max_depth-1)[0]
            if value < ans:
                resultedaction=action 
            value = max(ans, value)

    else:
        value = 99999
        sum = 0
        for action, state in actions_states: 
            ans = expectimax(game, state,heuristic, max_depth-1)[0]
            sum += ans # we try to store our cummilative value for successor to genrate our proability
            if value > ans:
                resultedaction=action
            value = min(ans, value)
        avg = sum / len(actions_states) # calculate wighted average
        value = avg 

    return value, resultedaction