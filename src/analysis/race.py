import matplotlib.pyplot as plt
import matplotlib
from analysis.base import _Base


class RaceAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.plot_race,
                            self.plot_race_v_min_sentence, self.plot_race_v_max_sentence]

    def plot_race(self):
        plt.figure()
        ax = self.df[['Defendant_Race', 'File_Number_Sequence']
                     ].drop_duplicates()['Defendant_Race'].value_counts().plot.bar()
        ax.set_title('Charges by Race: {0}'.format(self.drug))
        ax.set_ylabel('Count')
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        self.save_figure('race_distribution')

    def plot_race_v_min_sentence(self):
        ax = self.df[['Defendant_Race', 'Minimum_Sentence_Length_in_Days']
                     ].boxplot(grid=False, by='Defendant_Race')
        ax.set_title('')
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Race')
        ax.set_ylabel('Minimum Sentence Length (Days)')
        plt.title("Minimum Sentence Length by Race: {0}".format(self.drug))
        self.save_figure('race_v_min_sentence')

    def plot_race_v_max_sentence(self):
        ax = self.df[['Defendant_Race', 'Maximum_Sentence_Length_in_Days']
                     ].boxplot(grid=False, by='Defendant_Race')
        ax.set_title('')
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Race')
        ax.set_ylabel('Maximum Sentence Length (Days)')
        plt.title("Maximum Sentence Length by Race: {0}".format(self.drug))
        self.save_figure('race_v_max_sentence')
