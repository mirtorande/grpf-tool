#!/usr/bin/env python3
from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from math import floor

Colors = ['green', 'blue', 'orange']


class Animation:
    def __init__(self, my_map, start, goals, path, predictions):
        self.my_map = np.flip(np.transpose(my_map), 1)
        self.start = start
        self.goals = []
        self.predictions = predictions
        for goal in goals:
            self.goals.append((goal[1], len(self.my_map[0]) - 1 - goal[0]))
        self.path = []
        for loc in path:
            self.path.append((loc[1], len(self.my_map[0]) - 1 - loc[0]))

        aspect = len(self.my_map) / len(self.my_map[0])

        self.fig = plt.figure(frameon=False, figsize=(4 * aspect, 4))
        self.ax = self.fig.add_subplot(111, aspect='equal')
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=None, hspace=None)
        # self.ax.set_frame_on(False)

        self.patches = []
        self.artists = []
        self.goal_predictions = dict()
        # create boundary patch

        x_min = -0.5
        y_min = -0.5
        x_max = len(self.my_map) - 0.5
        y_max = len(self.my_map[0]) - 0.5
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)

        self.patches.append(Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, facecolor='none', edgecolor='gray'))
        for i in range(len(self.my_map)):
            for j in range(len(self.my_map[0])):
                if self.my_map[i][j]:
                    self.patches.append(Rectangle((i - 0.5, j - 0.5), 1, 1, facecolor='gray', edgecolor='gray'))

        # create agent and goals:
        self.T = 0
        for i, goal in enumerate(self.goals):
            self.patches.append(Rectangle((goal[0] - 0.25, goal[1] - 0.25), 0.5, 0.5, facecolor=Colors[i % len(Colors)],
                                          edgecolor='black', alpha=0.5))
            self.goal_predictions[i] = self.ax.text(self.goals[i][0], self.goals[i][1], str(i))
            self.goal_predictions[i].set_horizontalalignment('center')
            self.goal_predictions[i].set_verticalalignment('center')
            self.artists.append(self.goal_predictions[i])

        name = "agent"
        self.agent = Circle((start[0], start[1]), 0.3, facecolor=Colors[i % len(Colors)],
                                edgecolor='black')
        self.agent.original_face_color = Colors[i % len(Colors)]
        self.patches.append(self.agent)
        self.T = len(path) - 1
        self.agent_name = self.ax.text(start[0], start[1] + 0.25, name)
        self.agent_name.set_horizontalalignment('center')
        self.agent_name.set_verticalalignment('center')
        self.artists.append(self.agent_name)

        self.animation = animation.FuncAnimation(self.fig, self.animate_func,
                                                 init_func=self.init_func,
                                                 frames=int(self.T + 1) * 10,
                                                 interval=100,
                                                 blit=True)

    def save(self, file_name, speed):
        self.animation.save(
            file_name,
            fps=10 * speed,
            dpi=200,
            savefig_kwargs={"pad_inches": 0, "bbox_inches": "tight"})

    @staticmethod
    def show():
        plt.show()

    def init_func(self):
        for p in self.patches:
            self.ax.add_patch(p)
        for a in self.artists:
            self.ax.add_artist(a)
        return self.patches + self.artists

    # Animation
    def animate_func(self, t):
        pos = self.get_state(t / 10, self.path)
        self.agent.center = (pos[0], pos[1])
        self.agent_name.set_position((pos[0], pos[1] + 0.5))

        for i in self.goal_predictions:
            self.goal_predictions[i].set_text("{:.2f}".format(self.predictions[floor(t/10)][i]*100))

        return self.patches + self.artists

    @staticmethod
    def get_state(t, path):
        if int(t) <= 0:
            return np.array(path[0])
        elif int(t) >= len(path):
            return np.array(path[-1])
        else:
            pos_last = np.array(path[int(t) - 1])
            pos_next = np.array(path[int(t)])
            pos = (pos_next - pos_last) * (t - int(t)) + pos_last
            return pos
