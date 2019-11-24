import matplotlib.pyplot as plt
import matplotlib
from analysis.base import _Base


class RaceAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.plot_race, self.plot_race_v_punishment]

    def plot_race(self):
        ax = self.df[['Defendant_Race', 'File_Number_Sequence']
                     ].drop_duplicates()['Defendant_Race'].value_counts().plot.bar()
        ax.set_title('Charges by Race: {0}'.format(self.drug))
        ax.set_ylabel('Count')
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        self.save_figure('race_distribution')

    def plot_race_v_punishment(self):
        ax = self.df[['Defendant_Race', self.harshness_measure[self.st]]
                     ].boxplot(grid=False, by='Defendant_Race')
        ax.set_title('')
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Race')
        ax.set_ylabel(' '.join(self.harshness_measure[self.st].split('_')))
        plt.title("{0} Punishment by Race: {1}".format(self.st, self.drug))
        self.save_figure('race_v_punishment')
