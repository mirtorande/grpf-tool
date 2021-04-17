from single_agent_planner import compute_heuristics, a_star
import numpy as np

class DataCruncher(object):
    """Class that calculates relevant statistics from the data found by the observer."""

    def __init__(self, my_map, paths, starts, goals, agent_goals, predictions, predictions2):
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
        self.predictions2 = predictions2

        self.CPU_time = 0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    # calculate entropy at a specific timestep
    def entropy_at_timestep(self, probs):
        ent = 0.0
        for i in probs:
            if i==0:
                continue
            ent -= i * np.log2(i)
        ent /= np.log2(len(probs))
        return ent

    def calculate_entropy(self):
        entropy = dict()

        for n_agent, _ in enumerate(self.predictions):
            entropy[n_agent] = dict()
            for step, _ in enumerate(self.predictions[n_agent]):
                entropy[n_agent][step] = self.entropy_at_timestep(self.predictions[n_agent][step])

        return entropy
    
    def calculate_entropy2(self):
        entropy2 = dict()

        for n_agent, _ in enumerate(self.predictions2):
            entropy2[n_agent] = dict()
            for step, _ in enumerate(self.predictions2[n_agent]):
                entropy2[n_agent][step] = self.entropy_at_timestep(self.predictions2[n_agent][step])

        return entropy2
    
    def calculate_guess_and_metric_error(self):
        guess = dict()
        metric_error = dict()

        for n_agent, _ in enumerate(self.predictions):
            guess[n_agent] = dict()
            metric_error[n_agent] = dict()
            for step, _ in enumerate(self.predictions[n_agent]):
                # guess
                step_prediction = self.predictions[n_agent][step]
                this_guess = step_prediction.index(max(step_prediction))
                guess[n_agent][step] = this_guess

                # metric error (A* distance between guessed goal and actual goal)
                path = a_star(self.my_map, self.agent_goals[n_agent], self.goals[this_guess], self.heuristics[this_guess],
                            0, [])
                if path is None:
                    raise BaseException('No solutions')
                path_length = len(path) - 1
                metric_error[n_agent][step] = path_length
        return guess, metric_error