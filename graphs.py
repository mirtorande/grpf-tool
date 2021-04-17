#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Graphs:
    def __init__(self, entropy, entropy2, guess, metric_error):
        # prepare data
        df = pd.DataFrame({"entropy": entropy[0], "entropy2": entropy2[0], "guess": guess[0], "metric_error": metric_error[0]})
        #print(df)

        # prepare figure
        self.fig, self.axs = plt.subplots(2, 3, figsize=(10, 8)) #plt.figure(frameon=False, figsize=(8, 4))
        # 1
        x_axis = np.arange(0, len(df["entropy"]), 1)
        y_axis = df["entropy"]
        self.axs[0,0].bar(x = x_axis, height = y_axis)
        self.axs[0,0].set_xticks(x_axis)
        self.axs[0,0].set_title("Enthropy (nor. minmax)")

        # 2
        x_axis = np.arange(0, len(df["entropy2"]), 1)
        y_axis = df["entropy2"]
        self.axs[0,1].bar(x = x_axis, height = y_axis)
        self.axs[0,1].set_xticks(x_axis)
        self.axs[0,1].set_title("Enthropy (nor. sum)")

        # 3
        guesses = list(enumerate(df["guess"]))
        columns = ("Timestep", "Goal")
        #print(guesses)
        self.axs[0,2].table(cellText = guesses,
                            colLabels = columns,
                            loc='best'
                            )
        self.axs[0,2].set_title("Goal guesses")

        # 4
        x_axis = np.arange(0, len(df["metric_error"]), 1)
        y_axis = df["metric_error"]
        self.axs[1,0].bar(x = x_axis, height = y_axis)
        self.axs[1,0].set_xticks(x_axis)
        self.axs[1,0].set_title("Metric error")

        self.axs[0,2].axis('off')
        self.axs[1,2].axis('off')
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