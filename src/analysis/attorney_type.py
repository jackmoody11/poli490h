import matplotlib.pyplot as plt
from analysis.base import _Base


class AttorneyAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.plot_min_sentence_by_attorney_type]

    def attorney_type_analysis(self):
        plot_min_sentence_by_attorney_type(df, drug_name)

    @_Base.active
    def plot_min_sentence_by_attorney_type(self):
        ax = self.df[['District_Court_Attorney_Type', 'Minimum_Sentence_Length_in_Days']].boxplot(
            grid=False, by='District_Court_Attorney_Type', showfliers=False)
        ax.set_title(
            'Minimum Sentence Outcomes by Attorney Type: {0}'.format(self.drug))
        plt.xticks(rotation=90)
        ax.get_figure().suptitle('')
        ax.set_xlabel('Attorney Type (District Court)')
        ax.set_ylabel('Minimum Sentence Length (Days)')
        self.save_figure('min_sentence_by_attorney_type')
