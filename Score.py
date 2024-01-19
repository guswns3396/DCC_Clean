# class Runner:
#     """
#     Takes in an instance of Scorer and runs its pipeline
#     """
#     def __init__(self, scorer):
#         self.scorer = scorer
#
#     def run(self, **kwargs):
#         # verify range
#         self.scorer.verify_range()
#         # verify number of columns
#         self.scorer.verify_cols()
#         # add missing
#         if self.scorer.include_missing:
#             self.scorer.add_missing()
#         self.scorer.score(**kwargs)
#         return self.scorer.df


class Scorer:
    """
    Scorer base class
    """
    def __init__(self, df, col_name, include_missing):
        """
        Constructor
        :param df: df to score containing only columns for scoring
        :param col_name: common column name
        :param include_missing: whether to include % missing for score
        """
        self.df = df.copy()
        self.original_cols = df.columns
        self.col_name = col_name
        self.include_missing = include_missing

    def score(self):
        raise NotImplementedError

    def verify_cols(self):
        raise NotImplementedError

    def verify_range(self):
        raise NotImplementedError

    def add_missing(self):
        raise NotImplementedError


class PvsARFIDScorer(Scorer):
    def __init__(self, df, col_name, include_missing=True):
        super().__init__(df, col_name, include_missing)

    def verify_cols(self):
        assert len(self.df.columns) == 7

    def verify_range(self):
        assert (self.df.isin(range(1, 6)) | self.df.isna()).all(axis=None)

    def score(self, reverse_coded):
        df = self.df
        cols = self.original_cols
        col_name = self.col_name
        if reverse_coded:
            reverse_idx = [x - 1 for x in [1, 2, 4, 6]]
            reverse_code = {i: 6 - i for i in range(1, 6)}
            df.loc[:, cols[reverse_idx]] = df.loc[:, cols[reverse_idx]].replace(reverse_code)
        df[col_name + '_score'] = df[cols].sum(axis=1) / df[cols].notnull().sum(axis=1) * len(cols)
        self.df = df

    def add_missing(self):
        df = self.df
        cols = self.original_cols
        col_name = self.col_name
        df[col_name + '_score_missing'] = df[cols].isnull().sum(axis=1) / len(cols)
        self.df = df
