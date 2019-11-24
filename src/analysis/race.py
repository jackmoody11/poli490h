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
        ax = self.df[['Defendant_Race', self.harshness_measure]
                     ].boxplot(grid=False, by='Defendant_Race')
        ax.set_title('')
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Race')
        ax.set_ylabel(self.get_punishment_name())
        plt.title("{0} Punishment by Race: {1}".format(
            self.sentence_type, self.drug))
        self.save_figure('race_v_punishment')

    def plot_race_v_punishment_no_outliers(self):
        ax = self.df[['Defendant_Race', self.harshness_measure]
                     ].boxplot(grid=False, by='Defendant_Race', showfliers=False)
        ax.set_title('')
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Race')
        ax.set_ylabel(self.get_punishment_name())
        plt.title("{0} Punishment by Race: {1} (No Outliers)".format(
            self.sentence_type, self.drug))
        self.save_figure('race_v_punishment_no_outliers')
