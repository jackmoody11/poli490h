import matplotlib.pyplot as plt
from analysis.base import _Base
import seaborn as sns


class AgeAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.plot_age,
                            self.plot_offenses_v_age,
                            self.plot_age_v_punishment,
                            self.plot_age_v_punishment_regression,
                            self.plot_age_v_punishment_quadratic_regression]

    def plot_age(self):
        plt.figure()
        ax = self.df[['Age', 'File_Number_Sequence']].drop_duplicates()[
            'Age'].hist()
        ax.set_title('Age Distribution: {0} Punishment, {1}'.format(
            self.sentence_type, self.drug))
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
        dependent = self.harshness_measure
        ax = self.df[[independent, dependent]].groupby(
            independent)[dependent].mean().plot(style='.')
        ax.set_title(
            'Average {0} Punishment by Age: {1}'.format(self.sentence_type, self.drug))
        ax.set_xlabel(independent)
        ax.set_ylabel(self.get_punishment_name())
        self.save_figure('age_v_punishment')

    def plot_age_v_punishment_regression(self):
        independent = 'Age'
        dependent = self.harshness_measure
        series = self.df[[independent, dependent]].groupby(
            independent)[dependent].mean()
        ax = sns.regplot(x=series.index.values, y=series.values)
        ax.set_xlabel('Age')
        ax.set_ylabel(self.get_punishment_name())
        ax.set_title('Age vs. Punishment: {0} {1} Punishment'.format(
            self.drug, self.sentence_type))
        self.save_figure('age_v_punishment_regression')

    def plot_age_v_punishment_quadratic_regression(self):
        independent = 'Age'
        dependent = self.harshness_measure
        series = self.df[[independent, dependent]].groupby(
            independent)[dependent].mean()
        ax = sns.regplot(x=series.index.values,
                         y=series.values, order=2)
        ax.set_xlabel('Age')
        ax.set_ylabel(self.get_punishment_name())
        ax.set_title('Age vs. Punishment: {0} {1} Punishment'.format(
            self.drug, self.sentence_type))
        self.save_figure('age_v_punishment_quadratic_regression')
