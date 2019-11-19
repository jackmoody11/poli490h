import os
import matplotlib.pyplot as plt

FIGURE_PATH = os.path.abspath(
    os.path.dirname(__file__)) + '/../../figures'


class _Base():
    def __init__(self, df, drug_name, sentence_type):
        self.df = df
        self.drug = drug_name
        self.st = sentence_type
        self.__methods__ = []

    def save_figure(self, filename):
        plt.savefig(
            FIGURE_PATH + '/{0}/{1}/{2}.png'.format(self.drug, self.st, filename), bbox_inches='tight', transparent=True)
        plt.close()

    def run(self):
        for method in self.__methods__:
            try:
                method()
            except (TypeError, ValueError):
                pass
