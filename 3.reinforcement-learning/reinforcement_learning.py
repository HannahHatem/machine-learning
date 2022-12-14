from typing import Callable, DefaultDict, Dict, Generic, List, Optional, Union
from agents import Agent
from environment import Environment, S, A
from helpers.mt19937 import RandomGenerator

import json
from collections import defaultdict

# The base class for all Reinforcement Learning Agents required for this problem set
class RLAgent(Agent[S, A]):
    rng: RandomGenerator # A random number generator used for exploration
    actions: List[A] # A list of all actions that the environment accepts
    discount_factor: float # The discount factor "gamma"
    epsilon: float # The exploration probability for epsilon-greedy
    learning_rate: float # The learning rate "alpha"

    def __init__(self,
            actions: List[A], 
            discount_factor: float = 0.99, 
            epsilon: float = 0.5, 
            learning_rate: float = 0.01, 
            seed: Optional[int] = None) -> None:
        super().__init__()
        self.rng = RandomGenerator(seed) # initialize the random generator with a seed for reproducability
        self.actions = actions
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.learning_rate = learning_rate

    # A virtual function that returns the Q-value for a specific state and action
    # This should be overriden by the derived RL agents
    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        return 0
    
    # Returns true if we should explore (rather than exploit)
    def should_explore(self) -> bool:
        return self.rng.float() < self.epsilon

    def act(self, env: Environment[S, A], observation: S, training: bool = False) -> A:
        actions = env.actions()
        if training and self.should_explore():
            #Return a random action whose index is "self.rng.int(0, len(actions)-1)"
            return actions[self.rng.int(0, len(actions)-1)]
        else:
            #Return the action with the maximum q-value as calculated by "compute_q" above
            # if more than one action has the maximum q-value, return the one that appears first in the "actions" list
            _, _, best_action = max((self.compute_q(env, observation, action), -index, action) for index, action in enumerate(actions))
            return best_action

#############################
#######     SARSA      ######
#############################

# This is a class for a generic SARSA agent
class SARSALearningAgent(RLAgent[S, A]):
    Q: DefaultDict[str, DefaultDict[str, float]] # The table of the Q values
                                                 # The first key is the string representation of the state
                                                 # The second key is the string representation of the action
                                                 # The value is the Q-value of the given state and action
    
    def __init__(self, 
            actions: List[A], 
            discount_factor: float = 0.99, 
            epsilon: float = 0.5, 
            learning_rate: float = 0.01, 
            seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda:defaultdict(lambda:0)) # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        return self.Q[str(state)][str(action)] # Return the Q-value of the given state and action
        # NOTE: we cast the state and the action to a string before querying the dictionaries
    
    # Update the value of Q(state, action) using this transition via the SARSA update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, next_action: Optional[A]):
        #TODO: Complete this function to update Q-table using the SARSA update rule
        # If next_action is None, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        if next_action == None:
            next_state = 0
        self.Q[str(state)][str(action)] = self.Q[str(state)][str(action)] + self.learning_rate * (reward + self.discount_factor * self.Q[str(next_state)][str(next_action)] - self.Q[str(state)][str(action)])

    # Save the Q-table to a json file
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.Q, f, indent=2, sort_keys=True)
    
    # load the Q-table from a json file
    def load(self, file_path: str):
        with open(file_path, 'r') as f:
            self.Q = json.load(f)

#############################
#####   Q-Learning     ######
#############################

