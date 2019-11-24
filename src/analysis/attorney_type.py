import matplotlib.pyplot as plt
from analysis.base import _Base


class AttorneyAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.plot_punishment_by_attorney_type]

    def plot_punishment_by_attorney_type(self):
        ax = self.df[['District_Court_Attorney_Type', self.harshness_measure]].boxplot(
            grid=False, by='District_Court_Attorney_Type', showfliers=False)
        ax.set_title(
            '{0} Punishment Outcomes by Attorney Type: {1}'.format(self.sentence_type, self.drug))
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Attorney Type (District Court)')
        ax.set_ylabel(self.get_punishment_name())
        self.save_figure('punishment_by_attorney_type')
