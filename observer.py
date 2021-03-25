from single_agent_planner import compute_heuristics, a_star

class Observer(object):
    """An observer that tries to predit the goal of an agent."""

    def __init__(self, my_map, path, start, goals):
        """my_map   - list of lists specifying obstacle positions
        path      - [(x1, y1), (x2, y2), ...] list of the steps take by the agent
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.path = path
        self.start = start
        self.goals = goals

        self.CPU_time = 0

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

        # initialize the prediction dictionary to 1/n_goals
        self.predictions = dict()
        n_goals = len(self.goals)
        """initial_prediction = []
        for goal in self.goals:
            initial_prediction.append(1/n_goals)
        self.predictions[0] = initial_prediction"""
    
    # algoritmo stub, andrà poi reso separabile dalla classe
    # (o create classi interscambiabili come è stato fatto per gli agent solver)
    def elaborate_predictions(self):
        # per ogni passo
        for time, step in enumerate(self.path):
            # calcola la distanza da tutte le uscite
            path_lengths = []
            for i, goal in enumerate(self.goals):
                path = a_star(self.my_map, step, goal, self.heuristics[i],
                          0, [])
                if path is None:
                    raise BaseException('No solutions')
                path_length = len(path) - 1
                path_lengths.append(path_length)
            # calculate prediction
            prediction = []
            sum_of_lengths = sum(path_lengths)
            for p_l in path_lengths:
                if p_l == 0:
                    prediction.append(10000000)
                else:
                    prediction.append(sum_of_lengths/p_l)
            normalized_prediction = [float(i)/sum(prediction) for i in prediction]
            self.predictions[time] = normalized_prediction
        print("Observer predictions: ", self.predictions)

