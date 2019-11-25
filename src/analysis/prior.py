from analysis.base import _Base
import seaborn as sns


class PriorPointsAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.plot_prior_points_v_punishment]

    def plot_prior_points_v_punishment(self):
        independent = 'Structured_Sentence_Prior_Record_Points'
        dependent = self.harshness_measure
        series = self.df[[independent, dependent]].groupby(
            independent)[dependent].mean()
        ax = sns.regplot(x=series.index.values, y=series.values)
        ax.set_xlabel('Prior Points')
        ax.set_ylabel(self.get_punishment_name())
        ax.set_title('Prior Points vs. Punishment: {0} {1} Punishment'.format(
            self.drug, self.sentence_type))
        self.save_figure('prior_points_v_punishment')
