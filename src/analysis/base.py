import os
import matplotlib.pyplot as plt
from functools import wraps

FIGURE_PATH = os.path.abspath(
    os.path.dirname(__file__)) + '/../../figures'


def community(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.sentence_type == 'Community':
            return f(self, *args, **kwargs)
        else:
            pass
    return wrapper


def intermediate(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.sentence_type == 'Intermediate':
            return f(self, *args, **kwargs)
        else:
            pass
    return wrapper


def active(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.sentence_type == 'Active':
            return f(self, *args, **kwargs)
        else:
            pass
    return wrapper


class _Base():

    from analysis.base import active, intermediate, community

    def __init__(self, df, drug_name, sentence_type):
        harshness_map = {'Active': 'Minimum_Sentence_Length_in_Days',
                         'Intermediate': 'Probation_in_Days',
                         'Community': 'Community_Service_Hours'}
        self.df = df
        self.drug = drug_name
        self.sentence_type = sentence_type
        self.harshness_measure = harshness_map.get(self.sentence_type)
        self.__methods__ = []

    def save_figure(self, filename):
        plt.savefig(
            FIGURE_PATH + '/{0}/{1}/{2}.png'.format(self.drug, self.sentence_type, filename), bbox_inches='tight', transparent=True)
        plt.close()

    def run(self):
        for method in self.__methods__:
            method()

    def get_punishment_name(self):
        return ' '.join(self.harshness_measure.split('_'))
