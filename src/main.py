import pandas as pd
import geopandas as gpd
import os
from analysis.main import create_figures
from analysis.utils import linear_regression
from make_map import map_all
import matplotlib.pyplot as plt
from tqdm import tqdm

pd.options.mode.chained_assignment = None  # default='warn'

FIGURE_PATH = os.path.abspath(
    os.path.dirname(__file__)) + '/../figures'


def save_figure(filename):
    plt.savefig(
        FIGURE_PATH + '/{0}.png'.format(filename), bbox_inches='tight', transparent=True)
    plt.close()


def read_offense_code(csv_file):
    data_path = os.path.dirname(os.path.realpath(
        __file__)) + '/../data'
    return pd.read_csv(data_path + '/offense_codes/possession/{0}'.format(csv_file))


if __name__ == '__main__':
    marijuana_offense_codes = read_offense_code(
        'marijuana.csv')['code']
    cocaine_offense_codes = read_offense_code('cocaine.csv')['code']
    heroin_offense_codes = read_offense_code('heroin.csv')['code']

    df = pd.read_csv('../data/cleaned/3drugs_cleaned.zip', low_memory=False)

    marijuana = df[df['Charged_Offense_Code'].isin(
        marijuana_offense_codes)]
    cocaine = df[df['Charged_Offense_Code'].isin(
        cocaine_offense_codes)]
    heroin = df[df['Charged_Offense_Code'].isin(heroin_offense_codes)]

    for drug_name, df in tqdm({'Marijuana': marijuana, 'Cocaine': cocaine, 'Heroin': heroin}.items()):
        for sentence_type in ('Active', 'Intermediate', 'Community'):
            _df = df[df['Active_Sentence_Indicator'] == sentence_type]
            create_figures(_df, drug_name, sentence_type)
