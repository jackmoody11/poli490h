from analysis.base import _Base
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from analysis.utils import linear_regression


class RegressionAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.run_regression]

    def run_regression(self):
        harshness_measure = {'Active': 'Minimum_Sentence_Length_in_Days',
                             'Intermediate': 'Probation_in_Days',
                             'Community': 'Community_Service_Hours'}
        if self.st == 'Community':
            _df = self.df[(self.df['Active_Sentence_Indicator'] == self.st) & (
                self.df['Minimum_Sentence_Length_in_Days'].isna())]
        else:
            _df = self.df[(self.df['Active_Sentence_Indicator']
                           == self.st)]

        results = linear_regression(_df, harshness_measure[self.st], ['Age'], [
                                    'Defendant_Race', 'County', 'Plea_Code', 'District_Court_Attorney_Type', 'Defendant_Sex_Code'])
        plt.text(0.01, 0.05, str(results.summary2()), {
            'fontsize': 10}, fontproperties='monospace')
        plt.axis('off')
        self.save_figure('regression')
