import matplotlib.pyplot as plt
from analysis import save_figure


def age_analysis(df, drug_name):
    plot_age(df, drug_name)
    plot_offenses_v_age(df, drug_name)
    plot_age_v_avg_probation_length(df, drug_name)
    plot_age_v_avg_min_sentence_length(df, drug_name)
    plot_age_v_avg_max_sentence_length(df, drug_name)


def plot_age(df, drug_name):
    plt.figure()
    ax = df[['Age', 'File_Number_Sequence']].drop_duplicates()['Age'].hist()
    ax.set_title('Age Distribution: {0}'.format(drug_name))
    ax.set_ylabel('Count')
    ax.set_xlabel('Age (Years)')
    ax.grid(False)
    save_figure(drug_name, 'age_distribution')


def plot_offenses_v_age(df, drug_name):
    plt.figure()
    ax = df.groupby(['File_Number_Sequence', 'Age']).size().reset_index().\
        rename(columns={0: 'File_Charges'}).drop_duplicates().groupby(
            'Age')['File_Charges'].mean().plot(style='.')
    ax.set_title('Number of Charges by Age')
    ax.set_xlabel('Age')
    ax.set_ylabel('Average Number of Charges')
    save_figure(drug_name, 'average_offense_count_by_age')


def plot_age_v_avg_probation_length(df, drug_name):
    independent = 'Age'
    dependent = 'Probation_Length'
    ax = df[[independent, dependent]].groupby(
        independent)[dependent].mean().plot(style='.')
    ax.set_title(
        'Average Probation Length by Age: {0}'.format(drug_name))
    ax.set_xlabel(independent)
    ax.set_ylabel('Average Probation Length (Days)')
    save_figure(drug_name, 'age_v_avg_probation_length')


def plot_age_v_avg_min_sentence_length(df, drug_name):
    independent = 'Age'
    dependent = 'Minimum_Sentence_Length_in_Days'
    ax = df[[independent, dependent]].groupby(
        independent)[dependent].mean().plot(style='.')
    ax.set_title(
        'Average Minimum Sentence Length by Age: {0}'.format(drug_name))
    ax.set_xlabel(independent)
    ax.set_ylabel('Average Minimum Sentence Length (Days)')
    save_figure(drug_name, 'age_v_avg_min_sentence_length')


def plot_age_v_avg_max_sentence_length(df, drug_name):
    independent = 'Age'
    dependent = 'Maximum_Sentence_Length_in_Days'
    ax = df[[independent, dependent]].groupby(
        independent)[dependent].mean().plot(style='.')
    ax.set_title(
        'Average Maximum Sentence Length by Age: {0}'.format(drug_name))
    ax.set_xlabel(independent)
    ax.set_ylabel('Average Maximum Sentence Length (Days)')
    save_figure(drug_name, 'age_v_avg_max_sentence_length')
