from single_agent_planner import compute_heuristics, a_star
import numpy as np

class SDObserver(object):
    """An observer that tries to predit the goal of an agent."""

    def __init__(self, my_map, paths, starts, goals):
        """my_map   - list of lists specifying obstacle positions
        path      - [(x1, y1), (x2, y2), ...] list of the steps take by the agent
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.paths = paths
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(starts)

        self.CPU_time = 0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

        # initialize the prediction dictionary to 1/n_goals
        self.predictions = dict()
        self.predictions2 = dict()
        """
        n_goals = len(self.goals)
        initial_prediction = []
        for goal in self.goals:
            initial_prediction.append(1/n_goals)
        self.predictions[0] = dict()
        for a in range(self.num_of_agents):
            self.predictions[0][a] = initial_prediction"""

    # (o create classi interscambiabili come è stato fatto per gli agent solver)
    def elaborate_predictions(self):
        # per ogni agente
        for n_agent in range(self.num_of_agents):
            self.predictions[n_agent] = dict()
            self.predictions2[n_agent] = dict()
            # per ogni passo
            #print(self.num_of_agents, self.paths)
            for time, step in enumerate(self.paths[n_agent]):
                # calcola la distanza da tutte le uscite
                big_N = 1000000000.0
                path_lengths = []

                for i, goal in enumerate(self.goals):
                    path = a_star(self.my_map, step, goal, self.heuristics[i],
                            0, [])
                    if path is None:
                        raise BaseException('No solutions')
                    path_length = len(path) - 1
                    path_lengths.append(path_length)

                # predictions
                prediction = []
                max_lenght = max(path_lengths)
                min_lenght = min(path_lengths)                
                for i, p_l in enumerate(path_lengths):
                    if p_l == 0:
                        prediction = [0] * len(path_lengths)
                        prediction[i] = 1
                        break
                    else:
                        prediction.append(float((max_lenght-p_l)/(max_lenght-min_lenght)))

                # predictions 2
                prediction2 = []
                sum_of_lenghts = sum(path_lengths)
                for i, p_l in enumerate(path_lengths):
                    if p_l == 0:
                        prediction2.append(big_N)
                    else:
                        prediction2.append((p_l)/(sum_of_lenghts))
                #print(prediction2)
                normalized_prediction2 = [float(i)/sum(prediction2) for i in prediction2]

                self.predictions[n_agent][time] = prediction
                self.predictions2[n_agent][time] = normalized_prediction2
        return self.predictions, self.predictions2
