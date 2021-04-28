#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Graphs:
    def __init__(self, entropy, metric_error):
        # prepare data
        df = pd.DataFrame({"entropy": entropy, "metric_error": metric_error})
        entropy = df["entropy"]
        #print(df)

        # prepare figure
        self.fig, self.axs = plt.subplots(1, 2, figsize=(10, 5)) #plt.figure(frameon=False, figsize=(8, 4))
        # 1
        x_axis = np.arange(0, len(entropy), 1)
        y_axis = entropy
        self.axs[0].bar(x = x_axis, height = y_axis)
        self.axs[0].set_xticks(np.arange(0, len(entropy), 2))
        self.axs[0].set_title("Enthropy")

        # 2
        x_axis = np.arange(0, len(df["metric_error"]), 1)
        y_axis = df["metric_error"]
        self.axs[1].bar(x = x_axis, height = y_axis)
        self.axs[1].set_xticks(np.arange(0, len(df["metric_error"]), 2))
        self.axs[1].set_title("Metric error")

        """
        # PRINT TABLE
        guesses = list(enumerate(df["guess"]))
        columns = ("Timestep", "Goal")
        #print(guesses)
        self.axs[0,1].table(cellText = guesses,
                            colLabels = columns,
                            loc='best'
                            )
        self.axs[0,1].set_title("Goal guesses")

        # 4
        self.axs[0,1].axis('off')
        self.axs[1,1].axis('off')"""

    def save(self, file_name):
        plt.savefig(
            file_name,
            dpi=200,
            pad_inches=0,
            bbox_inches="tight")

    @staticmethod
    def show():
        plt.show()