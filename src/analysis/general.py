from analysis.base import _Base
import matplotlib.pyplot as plt


class GeneralAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.plot_punishment]

    def plot_punishment(self):
        plt.figure()
        ax = self.df[self.harshness_measure[self.st]].dropna().plot.hist()
        ax.set_title(
            '{0} Punishment Distribution: {1}'.format(self.st, self.drug))
        ax.set_ylabel('Count')
        ax.set_xlabel(' '.join(self.harshness_measure[self.st].split('_')))
        ax.grid(False)
        self.save_figure('punishment')
