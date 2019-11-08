import pandas as pd
import geopandas as gpd
import os
from analysis import create_figures
from make_map import map_all

pd.options.mode.chained_assignment = None  # default='warn'


if __name__ == '__main__':
    data_path = os.path.dirname(os.path.realpath(
        __file__)) + '/../data'

    def read_offense_code(csv_file):
        return pd.read_csv(os.path.abspath(os.path.dirname(__file__)) + '/../data/offense_codes/{0}'.format(csv_file))

    marijuana_offense_codes = read_offense_code('marijuana.csv')['code']
    cocaine_offense_codes = read_offense_code('cocaine.csv')['code']
    heroin_offense_codes = read_offense_code('heroin.csv')['code']

    # Read in files and initial data frames, offense codes, and county codes
    # Be sure to change to 3drugs.csv
    us_counties = gpd.read_file(data_path + '/map/us_counties.json')
    nc_zip_codes = gpd.read_file(data_path + '/map/nc_zip_codes.json')
    nc_zip_codes['ZCTA5CE10'] = nc_zip_codes['ZCTA5CE10'].astype(int)

    # Clean data frame
    df = pd.read_csv('../data/cleaned/3drugs_cleaned.csv')
    # Limit to different types of drug offenses
    marijuana = df[df['Charged_Offense_Code'].isin(
        marijuana_offense_codes)]
    cocaine = df[df['Charged_Offense_Code'].isin(
        cocaine_offense_codes)]
    heroin = df[df['Charged_Offense_Code'].isin(heroin_offense_codes)]

    # Loop through analysis for each drug
    for drug_name, drug in {'marijuana': marijuana, 'cocaine': cocaine, 'heroin': heroin}.items():
        create_figures(drug, drug_name)
        map_all(drug, drug_name, nc_zip_codes, us_counties)
