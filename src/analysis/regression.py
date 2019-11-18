from analysis.base import _Base
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt


class RegressionAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.run_regression]

    def run_regression(self):
        for sentence_type, harshness_measure in (('Active', 'Minimum_Sentence_Length_in_Days'), ('Intermediate', 'Probation_in_Days'), ('Community', 'Community_Service_Hours')):
            if sentence_type == 'Community':
                _df = self.df[(self.df['Active_Sentence_Indicator'] == sentence_type) & (self.df['Minimum_Sentence_Length_in_Days'].isna())][[
                    harshness_measure, 'Age', 'Defendant_Race', 'County', 'Plea_Code', 'District_Court_Attorney_Type', 'Defendant_Sex_Code']].dropna(axis=0)
            else:
                _df = self.df[(self.df['Active_Sentence_Indicator'] == sentence_type)][[
                    harshness_measure, 'Age', 'Defendant_Race', 'County', 'Plea_Code', 'District_Court_Attorney_Type', 'Defendant_Sex_Code']].dropna(axis=0)
            y = _df[harshness_measure]
            X = pd.concat([_df['Age'], *[pd.get_dummies(_df[var]) for var in ('Defendant_Race',
                                                                              'County', 'Plea_Code', 'District_Court_Attorney_Type', 'Defendant_Sex_Code')]], axis=1)
            # Avoid numpy .ptp deprecation warning : https://stackoverflow.com/questions/56310898/futurewarning-method-ptp
            X = sm.add_constant(X.to_numpy())
            model = sm.OLS(y, X)
            results = model.fit()
            summary = results.summary()

            # plt.rc('figure', figsize=(12, 7))
            plt.text(0.01, 0.05, str(summary), {
                     'fontsize': 10}, fontproperties='monospace')
            plt.axis('off')
            self.save_figure('regression')
            # results_html = summary.tables[1].as_html()
            # coef_header = self.drug_name + '_' + sentence_type + '_coef'
            # p_value_header = self.drug_name + '_' + sentence_type + '_p_value'
            # series = pd.read_html(results_html, header=0, index_col=0)[0][[
            #     'coef', 'P>|t|']].rename({'coef': coef_header, 'P>|t|': p_value_header}, axis=1)
            # self.coefficients = pd.concat([coefficients, series], axis=1)
