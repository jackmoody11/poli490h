import os
import matplotlib.pyplot as plt
from functools import wraps

FIGURE_PATH = os.path.abspath(
    os.path.dirname(__file__)) + '/../../figures'


def community(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.st == 'Community':
            return f
        else:
            pass
    return wrapper


def intermediate(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.st == 'Intermediate':
            return f
        else:
            pass
    return wrapper


def active(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.st == 'Active':
            return f
        else:
            pass
    return wrapper


class _Base():
    from analysis.base import active, intermediate, community

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
            method()
