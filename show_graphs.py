#!/usr/bin/env python3
import argparse
from graphs import Graphs
import pandas as pd
import json

def jsonKeys2int(x):
    result = {}
    if isinstance(x, dict):
            for k,v in x.items():
                try:
                    as_int = int(k)
                    result[as_int] = v
                except ValueError:
                    result[k] = v
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualizes a simulation')
    parser.add_argument('--instance', type=str, default=None,
                        help='The name of the instance file(s)')
    args = parser.parse_args()

    with open( "solved-simulations/" + args.instance , "r" ) as readfile:
        data = json.load(readfile, object_hook=jsonKeys2int)
    
    print("***Showing graphs***")
    graphs = Graphs(data["entropy"])
    graphs.save("output/graphs.png")
    graphs.show()