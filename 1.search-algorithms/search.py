from asyncio.windows_events import NULL
from importlib.resources import path
from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils

#TODO: Import any modules you want to use
import heapq
import queue

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def GetSolution(initial_state, actions,guide, node):
    #This function gets the action path using the quide dictionary which it's key is a node and the value is parent
    path = [node]
    actionPath = []
    while 1:
        if  path[-1] == initial_state:
            actionPath.reverse()
            return actionPath
        path.append( guide[ path[-1] ])
        actionPath.append(actions[path[-2]])
    

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    explored = []
    frontier = []
    guide = {}    #key is a node and value is the parent
    actions = {}
    S= problem.get_initial_state()

    if S!= NULL:
        frontier.append(S)
    else:
        return None

    while len(frontier) !=0:

        node =  frontier.pop(0) 

        if problem.is_goal(node):
            return GetSolution(initial_state, actions,guide, node)

        explored.append(node)
        children = problem.get_actions(node)

        for childNode in children:
            graphNode = problem.get_successor(node,childNode)
            if ((graphNode in explored) or (graphNode in frontier)):
                pass
            
            else:
                # check is the state is a possible state to append to frontier
                if node != problem.get_successor(node,childNode):
                    guide[graphNode] = node
                    actions[graphNode] = childNode
                    frontier.append(graphNode)
        
    
    return None   

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    Solution = []
    stack = []
    guide = {}
    actions = {}
    S= problem.get_initial_state()

    if S!= NULL:
        stack.append(S)
    else:
        return None

    while len(stack) !=0:
        node =  stack.pop()

        if problem.is_goal(node):
            return GetSolution(initial_state, actions,guide, node)

        Solution.append(node)
        children = problem.get_actions(node)

        for childNode in children:
            
            graphNode = problem.get_successor(node,childNode)
            if ((graphNode in Solution) or (graphNode in stack)):
                pass
            
            else:
                if node != problem.get_successor(node,childNode):
                    guide[graphNode] = node
                    actions[graphNode] = childNode
                    stack.append(graphNode)
        
    return None   

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    explored = []
    frontier =  [] # here the frontier is a list of tuples (node, cost) 
    guide = {}    
    actions = {}
    cost = {}
    S= problem.get_initial_state()
    cost[S] = 0

    if S!= NULL:
        frontier.append(tuple((S, 0)))
    else:
        return None

    while len(frontier) !=0:
        # sort frontier descendingly according to their cost which is tup[1]
        frontier.sort(key=lambda tup: tup[1], reverse=False)
        # pop the first node after sorting which is tup[0]
        node =  frontier.pop(0)[0]

        if problem.is_goal(node):
           return GetSolution(initial_state, actions,guide, node)

        explored.append(node)
        children = problem.get_actions(node)

        for childNode in children:
            # graphNode is a possible state, childNode is an action
            graphNode = problem.get_successor(node,childNode)

            if graphNode in explored :
                pass
            
            else:
                #check if it's a possible action
                if node != problem.get_successor(node,childNode):
                    currCost = cost[node]+problem.get_cost(node,childNode)
                    # add a boolean to append graphNode to the frontier once 
                    isFound = False
                    # check if the node already exists in frontier to replace it with similar node if found
                    for frontNode in frontier:
                        if graphNode == frontNode[0] and (currCost < frontNode[1]):
                            frontier.remove(frontNode)
                            frontier.append(tuple((graphNode, currCost)))
                            cost[graphNode] = currCost
                            guide[graphNode] = node
                            actions[graphNode] = childNode
                            isFound = True
                            break
                        # if the node is found in frontier but we won't replace it as the frontier already has the one with lower cost
                        if graphNode == frontNode[0]:
                            isFound = True
                            break
                    
                    if isFound == False:
                        guide[graphNode] = node
                        actions[graphNode] = childNode
                        cost[graphNode] = cost[node]+problem.get_cost(node,childNode)
                        frontier.append(tuple((graphNode, cost[node]+problem.get_cost(node,graphNode))))

    return None   

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    explored = []
    frontier =  [] # here the frontier is a list of tuples (node, cost)
    guide = {}
    cost = {}
    actions = {}
    S= problem.get_initial_state()
    cost[S] = 0

    if S!= NULL:
        frontier.append(tuple((S, 0)))
    else:
        return None

    while len(frontier) !=0:
        # sort frontier descendingly according to their cost which is tup[1]
        frontier.sort(key=lambda tup: tup[1], reverse=False)
        # pop the first node after sorting which is tup[0]
        node =  frontier.pop(0)[0]

        if problem.is_goal(node):
            return GetSolution(initial_state, actions,guide, node)

        explored.append(node)
        children = problem.get_actions(node)

        for childNode in children:
            # graphNode is a possible state, childNode is an action
            graphNode = problem.get_successor(node,childNode)
           
            if graphNode in explored :
                pass
            
            else:
                #check if it's a possible action
                if node != problem.get_successor(node,childNode):
                    # add a boolean to append graphNode to the frontier once 
                    currCost = cost[node]+problem.get_cost(node,childNode)+ heuristic(problem,graphNode)
                    isFound = False
                    # check if the node already exists in frontier to replace it with similar node if found
                    for frontNode in frontier:
                        if graphNode == frontNode[0] and (currCost < frontNode[1]+ heuristic(problem,frontNode[0])):
                            frontier.remove(frontNode)
                            frontier.append(tuple((graphNode, cost[node]+problem.get_cost(node,childNode)+heuristic(problem,graphNode) )))
                            cost[graphNode] = cost[node]+problem.get_cost(node,childNode)
                            guide[graphNode] = node
                            actions[graphNode] = childNode
                            isFound = True
                            break
                        # if the node is found in frontier but we won't replace it as the frontier already has the one with lower cost
                        if graphNode == frontNode[0]:
                            isFound = True
                            break
                    
                    if isFound == False:
                        guide[graphNode] = node
                        actions[graphNode] = childNode
                        cost[graphNode] = cost[node]+problem.get_cost(node,childNode)
                        frontier.append(tuple((graphNode, cost[node]+problem.get_cost(node,childNode)+heuristic(problem,graphNode) )  ))

    return None
   
