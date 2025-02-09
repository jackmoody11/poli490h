import matplotlib.pyplot as plt
from analysis.base import _Base


class PleaAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.df = self.df[~((self.df['Plea_Code'] == 'Not_Guilty') & (
            self.df['Verdict_Code'] == 'Not_Guilty'))]
        self.__methods__ = [self.plot_plea_v_punishment,
                            self.plot_plea_v_punishment_no_outliers]

    def plot_plea_v_punishment(self):
        ax = self.df[[self.harshness_measure, 'Plea_Code']
                     ].boxplot(grid=False, by='Plea_Code')
        ax.set_title('')
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Plea Code')
        ax.set_ylabel(self.get_punishment_name())
        plt.title("{0} Punishment by Plea: {1}".format(
            self.sentence_type, self.drug))
        self.save_figure('plea_form_v_punishment')

    def plot_plea_v_punishment_no_outliers(self):
        ax = self.df[[self.harshness_measure, 'Plea_Code']
                     ].boxplot(grid=False, by='Plea_Code', showfliers=False)
        ax.set_title('')
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Plea Code')
        ax.set_ylabel(self.get_punishment_name())
        plt.title("{0} Punishment by Plea: {1} (No Outliers)".format(
            self.sentence_type, self.drug))
        self.save_figure('plea_form_v_punishment_no_outliers')