# This is a class for a generic Q-learning agent
class QLearningAgent(RLAgent[S, A]):
    Q: DefaultDict[str, DefaultDict[str, float]] # The table of the Q values
                                                 # The first key is the string representation of the state
                                                 # The second key is the string representation of the action
                                                 # The value is the Q-value of the given state and action
    
    def __init__(self, 
            actions: List[A], 
            discount_factor: float = 0.99, 
            epsilon: float = 0.5, 
            learning_rate: float = 0.01, 
            seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda:defaultdict(lambda:0)) # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        return self.Q[str(state)][str(action)] # Return the Q-value of the given state and action
        # NOTE: we cast the state and the action to a string before querying the dictionaries
    
    # Given a state, compute and return the utility of the state using the function "compute_q"
    def compute_utility(self, env: Environment[S, A], state: S) -> float:
        #TODO: Complete this function.
        # return the uitility of the given state using the function "compute_q"
        #Compute the max utility  value of the given state and action
        return max(self.compute_q(env, state, action) for action in env.actions())
        #return compute_q(env, state, self.act(env, state, False))

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        #TODO: Complete this function to update Q-table using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        if done:
            next_state = 0
        #Update the q of the given state and action
        self.Q[str(state)][str(action)] = self.Q[str(state)][str(action)] + self.learning_rate * (reward + self.discount_factor * self.compute_utility(env, next_state) - self.Q[str(state)][str(action)])

    
    # Save the Q-table to a json file
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.Q, f, indent=2, sort_keys=True)
    
    # load the Q-table from a json file
    def load(self, file_path: str):
        with open(file_path, 'r') as f:
            self.Q = json.load(f)

#########################################
#####   Approximate Q-Learning     ######
#########################################

# The type definition for a set of features representing a state
# The key is the feature name and the value is the feature value
Features = Dict[str, float]

# This class takes a state and returns the a set of features
class FeatureExtractor(Generic[S, A]):

    # Returns a list of feature names.
    # This will be used by the Approximate Q-Learning agent to initialize its weights dictionary.
    @property
    def feature_names(self) -> List[str]:
        return []
    
    # Given an enviroment and an observation (a state), return a set of features that represent the given state
    def extract_features(self, env: Environment[S, A], state: S) -> Features:
        return {}

# This is a class for a generic Q-learning agent
class ApproximateQLearningAgent(RLAgent[S, A]):
    weights: Dict[str, Features]    # The weights dictionary for this agent.
                                    # The first key is action and the second key is the feature name
                                    # The value is the weight 
    feature_extractor: FeatureExtractor[S, A]   # The feature extractor used to extract the features corresponding to a state

    def __init__(self, 
            feature_extractor: FeatureExtractor[S, A],
            actions: List[A], 
            discount_factor: float = 0.99, 
            epsilon: float = 0.5, 
            learning_rate: float = 0.01,
            seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        feature_names = feature_extractor.feature_names
        self.weights = {str(action):{feature: 0 for feature in feature_names} for action in actions} # we initialize the weights to 0
        self.feature_extractor = feature_extractor

    # Given the features of state and an action, compute and return the Q value
    def __compute_q_from_features(self, features: Dict[str, float], action: A) -> float:
        #TODO: Complete this function
        # NOTE: Remember to cast the action to string before quering self.weights
        # given the features of state and an action. Compute and return the Q value
        #Compute the q value of the given state and action
        return sum(self.weights[str(action)][feature] * features[feature] for feature in features)
        
    
    # Given the features of a state, compute and return the utility of the state using the function "__compute_q_from_features"
    def __compute_utility_from_features(self, features: Dict[str, float]) -> float:
        #TODO: Complete this function
        # given the features of a state, compute and return the utility of the state using the function "__compute_q_from_features"
        #Compute the max q value of the given state and action
        return max(self.__compute_q_from_features(features, action) for action in self.actions)

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        features = self.feature_extractor.extract_features(env, state)
        return self.__compute_q_from_features(features, action)

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        #TODO: Complete this function to update weights using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        #First, we start by computin the features of the state and the next_state
        my_next_features = self.feature_extractor.extract_features(env, next_state)
        my_features = self.feature_extractor.extract_features(env, state)
        if done:
            next_state = 0
        else:
            next_state = self.__compute_utility_from_features(my_next_features)
        #We start updating the weights
        q = self.compute_q(env, state, action)
        for feature, featureVal in my_features.items():
            self.weights[str(action)][feature] = self.weights[str(action)][feature] + self.learning_rate * ( (reward+self.discount_factor*next_state) - q) * featureVal
    
    # Save the weights to a json file
    def save(self, file_path: str):
        with open(file_path, 'w') as f:
            json.dump(self.weights, f, indent=2, sort_keys=True)
    
    # load the weights from a json file
    def load(self, file_path: str):
        with open(file_path, 'r') as f:
            self.weights = json.load(f)