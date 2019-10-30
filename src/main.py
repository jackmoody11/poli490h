from matplotlib.ticker import FuncFormatter
import pandas as pd
import geopandas as gpd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import csv
import os
import sys
from dateutil.relativedelta import relativedelta
from analysis import analysis, create_figures
from clean import clean
from make_map import map_all

pd.options.mode.chained_assignment = None  # default='warn'


def date_parser(date):
    try:
        return pd.datetime.strptime(date, '%Y%m%d')
    except ValueError:
        return pd.NaT


# Read in files and initial data frames, offense codes, and county codes
date_columns = ['CRRRCD', 'CRRTDT', 'CROCDT', 'CRODTA', 'CRRDOB', ]
df = pd.read_csv('./data/3drugs.csv',
                 dtype={'CRRKCY': str, 'CRRRCD': str, 'CRRDTS': str}, parse_dates=date_columns, date_parser=date_parser)  # Be sure to change to 3drugs.csv
fields = pd.read_csv('./data/fields.csv', index_col='field')
marijuana_offense_codes = pd.read_csv(
    './data/offense_codes_marijuana.csv')['code'].tolist()
cocaine_offense_codes = pd.read_csv(
    './data/offense_codes_cocaine.csv')['code'].tolist()
heroin_offense_codes = pd.read_csv(
    './data/offense_codes_heroin.csv')['code'].tolist()
county_codes = pd.read_csv(
    './data/county_codes.csv', dtype={'code': str}).set_index('code')['county'].to_dict()
nc_zip_codes = gpd.read_file('./data/map/nc_zip_codes.json')

if __name__ == '__main':
    # Clean data frame
    df = clean(df, fields, county_codes)

    # Limit to different types of drug offenses
    marijuana = df[df['Charged_Offense_Code'].isin(marijuana_offense_codes)]
    cocaine = df[df['Charged_Offense_Code'].isin(cocaine_offense_codes)]
    heroin = df[df['Charged_Offense_Code'].isin(heroin_offense_codes)]

    # Loop through analysis for each drug
    for drug_name, drug in {'marijuana': marijuana, 'cocaine': cocaine, 'heroin': heroin}.items():
        analysis(drug)
        create_figures(drug, drug_name)
        map_all(drug, nc_zip_codes)
