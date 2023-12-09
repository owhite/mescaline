#!/usr/bin/env python3

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class realTimePlot(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Baby Plotting Example')

        # Create Matplotlib figure and axis
        self.figure, self.axes = plt.subplots(2, 1, sharex=True)
        self.canvas = FigureCanvas(self.figure)

        # Create a timer for updating the plot
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.receive_data(1))

        # Initialize data
        self.x_data = np.arange(0, 10, 0.1)
        self.y1_data = np.zeros_like(self.x_data)
        self.y2_data = np.zeros_like(self.x_data)

        # Plot the initial data
        self.lines1, = self.axes[0].plot(self.x_data, self.y1_data, label='Data 1', color='blue')
        self.lines2, = self.axes[1].plot(self.x_data, self.y2_data, label='Data 2', color='green')

        self.axes[0].set_title('Vbat')
        self.axes[1].set_title('TMOT')

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Start the timer to update the plot every 100 milliseconds
        self.timer.start(100)

    def receive_data(self, d):
        p_y1 = np.random.random()
        p_y2 = np.random.random()
        self.update_plot(p_y1, p_y2)

    def update_plot(self, y1, y2):
        # Generate new data points
        y1 = np.random.random()
        y2 = np.random.random()

        # Shift existing data to the left
        self.y1_data = np.roll(self.y1_data, -1)
        self.y2_data = np.roll(self.y2_data, -1)

        # Append new data point
        self.y1_data[-1] = y1
        self.y2_data[-1] = y2

        # Update the plot data
        self.lines1.set_ydata(self.y1_data)
        self.lines2.set_ydata(self.y2_data)

        # Automatically adjust y-axis limits
        self.axes[0].relim()
        self.axes[1].relim()
        self.axes[0].autoscale()
        self.axes[1].autoscale()

        # Redraw the plot
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = realTimePlot()
    main_window.show()

    sys.exit(app.exec_())
