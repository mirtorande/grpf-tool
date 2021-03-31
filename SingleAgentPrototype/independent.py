import time as timer
from single_agent_planner import compute_heuristics, a_star, get_sum_of_cost


class IndependentSolver(object):
    """A planner that plans for each robot independently."""

    def __init__(self, my_map, start, goal):
        """my_map   - list of lists specifying obstacle positions
        start      - (x, y) start location
        goal       - (x, y) goal location
        """

        self.my_map = my_map
        self.start = start
        self.goal = goal

        self.CPU_time = 0

        # compute heuristics for the low-level search
        self.heuristics = compute_heuristics(my_map, goal)

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations."""

        start_time = timer.time()
        result = []

        path = a_star(self.my_map, self.start, self.goal, self.heuristics, 0, [])
        if path is None:
            raise BaseException('No solutions')
        result = path

        self.CPU_time = timer.time() - start_time

        print("\n Found a solution! \n")
        print("CPU time (s):    {:.2f}".format(self.CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(result)))

        return result
