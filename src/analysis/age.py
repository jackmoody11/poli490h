import matplotlib.pyplot as plt
from analysis.base import _Base


class AgeAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.plot_age,
                            self.plot_offenses_v_age, self.plot_age_v_punishment]

    def plot_age(self):
        plt.figure()
        ax = self.df[['Age', 'File_Number_Sequence']].drop_duplicates()[
            'Age'].hist()
        ax.set_title('Age Distribution: {0}'.format(self.drug))
        ax.set_ylabel('Count')
        ax.set_xlabel('Age (Years)')
        ax.grid(False)
        self.save_figure('age_distribution')

    def plot_offenses_v_age(self):
        plt.figure()
        ax = self.df.groupby(['File_Number_Sequence', 'Age']).size().reset_index().\
            rename(columns={0: 'File_Charges'}).drop_duplicates().groupby(
                'Age')['File_Charges'].mean().plot(style='.')
        ax.set_title('Number of Charges by Age')
        ax.set_xlabel('Age')
        ax.set_ylabel('Average Number of Charges')
        self.save_figure('average_offense_count_by_age')

    def plot_age_v_punishment(self):
        independent = 'Age'
        dependent = self.harshness_measure[self.st]
        ax = self.df[[independent, dependent]].groupby(
            independent)[dependent].mean().plot(style='.')
        ax.set_title(
            'Average {0} Punishment by Age: {1}'.format(self.st, self.drug))
        ax.set_xlabel(independent)
        ax.set_ylabel(' '.join(self.harshness_measure[self.st].split('_')))
        self.save_figure('age_v_punishment')
