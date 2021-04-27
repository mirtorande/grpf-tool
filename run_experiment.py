#!/usr/bin/python
import argparse
import glob
from pathlib import Path
from cbs import CBSSolver
from independent import IndependentSolver
from prioritized import PrioritizedPlanningSolver
from visualize import Animation
from single_agent_planner import get_sum_of_cost
from shortest_distance_observer import SDObserver
from crunch_data import DataCruncher
import json
import os

SOLVER = "CBS"

def print_experiment_instance(my_map, starts, goals):
    print('Start locations')
    print_locations(my_map, starts)
    print('Goal locations')
    print_locations(my_map, goals)


def print_locations(my_map, locations):
    starts_map = [[-1 for _ in range(len(my_map[0]))] for _ in range(len(my_map))]
    for i in range(len(locations)):
        starts_map[locations[i][0]][locations[i][1]] = i
    to_print = ''
    for x in range(len(my_map)):
        for y in range(len(my_map[0])):
            if starts_map[x][y] >= 0:
                to_print += str(starts_map[x][y]) + ' '
            elif my_map[x][y]:
                to_print += '@ '
            else:
                to_print += '. '
        to_print += '\n'
    print(to_print)

def import_environment(filename):
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    f = open(filename, 'r')
    # first line: #rows #columns
    line = f.readline()
    rows, columns = [int(x) for x in line.split(' ')]
    rows = int(rows)
    columns = int(columns)
    # #rows lines with the map
    my_map = []
    for r in range(rows):
        line = f.readline()
        my_map.append([])
        for cell in line:
            if cell == '@':
                my_map[-1].append(True)
            elif cell == '.':
                my_map[-1].append(False)
    # next line: #goals
    line = f.readline()
    num_goals = int(line)
    goals = []
    for g in range(num_goals):
        line = f.readline()
        gx, gy = [int(x) for x in line.split(' ')]
        goals.append((gx, gy))
    f.close()
    return my_map, goals



def import_experiment(filename):
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    f = open(filename, 'r')
    # first line: environment ID
    line = f.readline()
    my_map, goals = import_environment("instances/"+line.rstrip()+".txt")
    
    # #agents
    line = f.readline()
    num_agents = int(line)
    # #agents lines with the start positions
    starts = []
    for a in range(num_agents):
        line = f.readline()
        sx, sy = [int(x) for x in line.split(' ')]
        starts.append((sx, sy))
    # agent goals
    agent_goals = []
    for a in range(num_agents):
        line = f.readline()
        goal_id = int(line)
        agent_goals.append(goals[goal_id])

    f.close()
    return my_map, starts, goals, agent_goals


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs various MAPF algorithms')
    parser.add_argument('--instance', type=str, default=None,
                        help='The name of the instance file(s)')
    parser.add_argument('--batch', action='store_true', default=False,
                        help='Use batch output instead of animation')
    parser.add_argument('--disjoint', action='store_true', default=False,
                        help='Use the disjoint splitting')
    parser.add_argument('--solver', type=str, default=SOLVER,
                        help='The solver to use (one of: {CBS,Independent,Prioritized}), defaults to ' + str(SOLVER))

    args = parser.parse_args()

    # result_file = open("results.csv", "w", buffering=1)

    for file in sorted(glob.glob("instances/" + args.instance)):

        print("***Import an instance***")
        my_map, starts, goals, agent_goals = import_experiment(file)
        #print(starts, agent_goals)
        print_experiment_instance(my_map, starts, goals)

        if args.solver == "CBS":
            print("***Run CBS***")
            cbs = CBSSolver(my_map, starts, agent_goals)
            paths = cbs.find_solution(args.disjoint)
        elif args.solver == "Independent":
            print("***Run Independent***")
            solver = IndependentSolver(my_map, starts, agent_goals)
            paths = solver.find_solution()
        elif args.solver == "Prioritized":
            print("***Run Prioritized***")
            solver = PrioritizedPlanningSolver(my_map, starts, agent_goals)
            paths = solver.find_solution()
        else:
            raise RuntimeError("Unknown solver!")

        # Observer
        observer = SDObserver(my_map, paths, starts, goals)
        predictions = observer.elaborate_predictions()
        data_cruncher = DataCruncher(my_map, paths, starts, goals, agent_goals, predictions)
        entropy = data_cruncher.calculate_entropy()
        guess, metric_error = data_cruncher.calculate_guess_and_metric_error()

        cost = get_sum_of_cost(paths)
        solved_experiment = {
            "map": my_map,
            "starts": starts,
            "goals": goals,
            "agent_goals": agent_goals,
            "paths": paths,
            "predictions": predictions,
            "entropy": entropy,
            "guess": guess,
            "metric_error": metric_error,
            "cost": cost
        }

        simulation_result_filename = "solved-simulations/" + os.path.splitext(args.instance)[0] + "_" + args.solver.lower() + "_simulation.json"

        with open(simulation_result_filename , "w" ) as writefile:
            json.dump( solved_experiment , writefile )

        #if not args.batch:
            #print("***Test paths on a simulation***")
            #animation = Animation(my_map, starts, goals, paths, predictions)
            # animation.save("output.mp4", 1.0)
            #animation.show()
    writefile.close()
