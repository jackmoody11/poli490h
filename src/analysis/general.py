from analysis.base import _Base
import matplotlib.pyplot as plt


class GeneralAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = []

    def plot_probation_length(self):
        plt.figure()
        ax = self.df['Probation_Length'].dropna().plot.hist()
        ax.set_title('Probation Length Distribution: {0}'.format(self.drug))
        ax.set_ylabel('Count')
        ax.set_xlabel('Probation Length (Days)')
        ax.grid(False)
        save_figure('probation_length')
