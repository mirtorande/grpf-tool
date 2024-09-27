# GRPF-Tool

GRPF-Tool is a Python-based tool designed for testing goal recognition algorithms within a pathfinding environment. This tool is useful for researchers and developers working on artificial intelligence and robotics, particularly in the field of pathfinding and goal recognition.

<img src="https://github.com/user-attachments/assets/b92d092f-439c-4cd5-8dae-176092e02964" width=400>

## Problem Statement

In many AI applications, understanding and predicting the goals of agents moving through an environment is crucial. This is particularly important in areas such as robotics, game development, and autonomous driving. The challenge lies in accurately recognizing the goal of an agent based on its observed behavior and movements, which can be complex and dynamic.

## Solution

GRPF-Tool addresses this problem by providing a testing environment for various goal recognition algorithms. By simulating different pathfinding scenarios, the tool allows users to:

- Test and compare the performance of different goal recognition algorithms.
- Analyze the accuracy and efficiency of these algorithms in various environments.
- Develop and refine new algorithms with the help of a controlled testing setup.

## Features

- **Pathfinding Simulation**: Simulates various pathfinding scenarios to test goal recognition algorithms.
- **Algorithm Comparison**: Allows comparison of different algorithms to determine their effectiveness.

## Installation

To install GRPF-Tool, you can clone the repository and install the required dependencies:

```bash
git clone https://github.com/mirtorande/grpf-tool.git
cd grpf-tool
pip install -r requirements.txt
```

## Usage

Here is a basic example of how to use GRPF-Tool:

```python
from grpf_tool import GoalRecognition

# Initialize the GoalRecognition environment
env = GoalRecognition()

# Define your pathfinding scenario
scenario = env.create_scenario()

# Run the goal recognition algorithm
result = env.run_algorithm(scenario)

# Analyze the result
print(result)
```

## License

This project is licensed under the CC0 License. See the [LICENSE](LICENSE) file for details.
