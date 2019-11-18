from analysis.base import _Base


class CountyAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = []
