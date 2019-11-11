import matplotlib.pyplot as plt
import matplotlib
from analysis import save_figure


def race_analysis(df, drug_name):
    plot_race(df, drug_name)
    plot_race_v_min_sentence(df, drug_name)
    plot_race_v_max_sentence(df, drug_name)


def plot_race(df, drug_name):
    plt.figure()
    ax = df[['Defendant_Race', 'File_Number_Sequence']
            ].drop_duplicates()['Defendant_Race'].value_counts().plot.bar()
    ax.set_title('Charges by Race: {0}'.format(drug_name))
    ax.set_ylabel('Count')
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    save_figure(drug_name, 'race_distribution')


def plot_race_v_min_sentence(df, drug_name):
    ax = df[['Defendant_Race', 'Minimum_Sentence_Length_in_Days']
            ].boxplot(grid=False, by='Defendant_Race')
    ax.set_title('')
    plt.xticks(rotation=90)
    ax.get_figure().suptitle('')
    ax.set_xlabel('Race')
    ax.set_ylabel('Minimum Sentence Length (Days)')
    plt.title("Minimum Sentence Length by Race: {0}".format(drug_name))
    save_figure(drug_name, 'race_v_min_sentence')


def plot_race_v_max_sentence(df, drug_name):
    ax = df[['Defendant_Race', 'Maximum_Sentence_Length_in_Days']
            ].boxplot(grid=False, by='Defendant_Race')
    ax.set_title('')
    plt.xticks(rotation=90)
    ax.get_figure().suptitle('')
    ax.set_xlabel('Race')
    ax.set_ylabel('Maximum Sentence Length (Days)')
    plt.title("Maximum Sentence Length by Race: {0}".format(drug_name))
    save_figure(drug_name, 'race_v_max_sentence')
