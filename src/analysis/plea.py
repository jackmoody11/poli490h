import matplotlib.pyplot as plt
from analysis.base import _Base


class PleaAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.df = self.df[~((self.df['Plea_Code'] == 'Not_Guilty') & (
            self.df['Verdict_Code'] == 'Not_Guilty'))]
        self.__methods__ = [self.plot_plea_v_probation,
                            self.plot_plea_v_min_sentence, self.plot_plea_v_max_sentence]

    @_Base.interemdiate
    def plot_plea_v_probation(self):
        ax = self.df[['Probation_in_Days', 'Plea_Code']
                     ].boxplot(grid=False, by='Plea_Code')
        ax.set_title('')
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Plea Code')
        ax.set_ylabel('Probation (Days)')
        plt.title("Probation Length by Plea: {0}".format(self.drug))
        self.save_figure('plea_form_v_probation')

    @_Base.active
    def plot_plea_v_min_sentence(self):
        ax = self.df[['Minimum_Sentence_Length_in_Days', 'Plea_Code']
                     ].boxplot(grid=False, by='Plea_Code')
        ax.set_title('')
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Plea Code')
        ax.set_ylabel('Minimum Sentence Length (Days)')
        plt.title("Minimum Sentence Length by Plea: {0}".format(self.drug))
        self.save_figure('plea_form_v_min_sentence')

    @_Base.active
    def plot_plea_v_max_sentence(self):
        ax = self.df[['Maximum_Sentence_Length_in_Days', 'Plea_Code']
                     ].boxplot(grid=False, by='Plea_Code')
        ax.set_title('')
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Plea Code')
        ax.set_ylabel('Maximum Sentence Length (Days)')
        plt.title("Maximum Sentence Length by Plea: {0}".format(self.drug))
        self.save_figure('plea_form_v_max_sentence')
