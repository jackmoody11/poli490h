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
    df = pd.read_csv('../data/cleaned/3drugs_cleaned.zip', low_memory=False)
    # Limit to different types of drug offenses
    marijuana = df[df['Charged_Offense_Code'].isin(
        marijuana_offense_codes)]
    cocaine = df[df['Charged_Offense_Code'].isin(
        cocaine_offense_codes)]
    heroin = df[df['Charged_Offense_Code'].isin(heroin_offense_codes)]
    # Initialize coefficients data frame
    coefficients = pd.DataFrame()

    for drug_name, df in {'Marijuana': marijuana, 'Cocaine': cocaine, 'Heroin': heroin}.items():
        for sentence_type in ('Active', 'Intermediate', 'Community'):
            results = RegressionAnalysis(
                df, drug_name, sentence_type).get_results()
            series = get_significant_coefficients(
                results, drug_name, sentence_type)
            coefficients = pd.concat([coefficients, series], axis=1)
    # Only include county coefficients (should exclude WAKE)
    coefficients = coefficients[coefficients.index.isin(df['County'].unique())]
    coefficients.to_csv('../data/county_regressions.csv')
