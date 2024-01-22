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
    def __init__(self, df, col_name):
        """
        Constructor
        :param df: subset of data rows (excluding events that do not need to be scored)
        :param col_name: common column name
        """
        cols = df.columns[df.columns.str.match('^' + col_name + '_')]
        cols = cols[~cols.str.endswith('_complete')]
        self.df = df[cols].copy()
        self.original_cols = self.df.columns
        self.col_name = col_name

    def score(self):
        raise NotImplementedError

    def verify_cols(self):
        raise NotImplementedError

    def verify_range(self):
        raise NotImplementedError

    def add_missing(self):
        raise NotImplementedError


class PvsARFIDScorer(Scorer):
    def __init__(self, df, col_name):
        super().__init__(df, col_name)

    def verify_cols(self):
        assert len(self.df.columns) == 7

    def verify_range(self):
        assert (self.df.isin(range(1, 6)) | self.df.isna()).all(axis=None)

    def score(self, reverse_coded):
        df = self.df.copy()
        cols = self.original_cols
        col_name = self.col_name
        if reverse_coded:
            reverse_idx = [x - 1 for x in [1, 2, 4, 6]]
            reverse_code = {i: 6 - i for i in range(1, 6)}
            df.loc[:, cols[reverse_idx]] = df.loc[:, cols[reverse_idx]].replace(reverse_code)
        df[col_name + '_score'] = df[cols].sum(axis=1) / df[cols].notnull().sum(axis=1) * len(cols)
        self.df = df

    def add_missing(self):
        df = self.df.copy()
        cols = self.original_cols
        col_name = self.col_name
        df[col_name + '_score_missing'] = df[cols].isnull().sum(axis=1) / len(cols)
        self.df = df


class PARDIScorer(Scorer):
    def __init__(self, df, col_name):
        super().__init__(df, col_name)
        self.col_grps = {
            'sensory': [],
            'interest': [],
            'fear': [],
            'severity': []
        }

    def verify_cols(self):
        # TODO: make generalizable
        cols = self.original_cols
        col_name = self.col_name
        # add 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, and divide by 10
        self.col_grps['sensory'] = cols[cols.str.match('^' + col_name + '_5[0-9]_')]
        # add 60, 61, 62, 63, 64, 65 66, 67, 68, 69, 70, and divide by 11
        self.col_grps['interest'] = cols[cols.str.match('^' + col_name + '_(6[0-9]|70)_')]
        # add 71b, 72b, 73b, 74b, 75, 76, 77, 78, 79, 80, and divide by 10
        self.col_grps['fear'] = cols[cols.str.match('^' + col_name + '_(7[5-9]|7[1-4]b|80)_')]
        # Add: items 29a, 29b, 29c, 29d, 29e, 30, 32, 33, 34, 35 (if age 20 or below), 40, 41, 42, 43, 46, 47, 48
        # divide by 17 (if under 20) or 16 (if over 20)
        self.col_grps['severity'] = cols[cols.str.match('^' + col_name + '_(29[abcde]|3[02-5]|4[0-36-8])_')]
        assert len(self.col_grps['sensory']) == 10
        assert len(self.col_grps['interest']) == 11
        assert len(self.col_grps['fear']) == 10
        assert len(self.col_grps['severity']) == 17

    def verify_range(self):
        df = self.df
        for grp in self.col_grps:
            cols = self.col_grps[grp]
            if not (df[cols].isin(range(0, 7)) | df[cols].isna()).all(axis=None):
                print(df[
                            ~(df[cols].isin(range(0, 7)) | df[cols].isna()).all(axis=1)
                        ][cols])
            assert (df[cols].isin(range(0, 7)) | df[cols].isna()).all(axis=None)

    def score(self):
        df = self.df
        col_name = self.col_name

        for grp in self.col_grps:
            cols = self.col_grps[grp]
            df[col_name + '_' + grp + '_score'] = df[cols].sum(axis=1) / df[cols].notnull().sum(axis=1)

        self.df = df

    def add_missing(self):
        df = self.df
        col_name = self.col_name

        for grp in self.col_grps:
            cols = self.col_grps[grp]
            df[col_name + '_' + grp + '_score_missing'] = df[cols].isnull().sum(axis=1) / len(cols)

        self.df = df


class SDQScorer(Scorer):
    def __init__(self, df, col_name):
        super().__init__(df, col_name)

