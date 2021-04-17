#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Graphs:
    def __init__(self, entropy):

        self.fig = plt.figure(frameon=False, figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        entropy_series = pd.Series(entropy)
        x_axis = np.arange(0, len(entropy)-1, 1)
        index_pos = [entropy_series.index.get_loc(y) for y in x_axis]
        entropy_series.plot.bar()
        plt.xticks(index_pos, x_axis)
        plt.title("Enthropy trend")

    def save(self, file_name):
        plt.savefig(
            file_name,
            dpi=200,
            pad_inches=0,
            bbox_inches="tight")

    @staticmethod
    def show():
        plt.show()