from matplotlib.ticker import FuncFormatter
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import csv
import os
import sys
from dateutil.relativedelta import relativedelta


def get_fields(field_file):
    with open(field_file, 'r') as f:
        return list(csv.reader(f))[0]  # assume only one line


# Read in files and initial data frames, offense codes, and county codes
df = pd.read_csv('./data/example_arrests.csv', dtype={'CRRKCY': str})
fields = pd.read_csv('./data/fields.csv', index_col='field')
marijuana_offense_codes = pd.read_csv(
    './data/offense_codes_marijuana.csv')['code'].tolist()
cocaine_offense_codes = pd.read_csv(
    './data/offense_codes_cocaine.csv')['code'].tolist()
heroin_offense_codes = pd.read_csv(
    './data/offense_codes_heroin.csv')['code'].tolist()
county_codes = pd.read_csv(
    './data/county_codes.csv', dtype={'code': str}).set_index('code')['county'].to_dict()

df = df[fields.index.tolist()]  # limit data frame to desired fields
df.rename(columns=fields['description'].to_dict(), inplace=True)
df = df.replace({'.': np.nan})
# Make new column with column names based on column numbers
df['County'] = df['County_Number'].map(county_codes)
df['Defendant_Race'] = df['Defendant_Race_Code'].map(
    {'A': 'Asian', 'B': 'Black', 'H': 'Hispanic', 'I': 'Indian', 'O': 'Other', 'U': 'Unknown', 'W': 'White', 'X': 'Non-person'})  # Create new column to map races
df['Probation_Length'].replace({'.': 0})
df['Filing_Date'] = pd.to_datetime(df['Filing_Date'])
df['Year'] = df['File_Number_Century'] * 100 + \
    df['File_Number_Year']  # Convert century and year to single column
df.drop(['File_Number_Century', 'File_Number_Year'],
        inplace=True, axis=1)  # Drop old columns
df['Defendant_Date_of_Birth'] = pd.to_datetime(
    df['Defendant_Date_of_Birth'], errors='coerce')
df['Age'] = (pd.to_datetime(df['Year'], format='%Y').dt.year -
             df['Defendant_Date_of_Birth'].dt.year)

# Limit to different types of drug offenses
marijuana = df[df['Charged_Offense_Code'].isin(marijuana_offense_codes)]
cocaine = df[df['Charged_Offense_Code'].isin(cocaine_offense_codes)]
heroin = df[df['Charged_Offense_Code'].isin(heroin_offense_codes)]

marijuana_race_offense_code = marijuana.groupby(
    ['Defendant_Race', 'Charged_Offense_Code']).count()['County'].unstack('Defendant_Race')
marijuana_offense_code_counts = marijuana_race_offense_code.T.sum()
marijuana_race_counts = marijuana_race_offense_code.sum()

marijuana_race_pct = marijuana_race_counts / marijuana_race_counts.sum()


marijuana['Probation_Frame'].replace(
    {'Y': 365, 'M': 30, 'D': 1, '.': np.nan}, inplace=True)
marijuana['Probation_Length'].replace({'.': np.nan}, inplace=True)

marijuana['Probation_Length'] = marijuana['Probation_Length'].replace({
                                                                      '.': np.nan})
marijuana['Probation_Length'] = marijuana['Probation_Length'].astype(float)

marijuana['Probation_Length'] = marijuana['Probation_Length'] * \
    marijuana['Probation_Frame']
marijuana_probation_length = marijuana['Probation_Length'].dropna()
