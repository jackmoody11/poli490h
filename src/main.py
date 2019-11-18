import pandas as pd
import geopandas as gpd
import os
from analysis.main import create_figures
from analysis.utils import linear_regression
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

    # Clean data frame
    df = pd.read_csv('../data/cleaned/3drugs_cleaned.csv', low_memory=False)
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

    # Linear regression results
    results = linear_regression(
        df, 'Minimum_Sentence_Length_in_Days', ['Age', 'County_Population'], 'Plea_Code', 'Defendant_Sex_Code', 'District_Court_Attorney_Type', 'Defendant_Race')
    plt.text(0.01, 0.05, str(results.summary2()), {
             'fontsize': 10}, fontproperties='monospace')
    plt.axis('off')
    save_figure('linear_regression')

    # Loop through analysis for each drug and sentence type
    for drug_name, df in {'marijuana': marijuana, 'cocaine': cocaine, 'heroin': heroin}.items():
        for sentence_type in ('Active', 'Intermediate', 'Community'):
            _df = df[df['Active_Sentence_Indicator'] == sentence_type]
            create_figures(_df, drug_name, sentence_type)
