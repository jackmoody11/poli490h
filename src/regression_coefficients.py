from analysis.utils import linear_regression
from analysis.regression import RegressionAnalysis
from main import read_offense_code
import pandas as pd

if __name__ == '__main__':
    marijuana_offense_codes = read_offense_code(
        'possession/marijuana.csv')['code']
    cocaine_offense_codes = read_offense_code('possession/cocaine.csv')['code']
    heroin_offense_codes = read_offense_code('possession/heroin.csv')['code']

    # Clean data frame
    df = pd.read_csv('../data/cleaned/3drugs_cleaned.csv', low_memory=False)
    # Limit to different types of drug offenses
    marijuana = df[df['Charged_Offense_Code'].isin(
        marijuana_offense_codes)]
    cocaine = df[df['Charged_Offense_Code'].isin(
        cocaine_offense_codes)]
    heroin = df[df['Charged_Offense_Code'].isin(heroin_offense_codes)]
    # Initialize coefficients data frame
    coefficients = pd.DataFrame()

    for drug_name, df in {'marijuana': marijuana, 'cocaine': cocaine, 'heroin': heroin}.items():
        for sentence_type in ('Active', 'Intermediate', 'Community'):
            results = RegressionAnalysis(
                df, drug_name, sentence_type).get_results()
            summary = results.summary()
            results_html = summary.tables[1].as_html()
            coef_header = drug_name + '_' + sentence_type + '_coef'
            p_value_header = drug_name + '_' + sentence_type + '_p_value'
            series = pd.read_html(results_html, header=0, index_col=0)[0][[
                'coef', 'P>|t|']].rename({'coef': coef_header, 'P>|t|': p_value_header}, axis=1)
            series.drop_duplicates(inplace=True)
            coefficients = pd.concat([coefficients, series], axis=1)
    # Only include county coefficients (should exclude WAKE)
    coefficients = coefficients[coefficients.index.isin(df['County'].unique())]
    coefficients.to_csv('../data/county_regressions.csv')
