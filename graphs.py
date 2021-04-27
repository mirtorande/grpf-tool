#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Graphs:
    def __init__(self, entropy, guess, metric_error):
        # prepare data
        df = pd.DataFrame({"entropy": entropy[0], "guess": guess[0], "metric_error": metric_error[0]})
        #print(df)

        # prepare figure
        self.fig, self.axs = plt.subplots(2, 2, figsize=(10, 8)) #plt.figure(frameon=False, figsize=(8, 4))
        # 1
        x_axis = np.arange(0, len(df["entropy"]), 1)
        y_axis = df["entropy"]
        self.axs[0,0].bar(x = x_axis, height = y_axis)
        self.axs[0,0].set_xticks(np.arange(0, len(df["entropy"]), 5))
        self.axs[0,0].set_title("Enthropy (nor. minmax)")

        # 2
        x_axis = np.arange(0, len(df["metric_error"]), 1)
        y_axis = df["metric_error"]
        self.axs[1,0].bar(x = x_axis, height = y_axis)
        self.axs[1,0].set_xticks(np.arange(0, len(df["metric_error"]), 5))
        self.axs[1,0].set_title("Metric error")

        # 3
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
        self.axs[1,1].axis('off')

    def save(self, file_name):
        plt.savefig(
            file_name,
            dpi=200,
            pad_inches=0,
            bbox_inches="tight")

    @staticmethod
    def show():
        plt.show()