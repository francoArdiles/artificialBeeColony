import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

class Plotter:
    """
    Dibuja la búsqueda
    """

    def __init__(self, history):
        self.history = history

    def draw(self):
        plt.figure(1)
        plt.suptitle(self.history.name)
        plt.subplot(221)
        plt.title("Convergencia")
        plt.xlabel("iteracion")
        plt.ylabel("fitness")
        iterations = list(range(len(self.history.sols)))
        plt.plot(iterations, self.history.sols, marker='', color='green',
                 linewidth=1)
        plt.show()
