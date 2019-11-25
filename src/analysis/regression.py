from analysis.base import _Base
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from analysis.utils import linear_regression, get_significant_coefficients


class RegressionAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        if self.sentence_type == 'Community':
            _df = self.df[(self.df['Active_Sentence_Indicator'] == self.sentence_type) & (
                self.df['Minimum_Sentence_Length_in_Days'].isna())]
        else:
            _df = self.df[(self.df['Active_Sentence_Indicator']
                           == self.sentence_type)]
        try:
            self._results = linear_regression(_df, self.harshness_measure, ['Age', 'Structured_Sentence_Prior_Record_Points'],
                                              'Defendant_Race', 'County', 'Plea_Code', 'District_Court_Attorney_Type', 'Defendant_Sex_Code')
        except ValueError:
            pass
        self.__methods__ = [self.print_regression]

    def print_regression(self):
        try:
            plt.text(0.01, 0.05, str(self._results.summary2()), {
                'fontsize': 10}, fontproperties='monospace')
            plt.axis('off')
            self.save_figure('regression')
        except (ValueError, AttributeError):
            pass

    def get_results(self):
        return self._results
