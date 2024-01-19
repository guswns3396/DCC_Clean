class Runner:
    def __init__(self, scorer):
        self.scorer = scorer

    def run(self, **kwargs):
        self.scorer.verify_range()
        self.scorer.verify_cols()
        return self.scorer.score(**kwargs)


class Scorer:
    def __init__(self, df, include_missing):
        self.df = df
        self.include_missing = include_missing

    def score(self):
        raise NotImplementedError

    def verify_cols(self):
        raise NotImplementedError

    def verify_range(self):
        raise NotImplementedError


class PvsARFIDScorer(Scorer):
    def __init__(self, cols, include_missing=True):
        super().__init__(cols, include_missing)

    def verify_cols(self):
        assert len(self.df.columns) == 7

    def verify_range(self):
        assert (self.df.isin(range(1, 6)) | self.df.isna()).all(axis=None)

    def score(self, reverse_coded):
