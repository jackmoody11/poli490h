import matplotlib.pyplot as plt
from analysis.base import _Base


class AgeAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.plot_age, self.plot_offenses_v_age, self.plot_age_v_avg_probation_length,
                            self.plot_age_v_avg_min_sentence_length, self.plot_age_v_avg_max_sentence_length]

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

    @_Base.intermediate
    def plot_age_v_avg_probation_length(self):
        independent = 'Age'
        dependent = 'Probation_Length'
        ax = self.df[[independent, dependent]].groupby(
            independent)[dependent].mean().plot(style='.')
        ax.set_title(
            'Average Probation Length by Age: {0}'.format(self.drug))
        ax.set_xlabel(independent)
        ax.set_ylabel('Average Probation Length (Days)')
        self.save_figure('age_v_avg_probation_length')

    @_Base.active
    def plot_age_v_avg_min_sentence_length(self):
        independent = 'Age'
        dependent = 'Minimum_Sentence_Length_in_Days'
        ax = self.df[[independent, dependent]].groupby(
            independent)[dependent].mean().plot(style='.')
        ax.set_title(
            'Average Minimum Sentence Length by Age: {0}'.format(self.drug))
        ax.set_xlabel(independent)
        ax.set_ylabel('Average Minimum Sentence Length (Days)')
        self.save_figure('age_v_avg_min_sentence_length')

    # @_Base.community(self.st)
    # def plot_age_v_community_service(self):
    @_Base.active
    def plot_age_v_avg_max_sentence_length(self):
        independent = 'Age'
        dependent = 'Maximum_Sentence_Length_in_Days'
        ax = self.df[[independent, dependent]].groupby(
            independent)[dependent].mean().plot(style='.')
        ax.set_title(
            'Average Maximum Sentence Length by Age: {0}'.format(self.drug))
        ax.set_xlabel(independent)
        ax.set_ylabel('Average Maximum Sentence Length (Days)')
        self.save_figure('age_v_avg_max_sentence_length')
