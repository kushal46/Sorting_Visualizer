import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Plotter:
    def __init__(self, arr, interval=1000, title="Bubble Sort", *, 
                 repeat=0, window_shape=(7,5), xkcd=0):
        self.is_xkcd = xkcd
        self.arr = arr  # The array at different steps of sorting
        self.title = title
        self.window_shape = window_shape
        self.interval = interval
        self.repeat = repeat
        self.x = np.arange(start=0, stop=arr.shape[1])  # x-axis (indices of the array)
        self.colors = ['b'] * arr.shape[1]  # Initial color for all bars is blue ('b')
        self.bar_collections = None  # To hold the bar collection

    @staticmethod
    def on_close(event):
        if not sys.argv[0] == 'test.py':
            sys.exit(0)

    def animate(self, at):
        # Adjust the height of each bar to the current step's array
        for i in range(len(self.bar_collections)):
            self.bar_collections[i].set_height(self.arr[at][i])
            self.bar_collections[i].set_color(self.colors[i])  # Update the bar color
        self.update_colors(at)  # Update colors for the current frame

    def update_colors(self, at):
        """
        Update the color array based on which elements are being swapped, compared, or sorted.
        This is a basic approach and can be customized based on sorting algorithm.
        """
        self.colors = ['b'] * len(self.arr[at])  # Reset all colors to blue (default)

        if at < len(self.arr) - 1:
            # Highlight swapped elements in red
            for i in range(len(self.arr[at])):
                if self.arr[at][i] != self.arr[at + 1][i]:
                    self.colors[i] = 'r'  # Mark swapped elements as red

        # Optional: Color the array green when the sorting is complete
        if at == len(self.arr) - 1:  # Final step
            self.colors = ['g'] * len(self.arr[at])  # Mark all elements green (sorted)

    def plot_util(self):
        self.fig, self.graph = plt.subplots(figsize=self.window_shape)
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.graph.yaxis.set_visible(False)
        self.graph.xaxis.set_visible(False)

        self.graph.text(0, 1.15, self.title, transform=self.graph.transAxes,
                        size=24, weight=300, ha='left', va='top')

        self.bar_collections = self.graph.bar(self.x, self.arr[0], align='edge', width=0.5)

        # Animate the plot with updated heights and colors
        anim = FuncAnimation(self.fig, self.animate, frames=len(self.arr), 
                             interval=self.interval, blit=False, repeat=self.repeat,
                             repeat_delay=1000)

        plt.box(False)
        time.sleep(1)
        plt.show()
        anim.event_source.stop()
        del anim
        plt.close()

    def plot(self):
        try:
            if self.is_xkcd:
                with plt.xkcd():
                    self.plot_util()
            else:
                self.plot_util()
        except:
            pass
