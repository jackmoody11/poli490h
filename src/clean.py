import pandas as pd
import numpy as np
import json


def date_parser(date):
    try:
        return pd.datetime.strptime(date, '%Y%m%d')
    except ValueError:
        return pd.NaT


if __name__ == '__main__':
    with open('../data/reference/county_codes.json', 'r') as f:
        county_codes = json.load(f)
    with open('../data/reference/fields.json', 'r') as f:
        fields = json.load(f)
    county_populations = pd.read_csv(
        '../data/reference/nc_counties_population.csv', index_col='County')['2018_Population'].to_dict()
    county_size = pd.read_csv(
        '../data/reference/nc_counties_population.csv', index_col='County')['2010_Square_Miles'].to_dict()
    date_columns = ['CRRRCD', 'CRRTDT', 'CROCDT', 'CRODTA', 'CRRDOB']
    df = pd.read_csv('../data/raw/3drugs.zip',
                     dtype={'CRRKCY': str, 'CRRRCD': str, 'CRRDTS': str}, parse_dates=date_columns, date_parser=date_parser, usecols=fields.keys())
    df = df.loc[:, fields.keys()]  # limit data frame to desired fields
    df.rename(columns=fields, inplace=True)
    df.replace({'.': np.nan}, inplace=True)

    # Change mappings to make more sense
    df['County'] = df['County_Number'].map(county_codes)
    df['Defendant_Race'] = df.loc[:, 'Defendant_Race_Code'].map(
        {'A': 'Asian', 'B': 'Black', 'H': 'Hispanic', 'I': 'Indian', 'O': 'Other',
         'U': 'Unknown', 'W': 'White', 'X': 'Non-person'})  # Create new column to map races
    plea_codes = {
        'GA': 'Guilty Alford Plea',
        'GL': 'Guilty to Lesser',
        'GU': 'Guilty',
        'NC': 'No Contest',
        'NG': 'Not Guilty',
        'NR': 'Not Responsible',
        'RL': 'Responsible to Lesser',
        'RS': 'Responsible'
    }
    df['Plea_Code'] = df.loc[:, 'Plea_Code'].map(plea_codes)
    verdict_codes = {
        'GL': 'Guilty to Lesser',
        'GU': 'Guilty',
        'JA': 'Judgment Arrested (By Judge after Jury Verdict)',
        'NG': 'Not Guilty',
        'NR': 'Not Responsible',
        'PJ': 'Prayer for Judgment',
        'RL': 'Responsible to Lesser',
        'RS': 'Responsible'
    }
    df['Verdict_Code'] = df.loc[:, 'Verdict_Code'].map(verdict_codes)
    df['Verdict_Code'] = df[df['Verdict_Code'] != 'Not Guilty']['Verdict_Code']
    df['Defendant_Sex_Code'] = df['Defendant_Sex_Code'].map({
        'M': 'Male',
        'F': 'Female',
        'U': 'Unknown',
        'X': 'Non-person'
    })
    # Condense year to one column
    df['Year'] = pd.to_datetime(
        df['File_Number_Century'] * 100 + df['File_Number_Year'], format='%Y')
    df.drop(['File_Number_Century', 'File_Number_Year'],
            inplace=True, axis=1)

    # Calculate age at filing date and set outliers to NaN
    df['Age'] = (df['Filing_Date'] -
                 df['Defendant_Date_of_Birth']).dt.days // 365
    df.loc[(df['Age'] <= 10) | (df['Age'] >= 90)] = np.nan

    # Change probation length to all be in terms of days - number may be a few days off because of simplification
    # that month is 30 days and year is 365 days
    df['Probation_Frame'].replace({'Y': 365, 'M': 30, 'D': 1}, inplace=True)
    df['Probation_Length'] = df['Probation_Length'].astype(float)
    df['Probation_in_Days'] = df['Probation_Frame'] * df['Probation_Length']

    # Code min and max sentences to days
    # NOTE: Drops life sentences, as we are only interested in less serious drug crimes (want to try to exclude those
    # which include some sort of homicide or more serious felony)
    df['Minimum_Sentence_Length_in_Days'] = df['Minimum_Sentence_Length'].astype(float) * \
        df['Minimum_Sentence_Frame'].map({
            'D': 1.0,
            'M': 30.0,
            'Y': 365.0,
            'L': 10_000.0,
            'X': 30_000.0,
            'P': 5_000.0,
            'F': 0.0
        })
    df['Minimum_Sentence_Length_in_Days'] = df[df['Minimum_Sentence_Length_in_Days']
                                               < 5000]['Minimum_Sentence_Length_in_Days']
    df['Maximum_Sentence_Length_in_Days'] = df['Maximum_Sentence_Length'].astype(float) * df['Maximum_Sentence_Frame'].map({
        'D': 1.0,
        'M': 30.0,
        'Y': 365.0
    })

    # Add mappings for attorney types
    attorney_mappings = {
        'A': 'Appointed',
        'P': 'Public Defender',
        'R': 'Privately Retained or Self',
        'W': 'Waived'
    }
    df['District_Court_Attorney_Type'] = df['District_Court_Attorney_Type'].map(
        attorney_mappings)
    df['Superior_Court_Attorney_Type'] = df['Superior_Court_Attorney_Type'].map(
        attorney_mappings)

    df['Active_Sentence_Indicator'] = df['Active_Sentence_Indicator'].map({
        'A': 'Active',
        'C': 'Community',
        'I': 'Intermediate'
    })
    # Add county population and size

    def assign_county_population(county):
        try:
            return county_populations[county]
        except KeyError:
            return np.nan

    def assign_county_size(county):
        try:
            return county_size[county]
        except KeyError:
            return np.nan

    df['County_Population'] = df['County'].apply(assign_county_population)
    df['County_Size_Square_Miles'] = df['County'].apply(assign_county_size)
    df['County_Population_Square_Mile'] = df['County_Population'] / \
        df['County_Size_Square_Miles']

    df.to_csv('../data/cleaned/3drugs_cleaned.zip',
              compression='zip', na_rep='N/A')
