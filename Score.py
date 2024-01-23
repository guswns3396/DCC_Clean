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

    def score(self, reverse_code):
        df = self.df.copy()
        cols = self.original_cols
        col_name = self.col_name
        if reverse_code:
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
        self.col_grps = {
            'emotion': [x - 1 for x in [3, 8, 13, 16, 24]],
            'conduct': [x - 1 for x in [5, 7, 12, 18, 22]],
            'hyperactivity': [x - 1 for x in [2, 10, 15, 21, 25]],
            'peer': [x - 1 for x in [6, 11, 14, 19, 23]],
            'prosocial': [x - 1 for x in [1, 4, 9, 17, 20]]
        }

    def verify_cols(self):
        assert len(self.original_cols) == 25

    def verify_range(self):
        df = self.df
        cols = self.original_cols

        if not (df[cols].isin(range(0, 3)) | df[cols].isna()).all(axis=None):
            print(df[
                      ~(df[cols].isin(range(0, 3)) | df[cols].isna()).all(axis=1)
                  ][cols])
        assert (df[cols].isin(range(0, 3)) | df[cols].isna()).all(axis=None)

    def score(self, reverse_code):
        df = self.df.copy()
        cols_ori = self.original_cols
        col_name = self.col_name

        # fix reverse
        if reverse_code:
            reverse_idx = [x - 1 for x in [7, 11, 14, 21, 25]]
            reverse_code = {i: 2 - i for i in range(0, 3)}
            df.loc[:, cols_ori[reverse_idx]] = df.loc[:, cols_ori[reverse_idx]].replace(reverse_code)

        col_grps = self.col_grps
        # score by group
        for grp in col_grps:
            cols = cols_ori[col_grps[grp]]
            df[col_name + '_' + grp + '_score'] = df[cols].sum(axis=1) / df[cols].notnull().sum(axis=1) * len(cols)

        # score total
        cols = []
        for grp in col_grps:
            if grp == 'prosocial':
                continue
            cols += col_grps[grp]
        cols = cols_ori[cols]
        df[col_name + '_total_score'] = df[cols].sum(axis=1) / df[cols].notnull().sum(axis=1) * len(cols)

        self.df = df

    def add_missing(self):
        df = self.df
        col_name = self.col_name
        col_grps = self.col_grps
        cols_ori = self.original_cols

        # subscale missing
        for grp in col_grps:
            cols = cols_ori[col_grps[grp]]
            df[col_name + '_' + grp + '_score_missing'] = df[cols].isnull().sum(axis=1) / len(cols)

        # total missing
        cols = []
        for grp in col_grps:
            if grp == 'prosocial':
                continue
            cols += col_grps[grp]
        cols = cols_ori[cols]
        df[col_name + '_total_score_missing'] = df[cols].isnull().sum(axis=1) / len(cols)

        self.df = df


class CESDCScorer(Scorer):
    def __init__(self, df, col_name):
        super().__init__(df, col_name)

    def verify_cols(self):
        assert len(self.original_cols) == 20

    def verify_range(self):
        df = self.df
        cols = self.original_cols

        if not (df[cols].isin(range(0, 4)) | df[cols].isna()).all(axis=None):
            print(df[
                      ~(df[cols].isin(range(0, 4)) | df[cols].isna()).all(axis=1)
                  ][cols])
        assert (df[cols].isin(range(0, 4)) | df[cols].isna()).all(axis=None)

    def score(self, reverse_code):
        df = self.df.copy()
        cols = self.original_cols
        col_name = self.col_name

        # fix reverse
        if reverse_code:
            reverse_idx = [x - 1 for x in [4, 8, 12, 16]]
            reverse_code = {i: 3 - i for i in range(0, 4)}
            df.loc[:, cols[reverse_idx]] = df.loc[:, cols[reverse_idx]].replace(reverse_code)

        # score total
        df[col_name + '_score'] = df[cols].sum(axis=1) / df[cols].notnull().sum(axis=1) * len(cols)

        self.df = df

    def add_missing(self):
        df = self.df
        col_name = self.col_name
        cols = self.original_cols

        df[col_name + '_score_missing'] = df[cols].isnull().sum(axis=1) / len(cols)

        self.df = df


class PSQScorer(Scorer):
    def __init__(self, df, col_name):
        super().__init__(df, col_name)
        self.col_grps = {
            'authoritative': [x - 1 for x in range(1, 14)],
            'authoritarian': [x - 1 for x in range(14, 27)],
            'permissive': [x - 1 for x in range(27, 31)],
        }

    def verify_cols(self):
        assert len(self.original_cols) == 30

    def verify_range(self):
        df = self.df
        cols = self.original_cols

        if not (df[cols].isin(range(1, 7)) | df[cols].isna()).all(axis=None):
            print(df[
                      ~(df[cols].isin(range(1, 7)) | df[cols].isna()).all(axis=1)
                  ][cols])
        assert (df[cols].isin(range(1, 7)) | df[cols].isna()).all(axis=None)

    def score(self):
        df = self.df.copy()
        col_name = self.col_name
        col_grps = self.col_grps
        cols_ori = self.original_cols

        # score by group
        for grp in col_grps:
            cols = cols_ori[col_grps[grp]]
            df[col_name + '_' + grp + '_score'] = df[cols].sum(axis=1) / df[cols].notnull().sum(axis=1)

        self.df = df

    def add_missing(self):
        df = self.df
        col_name = self.col_name
        col_grps = self.col_grps
        cols_ori = self.original_cols

        # subscale missing
        for grp in col_grps:
            cols = cols_ori[col_grps[grp]]
            df[col_name + '_' + grp + '_score_missing'] = df[cols].isnull().sum(axis=1) / len(cols)

        self.df = df


