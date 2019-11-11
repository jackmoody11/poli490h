import pandas as pd
import geopandas as gpd
import os
from analysis.main import create_figures
from make_map import map_all
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None  # default='warn'

FIGURE_PATH = os.path.abspath(
    os.path.dirname(__file__)) + '/../figures'


def save_figure(filename):
    plt.savefig(
        FIGURE_PATH + '/{0}.png'.format(filename), bbox_inches='tight', transparent=True)
    plt.close()


if __name__ == '__main__':
    data_path = os.path.dirname(os.path.realpath(
        __file__)) + '/../data'

    def read_offense_code(csv_file):
        return pd.read_csv(data_path + '/offense_codes/{0}'.format(csv_file))

    # Only use codes which correspond to possession
    marijuana_offense_codes = read_offense_code(
        'possession/marijuana.csv')['code']
    cocaine_offense_codes = read_offense_code('possession/cocaine.csv')['code']
    heroin_offense_codes = read_offense_code('possession/heroin.csv')['code']

    # Read in files and initial data frames, offense codes, and county codes
    # Be sure to change to 3drugs.csv
    # us_counties = gpd.read_file(data_path + '/map/us_counties.json')
    # nc_zip_codes = gpd.read_file(data_path + '/map/nc_zip_codes.json')
    # nc_zip_codes['ZCTA5CE10'] = nc_zip_codes['ZCTA5CE10'].astype(int)

    # Clean data frame
    df = pd.read_csv('../data/cleaned/3drugs_cleaned.csv')
    # Limit to different types of drug offenses
    marijuana = df[df['Charged_Offense_Code'].isin(
        marijuana_offense_codes)]
    cocaine = df[df['Charged_Offense_Code'].isin(
        cocaine_offense_codes)]
    heroin = df[df['Charged_Offense_Code'].isin(heroin_offense_codes)]

    # Age v. Min Sentence Length
    ax = df[['Age', 'Minimum_Sentence_Length_in_Days']].groupby(
        'Age')['Minimum_Sentence_Length_in_Days'].mean().plot(style='.')
    ax.set_title('Age v. Average Minimum Sentence')
    ax.set_xlabel('Age')
    ax.set_ylabel('Minimum Sentence Length (Days)')
    save_figure('composite_age_v_avg_min_sentence')

    # Min Sentence by Attorney Type
    ax = df[['District_Court_Attorney_Type', 'Minimum_Sentence_Length_in_Days']].boxplot(
        grid=False, by='District_Court_Attorney_Type', showfliers=False)
    ax.set_title(
        'Minimum Sentence Outcomes by Attorney Type: Composite')
    plt.xticks(rotation=45)
    ax.get_figure().suptitle('')
    ax.set_xlabel('Attorney Type (District Court)')
    ax.set_ylabel('Minimum Sentence Length (Days)')
    save_figure('composite_min_sentence_by_attorney_type')

    # Loop through analysis for each drug
    for drug_name, drug in {'marijuana': marijuana, 'cocaine': cocaine, 'heroin': heroin}.items():
        create_figures(drug, drug_name)
        # map_all(drug, drug_name, nc_zip_codes, us_counties)
