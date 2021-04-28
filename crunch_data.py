from single_agent_planner import compute_heuristics, a_star
import numpy as np
import pandas as pd
from scipy.stats import entropy as scipy_entropy

class DataCruncher(object):
    """Class that calculates relevant statistics from the data found by the observer."""

    def __init__(self, my_map, paths, starts, goals, agent_goals, predictions):
        """my_map   - list of lists specifying obstacle positions
        path      - [(x1, y1), (x2, y2), ...] list of the steps take by the agent
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.paths = paths
        self.starts = starts
        self.goals = goals
        self.agent_goals = agent_goals
        self.num_of_agents = len(starts)
        self.predictions = predictions

        self.CPU_time = 0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    """
    # calculate entropy at a specific timestep
    def entropy_at_timestep(self, probs):
        ent = 0.0
        for p_i in probs:
            if p_i==0:
                continue
            ent -= p_i * np.log2(i)
        ent /= np.log2(len(probs))
        return ent"""

    def calculate_entropy(self):
        entropies = dict()

        for n_agent, _ in enumerate(self.predictions):
            entropies[n_agent] = dict()
            possibile_goals = len(self.predictions[n_agent])
            for step, _ in enumerate(self.predictions[n_agent]):
                entropies[n_agent][step] = scipy_entropy(self.predictions[n_agent][step], base=possibile_goals)

        # mean of entropies
        mean_entropy = []
        for step, _ in enumerate(entropies[0]):
            step_values = []
            for n_agent, _ in enumerate(entropies):
                if step in entropies[n_agent]:
                    step_values.append(entropies[n_agent][step])
            mean_entropy.append(np.mean(step_values))

        # maximum entropy for step
        max_entropy = []
        for step, _ in enumerate(entropies[0]):
            step_values = []
            for n_agent, _ in enumerate(entropies):
                if step in entropies[n_agent]:
                    step_values.append(entropies[n_agent][step])
            max_entropy.append(max(step_values))
        
        return mean_entropy, max_entropy


    def calculate_metric_error(self):
        metric_errors = dict()

        for n_agent, _ in enumerate(self.predictions):
            metric_errors[n_agent] = dict()
            for step, _ in enumerate(self.predictions[n_agent]):
                # guess
                step_prediction = self.predictions[n_agent][step]
                this_guess = step_prediction.index(max(step_prediction))

                # metric error (A* distance between guessed goal and actual goal)
                path = a_star(self.my_map, self.agent_goals[n_agent], self.goals[this_guess], self.heuristics[this_guess],
                            0, [])
                if path is None:
                    raise BaseException('No solutions')
                path_length = len(path) - 1
                metric_errors[n_agent][step] = path_length
        
        # mean of metric errors
        mean_metric_error = []
        for step, _ in enumerate(metric_errors[0]):
            step_values = []
            for n_agent, _ in enumerate(metric_errors):
                if step in metric_errors[n_agent]:
                    step_values.append(metric_errors[n_agent][step])
            mean_metric_error.append(np.mean(step_values))

        # maximum entropy for step
        max_metric_error = []
        for step, _ in enumerate(metric_errors[0]):
            step_values = []
            for n_agent, _ in enumerate(metric_errors):
                if step in metric_errors[n_agent]:
                    step_values.append(metric_errors[n_agent][step])
            max_metric_error.append(max(step_values))

        return mean_metric_error, max_metric_error
    
    def calculate_guess(self):
        guess = dict()

        for n_agent, _ in enumerate(self.predictions):
            guess[n_agent] = dict()
            for step, _ in enumerate(self.predictions[n_agent]):
                # guess
                step_prediction = self.predictions[n_agent][step]
                this_guess = step_prediction.index(max(step_prediction))
                guess[n_agent][step] = this_guess
        return guess