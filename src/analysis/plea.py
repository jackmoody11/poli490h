import matplotlib.pyplot as plt
from analysis import save_figure


def plea_analysis(df, drug_name):
    plot_plea_v_probation(df, drug_name)
    plot_plea_v_min_sentence(df, drug_name)
    plot_plea_v_max_sentence(df, drug_name)


def plot_plea_v_probation(df, drug_name):
    ax = df[['Probation_in_Days', 'Plea_Code']
            ].boxplot(grid=False, by='Plea_Code')
    ax.set_title('')
    plt.xticks(rotation=90)
    ax.get_figure().suptitle('')
    ax.set_xlabel('Plea Code')
    ax.set_ylabel('Probation (Days)')
    plt.title("Probation Length by Plea: {0}".format(drug_name))
    save_figure(drug_name, 'plea_form_v_probation')


def plot_plea_v_min_sentence(df, drug_name):
    ax = df[['Minimum_Sentence_Length_in_Days', 'Plea_Code']
            ].boxplot(grid=False, by='Plea_Code')
    ax.set_title('')
    plt.xticks(rotation=90)
    ax.get_figure().suptitle('')
    ax.set_xlabel('Plea Code')
    ax.set_ylabel('Minimum Sentence Length (Days)')
    plt.title("Minimum Sentence Length by Plea: {0}".format(drug_name))
    save_figure(drug_name, 'plea_form_v_min_sentence')


def plot_plea_v_max_sentence(df, drug_name):
    ax = df[['Maximum_Sentence_Length_in_Days', 'Plea_Code']
            ].boxplot(grid=False, by='Plea_Code')
    ax.set_title('')
    plt.xticks(rotation=90)
    ax.get_figure().suptitle('')
    ax.set_xlabel('Plea Code')
    ax.set_ylabel('Maximum Sentence Length (Days)')
    plt.title("Maximum Sentence Length by Plea: {0}".format(drug_name))
    save_figure(drug_name, 'plea_form_v_max_sentence')
