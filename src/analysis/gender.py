import matplotlib.pyplot as plt
import matplotlib
from analysis.base import _Base


class GenderAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.gender_distribution]

    def gender_distribution(self):
        ax = self.df[['Defendant_Sex_Code', 'File_Number_Sequence']
                     ].drop_duplicates()['Defendant_Sex_Code'].value_counts().plot.bar()
        ax.set_title('Charges by Sex: {0} Punishment, {1}'.format(
            self.sentence_type, self.drug))
        ax.set_ylabel('Count')
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        self.save_figure('sex_distribution')