def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    explored = []
    frontier =  [] # here the frontier is a list of tuples (node, cost)
    guide = {}
    actions = {}
    S= problem.get_initial_state()

    if S!= NULL:
        frontier.append(tuple((S, 0)))
    else:
        return None

    while len(frontier) !=0:
        # sort frontier descendingly according to their cost which is tup[1]
        frontier.sort(key=lambda tup: tup[1], reverse=False)
        # pop the first node after sorting which is tup[0]
        node =  frontier.pop(0)[0] 
       
        if problem.is_goal(node):
            return GetSolution(initial_state, actions,guide, node)

        explored.append(node)
        children = problem.get_actions(node)
        
        for childNode in children:
            # graphNode is a possible state, childNode is an action
            graphNode = problem.get_successor(node,childNode)
            
            if graphNode in explored :
                pass
            
            else:
                #check if it's a possible action  
                if node != problem.get_successor(node,childNode):
                    # add a boolean to append graphNode to the frontier once 
                    isFound = False
                    # check if the node already exists in frontier to replace it with similar node if found
                    for frontNode in frontier:
                        if graphNode == frontNode[0] and (heuristic(problem,graphNode) < heuristic(problem,frontNode[0])):
                            frontier.remove(frontNode)
                            frontier.append(tuple((graphNode, heuristic(problem,graphNode) )))
                            guide[graphNode] = node
                            actions[graphNode] = childNode
                            isFound = True
                            break
                        if graphNode == frontNode[0]:
                            isFound = True
                            break
                        # if the node is found in frontier but we won't replace it as the frontier already has the one with lower cost
                    if isFound == False:
                        guide[graphNode] = node
                        actions[graphNode] =childNode
                        frontier.append(tuple((graphNode, heuristic(problem,graphNode) )  ))

    return None