class SF36Scorer(Scorer):
    def __init__(self, df, col_name):
        super().__init__(df, col_name)
        self.likert_grps = {
            'likert5r': [x - 1 for x in [1, 2, 20, 22, 34, 36]],
            'likert3': [x - 1 for x in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]],
            'likert2': [x - 1 for x in [13, 14, 15, 16, 17, 18, 19]],
            'likert6r': [x - 1 for x in [21, 23, 26, 27, 30]],
            'likert6': [x - 1 for x in [24, 25, 28, 29, 31]],
            'likert5': [x - 1 for x in [32, 33, 35]]
        }
        self.col_grps = {
            'physfunc': [x - 1 for x in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]],
            'limphys': [x - 1 for x in [13, 14, 15, 16]],
            'limemo': [x - 1 for x in [17, 18, 19]],
            'energy': [x - 1 for x in [23, 27, 29, 31]],
            'emowell': [x - 1 for x in [24, 25, 26, 28, 30]],
            'socfunc': [x - 1 for x in [20, 32]],
            'pain': [x - 1 for x in [21, 22]],
            'genheal': [x - 1 for x in [1, 33, 34, 35, 36]]
        }

    def verify_cols(self):
        assert len(self.original_cols) == 36

    def verify_range(self):
        df = self.df
        cols = self.original_cols
        likert_grps = self.likert_grps

        for grp in likert_grps:
            if 'likert5' in grp:
                assert (df[cols[likert_grps[grp]]].isin([x for x in range(1, 6)]) | df[cols].isna()).all(
                    axis=None)
            elif 'likert3' in grp:
                assert (df[cols[likert_grps[grp]]].isin([x for x in range(1, 4)]) | df[cols].isna()).all(
                    axis=None)
            elif 'likert2' in grp:
                assert (df[cols[likert_grps[grp]]].isin([x for x in range(1, 3)]) | df[cols].isna()).all(
                    axis=None)
            elif 'likert6' in grp:
                assert (df[cols[likert_grps[grp]]].isin([x for x in range(1, 7)]) | df[cols].isna()).all(
                    axis=None)

    def score(self):
        df = self.df.copy()
        col_name = self.col_name
        col_grps = self.col_grps
        likert_grps = self.likert_grps
        cols_ori = self.original_cols

        # recode
        recode_map = {
            'likert5r': {x: 100 - (25 * (x - 1)) for x in range(1, 6)},
            'likert3': {x: 50 * (x - 1) for x in range(1, 4)},
            'likert2': {x: 100 * (x - 1) for x in range(1, 3)},
            'likert6r': {x: 100 - (20 * (x - 1)) for x in range(1, 7)},
            'likert6': {x: 20 * (x - 1) for x in range(1, 7)},
            'likert5': {x: (25 * (x - 1)) for x in range(1, 6)}
        }
        for grp in likert_grps:
            cols = cols_ori[likert_grps[grp]]
            df[cols] = df[cols].replace(recode_map[grp])

        # subscales
        for grp in col_grps:
            cols = cols_ori[col_grps[grp]]
            df[col_name + '_' + grp + '_score'] = df[cols].sum(axis=1) / df[cols].notnull().sum(axis=1)

        self.df = df

    def add_missing(self):
        df = self.df
        col_name = self.col_name
        col_grps = self.col_grps
        cols_ori = self.original_cols

        # subscale missing
        for grp in col_grps:
            cols = cols_ori[col_grps[grp]]
            df[col_name + '_' + grp + '_score_missing'] = df[cols].isnull().sum(axis=1) / len(cols)

        self.df = df


class RCMASScorer(Scorer):
    def __init__(self, df, col_name):
        super().__init__(df, col_name)
        self.col_grps = {
            'phy': [x - 1 for x in [1, 5, 7]],
            'wor': [x - 1 for x in [2, 3, 6, 8]],
            'soc': [x - 1 for x in [4, 9, 10]],
        }

    def verify_cols(self):
        assert len(self.original_cols) == 10

    def verify_range(self):
        df = self.df
        cols = self.original_cols

        if not (df[cols].isin(range(0, 2)) | df[cols].isna()).all(axis=None):
            print(df[
                      ~(df[cols].isin(range(0, 2)) | df[cols].isna()).all(axis=1)
                  ][cols])
        assert (df[cols].isin(range(0, 2)) | df[cols].isna()).all(axis=None)

    def score(self):
        df = self.df.copy()
        col_name = self.col_name
        col_grps = self.col_grps
        cols_ori = self.original_cols

        # score by group
        for grp in col_grps:
            cols = cols_ori[col_grps[grp]]
            df[col_name + '_' + grp + '_score'] = df[cols].sum(axis=1) / df[cols].notnull().sum(axis=1) * len(cols)

        # score total
        cols = []
        for grp in col_grps:
            cols += col_grps[grp]
        cols = cols_ori[cols]
        df[col_name + '_total_score'] = df[cols].sum(axis=1) / df[cols].notnull().sum(axis=1) * len(cols)

        self.df = df

    def add_missing(self):
        df = self.df
        col_name = self.col_name
        col_grps = self.col_grps
        cols_ori = self.original_cols

        # subscale missing
        for grp in col_grps:
            cols = cols_ori[col_grps[grp]]
            df[col_name + '_' + grp + '_score_missing'] = df[cols].isnull().sum(axis=1) / len(cols)

        # total missing
        cols = []
        for grp in col_grps:
            cols += col_grps[grp]
        cols = cols_ori[cols]
        df[col_name + '_total_score_missing'] = df[cols].isnull().sum(axis=1) / len(cols)
