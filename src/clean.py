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

    date_columns = ['CRRRCD', 'CRRTDT', 'CROCDT', 'CRODTA', 'CRRDOB']
    df = pd.read_csv('../data/raw/3drugs.csv',
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

    df.to_csv('../data/cleaned/3drugs_cleaned.csv', na_rep='N/A')
