from ..global_vars import pd

class TimePoint:
    def __init__(self, data, tp, arm, score_list):
        assert isinstance(data, pd.DataFrame)
        assert isinstance(tp, str)
        assert isinstance(arm, str)
        assert isinstance(score_list, list)
        self.raw = data.copy()
        self.data = data.copy()
        self.tp = tp
        self.arm = arm
        self.score_list = score_list
    
    def process(self, show_nan, show, grp):
        score_list = self.score_list
        for score_obj in score_list:
            print('\t\t', score_obj)
            self.data = score_obj.process(self.data, show_nan=show_nan, show=show, grp=grp)
    
class Arm:
    def __init__(self, arm, tps):
        assert isinstance(arm, str)
        assert isinstance(tps, dict)
        self.arm = arm
        self.tps = tps
    
    def process(self, show_nan, show, grp):
        print('ARM:', self.arm)
        for tp in self.tps:
            print('\tTIMEPOINT:', tp)
            self.tps[tp].process(show_nan=show_nan, show=show, grp=grp)
