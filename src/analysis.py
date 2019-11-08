import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(path, '/../data')
# DRUG_OUTPUT_FILES = {k: data_path + '/' +
#                      k for k in ['marijuana', 'cocaine', 'heroin']}
FIGURE_PATH = os.path.abspath(
    os.path.dirname(__file__)) + '/../figures'


def create_figures(df, drug_name):
    plot_probation_length(df, drug_name)
    plot_age(df, drug_name)
    plot_race(df, drug_name)
    plot_offense_codes(df, drug_name)
    plot_offenses_v_age(df, drug_name)


def plot_probation_length(df, drug_name):
    plt.figure()
    ax = df['Probation_Length'].dropna().plot.hist()
    ax.set_title('Probation Length Distribution: {0}'.format(drug_name))
    ax.set_ylabel('Count')
    ax.set_xlabel('Probation Length (Days)')
    plt.savefig(
        FIGURE_PATH + '/{0}/probation_length.png'.format(drug_name), bbox_inches='tight')


def plot_age(df, drug_name):
    plt.figure()
    ax = df[['Age', 'File_Number_Sequence']].drop_duplicates()['Age'].hist()
    ax.set_title('Age Distribution: {0}'.format(drug_name))
    ax.set_ylabel('Count')
    ax.set_xlabel('Age (Years)')
    plt.savefig(
        FIGURE_PATH + '/{0}/age_distribution.png'.format(drug_name), bbox_inches='tight')


def plot_race(df, drug_name):
    plt.figure()
    ax = df[['Defendant_Race', 'File_Number_Sequence']
            ].drop_duplicates()['Defendant_Race'].value_counts().plot.bar()
    ax.set_title('Charges by Race: {0}'.format(drug_name))
    ax.set_ylabel('Count')
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.savefig(
        FIGURE_PATH + '/{0}/race_distribution.png'.format(drug_name), bbox_inches='tight')


def plot_offense_codes(df, drug_name):
    plt.figure()
    df['Charged_Offense_Code'] = df['Charged_Offense_Code'].dropna().astype(int)
    ax = df[['Charged_Offense_Code', 'File_Number_Sequence']
            ].drop_duplicates()['Charged_Offense_Code'].value_counts().plot.bar()
    ax.set_title('Offense Code Frequency: {0}'.format(drug_name))
    ax.set_ylabel('Count')
    plt.savefig(
        FIGURE_PATH + '/{0}/offense_code_distribution.png'.format(drug_name), bbox_inches='tight')


def plot_offenses_v_age(df, drug_name):
    plt.figure()
    ax = df[df['Age'] < 100].groupby(['File_Number_Sequence', 'Age']).size().reset_index().\
        rename(columns={0: 'File_Charges'}).drop_duplicates().groupby(
            'Age')['File_Charges'].mean().plot(style='.')
    ax.set_title('Number of Charges by Age')
    ax.set_xlabel('Age')
    ax.set_ylabel('Average Number of Charges')
    plt.savefig(
        FIGURE_PATH + '/{0}/average_offense_count_by_age.png'.format(drug_name), bbox_inches='tight')
