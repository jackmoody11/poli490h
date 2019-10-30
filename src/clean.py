import pandas as pd
import numpy as np
import csv


def get_fields(field_file):
    with open(field_file, 'r') as f:
        return list(csv.reader(f))[0]  # assume only one line


def clean(df, fields, county_codes):
    df = df[fields.index.tolist()]  # limit data frame to desired fields
    df.rename(columns=fields['description'].to_dict(), inplace=True)
    df.replace({'.': np.nan}, inplace=True)

    df['County'] = df['County_Number'].map(county_codes)
    df['Defendant_Race'] = df['Defendant_Race_Code'].map(
        {'A': 'Asian', 'B': 'Black', 'H': 'Hispanic', 'I': 'Indian', 'O': 'Other', 'U': 'Unknown', 'W': 'White', 'X': 'Non-person'})  # Create new column to map races
    df['Probation_Length'].replace({'.': 0})

    # Condense year to one column
    df['Year'] = pd.to_datetime(
        df['File_Number_Century'] * 100 + df['File_Number_Year'], format='%Y')
    df.drop(['File_Number_Century', 'File_Number_Year'],
            inplace=True, axis=1)

    # Calculate age at filing date
    df['Age'] = (df['Filing_Date'] -
                 df['Defendant_Date_of_Birth']).dt.days // 365
    df[df['Age'] <= 0] = np.nan

    # Change probation length to all be in terms of days - number may be a few days off because of simplification
    # that month is 30 days and year is 365 days
    df['Probation_Frame'].replace(
        {'Y': 365, 'M': 30, 'D': 1, '.': np.nan}, inplace=True)
    df['Probation_Length'] = df['Probation_Length'].replace(
        {'.': np.nan}).astype(float) * df['Probation_Frame']
    return df
