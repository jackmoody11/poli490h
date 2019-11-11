import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
from analysis import FIGURE_PATH, save_figure
from analysis.age import age_analysis
from analysis.attorney_type import attorney_type_analysis
from analysis.county import county_analysis
from analysis.gender import gender_analysis
from analysis.plea import plea_analysis
from analysis.race import race_analysis


path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(path, '/../../data')


def create_figures(df, drug_name):
    # One off analyses
    plot_probation_length(df, drug_name)

    # Run analyses
    age_analysis(df, drug_name)
    attorney_type_analysis(df, drug_name)
    county_analysis(df, drug_name)
    gender_analysis(df, drug_name)
    plea_analysis(df, drug_name)
    race_analysis(df, drug_name)


def plot_probation_length(df, drug_name):
    plt.figure()
    ax = df['Probation_Length'].dropna().plot.hist()
    ax.set_title('Probation Length Distribution: {0}'.format(drug_name))
    ax.set_ylabel('Count')
    ax.set_xlabel('Probation Length (Days)')
    ax.grid(False)
    save_figure(drug_name, 'probation_length')
