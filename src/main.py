import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import csv


def get_fields(field_file):
    with open(field_file, 'r') as f:
        return list(csv.reader(f))[0]  # assume only one line


def fix_birthdays(x):
    try:
        return datetime.datetime.strptime(x, '%Y%m%d')
    except (ValueError, TypeError):
        return pd.NaT


if __name__ == "__main__":
    # Define variables
    df = pd.read_csv('../data/example_arrests.csv', dtype={'CRRKCY': str})
    fields = pd.read_csv('../data/fields.csv', index_col='field')
    marijuana_offense_codes = pd.read_csv(
        '../data/offense_codes_marijuana.csv')['code'].tolist()
    cocaine_offense_codes = pd.read_csv(
        '../data/offense_codes_cocaine.csv')['code'].tolist()
    heroin_offense_codes = pd.read_csv(
        '../data/offense_codes_heroin.csv')['code'].tolist()
    county_codes = pd.read_csv(
        '../data/county_codes.csv', dtype={'code': str}).set_index('code')['county'].to_dict()

    df = df[fields.index.tolist()]  # limit data frame to desired fields
    df.rename(columns=fields['description'].to_dict(), inplace=True)
    df['County'] = df['County_Number'].map(county_codes)

    # Limit to different types of drug offenses
    marijuana = df[df['CROFFC'].isin(marijuana_offense_codes)]
    cocaine = df[df['CROFFC'].isin(cocaine_offense_codes)]
    heroin = df[df['CROFFC'].isin(heroin_offense_codes)]

    # Replace . with NaN
    # df.replace({'.': np.nan}, inplace=True)

    # Fix DOB format
    # df['CRRDOB'] = df['CRRDOB'].apply(lambda x: fix_birthdays(x))

    # # Histogram of race
    # df['CRRACE'].hist()

    # # Histogram of sex
    # df['CRRSEX'].hist()

    # # Histogram of home state
    # df['CRRDST'].hist()

    # # Histogram of defendant age
    # df['CRRAGE'].hist()

    # # Histogram of DOB
    # df['CRRDOB'].hist()

    # # Histogram of offense codes
    # df['CROFFC'].hist(bins=100)

    # plt.show()
