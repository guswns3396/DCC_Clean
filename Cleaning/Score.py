from ..global_vars import pd, np, warnings, set_trace, INTAKE, ID, PID
from .Range import Range

class Score:
    def __init__(self, tp, arm, colname, cleaners):
        assert isinstance(tp, str)
        assert isinstance(arm, str)
        assert isinstance(colname, str)
        assert isinstance(cleaners, list)
        self.tp = tp
        self.arm = arm
        self.colname = colname
        self.cleaners = cleaners
    
    def get_cols(self, data):
        data = data.copy()
        colname = self.colname
        cols = data.columns[data.columns.str.startswith(colname)]
        self.cols = cols
        return self.cols
    
    def clean(self, data, show):
        data = data.copy()
        cleaners = self.cleaners
        for cleaner in cleaners:
            data = cleaner.clean(data, show=show)
        return data
    
    def get_invalid_range_idx(self, data, cols, set_range, dtype='str'):
        # make sure cols are array like
        assert (isinstance(cols, pd.Index) or isinstance(cols, list))
        # get data
        data = data.copy()
        
        # discrete
        if set_range.rtype == 'discrete':
            spc = set_range.spc
            if dtype == 'str':
                set_range = set([str(i) for i in set_range.set]) | set([str(i) for i in spc])
            elif dtype == 'float':
                set_range = set([float(i) for i in set_range.set]) | set([float(i) for i in spc])
            # add NaN
            set_range.add(np.nan)
            # get indices that violate range
            idx = data[cols][(~data[cols].isin(set_range)).any(axis=1)].index

        # continuous
        elif set_range.rtype == 'continuous':
            # see which entries cannot be converted to float
            def check_float_conversion(ser):
                return ser.str.match(r'^[0-9]\d*(\.\d+)?$', na=True)
            try:
                data_f = data.loc[:,cols].astype(float)
            except ValueError:
                data_s = data.loc[:,cols].apply(check_float_conversion)
                idx = data[(~data_s).any(axis=1)].index
                # look at continuous range
                data_f = data.loc[data.index[~data.index.isin(idx)], cols].astype(float)
            else:
                idx = pd.Index([])
            # consider min and max vals
            if set_range.start is None:
                ltmin = False
            else:
                ltmin = data_f < set_range.start
            if set_range.end is None:
                gtmax = False
            else:
                gtmax = data_f > set_range.end
            # consider range & NaN
            invalid = (ltmin | gtmax)
            # also special values
            valid = data.loc[data.index[~data.index.isin(idx)], cols].isin(set_range.spc)
            invalid = invalid & ~valid
            idx = idx.union(data_f[invalid.any(axis=1)].index)
            
        # date
        elif set_range.rtype == 'date':
            # convert to date
            data_d = data[cols].apply(pd.to_datetime)
            # consider min and max vals
            if set_range.start is None:
                ltmin = False
            else:
                ltmin = data_d < set_range.start
            if set_range.end is None:
                gtmax = False
            else:
                gtmax = data_d > set_range.end
            # consider range & NaN
            invalid = (ltmin | gtmax)
            # also special values
            valid = data.loc[data.index, cols].isin(set_range.spc)
            invalid = invalid & ~valid
            idx = data_d[invalid.any(axis=1)].index
            
        # any
        elif set_range.rtype == 'any':
            idx = []
            
        else:
            raise ValueError

        # store idx
        self.idx = idx
        return idx
    
    def verify_col_range(self, data, cols, grp=False):
        data = data.copy()
        idx = self.idx
        if not len(idx) == 0:
            if grp:
                view = data.copy()
                view['site'] = view[ID].str.slice(0,2)
                for i,v in view.loc[idx, [ID, *cols, 'site']].groupby('site'):
                    display(v)
            else:
                if ID in data.columns:
                    display(data.loc[idx, [ID, *cols]])
                elif PID+'_'+self.tp in data.columns:
                    display(data.loc[idx, [PID+'_'+self.tp, *cols]])
                else:
                    display('no ID col')
                    raise ValueError
            display('verify_col_range: invalid range')
            # set_trace()
            
    def verify(self, data, cols, set_range=None, dtype='str', grp=False):
        data = data.copy()
        self.get_invalid_range_idx(data, cols, set_range, dtype)
        self.verify_col_range(data, cols, grp=grp)
            
    def show_nan(self, data):
        data = data.copy()
        cols = self.cols
        tp = self.tp
        if data[cols].isna().any(axis=None):
            if self.arm in ['child_web', 'child_int']:
                display(data.loc[data[cols].isna().any(axis=1), [ID, *cols]])
            elif self.arm in ['parent_web']:
                display(data.loc[data[cols].isna().any(axis=1), [PID+'_'+tp, *cols]])
            else:
                raise KeyError
            display("NaN found")
            # set_trace()

    def get_col_idx(self, question_numbers, offset=1):
        result = [i-offset for i in question_numbers]
        return result

class ScoreCES(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)

    def score(self, data):
        data = data.copy()
        cols = self.cols
        tp = self.tp
        colname = self.colname
        # score
        data.loc[:,cols] = data.loc[:,cols].astype(float)
        data[colname+'_global_'+tp] = data[cols].mean(axis=1)
        # % missing
        data[colname+'_global_missing_'+tp] = data[cols].isnull().sum(axis=1) / len(cols)
        # update cols
        self.get_cols(data)
        return data

    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        assert len(cols) == 8
        # clean
        data = self.clean(data,show=show)
        # verify
        self.verify(data, cols, Range(rtype='discrete', set_=set([i for i in range(1, 4+1)])), grp=grp)
        # score
        data = self.score(data)
        # verify again
        self.verify(data, self.cols[~self.cols.str.endswith('_missing_'+self.tp)], Range(rtype='continuous', start_=1, end_=4, spc_=[]), grp=grp, dtype='float')
        # show nan
        if show_nan: self.show_nan(data)
        return data

class ScoreCET(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)

    def score(self, data):
        data = data.copy()
        cols = self.cols
        tp = self.tp
        colname = self.colname

        avoid_rule_driven = self.get_col_idx([9,10,11,15,16,20,22,23])
        weight_control = self.get_col_idx([2,6,8,13,18])
        mood_improvement = self.get_col_idx([1,4,14,17,24])
        lack_exercise_enjoyment = self.get_col_idx([5,12,21])
        exercise_rigidity = self.get_col_idx([3,7,19])

        # get scores
        data.loc[:,cols] = data.loc[:,cols].astype(float)
        data[colname+'_avoid_rule_driven_subscale_'+tp] = data[cols[avoid_rule_driven]].mean(axis=1)
        data[colname+'_weight_control_subscale_'+tp] = data[cols[weight_control]].mean(axis=1)
        data[colname+'_mood_improvement_subscale_'+tp] = data[cols[mood_improvement]].mean(axis=1)
        data[colname+'_lack_exercise_enjoyment_subscale_'+tp] = data[cols[lack_exercise_enjoyment]].mean(axis=1)
        data[colname+'_exercise_rigidity_subscale_'+tp] = data[cols[exercise_rigidity]].mean(axis=1)
        new_cols = [
            '_avoid_rule_driven_subscale_',
            '_weight_control_subscale_',
            '_mood_improvement_subscale_',
            '_lack_exercise_enjoyment_subscale_',
            '_exercise_rigidity_subscale_'
        ]
        data[colname+'_global_'+tp] = data[[colname+col+tp for col in new_cols]].mean(axis=1)
        # % missing
        for col,group in zip(new_cols,[avoid_rule_driven,weight_control,mood_improvement,lack_exercise_enjoyment,exercise_rigidity]):
            data[colname+col+'missing_'+tp] = data[cols[group]].isnull().sum(axis=1) / len(cols[group])
        data[colname+'_global_missing_'+tp] = data[cols[
            avoid_rule_driven+weight_control+mood_improvement+lack_exercise_enjoyment+exercise_rigidity
        ]].isnull().sum(axis=1) / len(cols[
            avoid_rule_driven+weight_control+mood_improvement+lack_exercise_enjoyment+exercise_rigidity
        ])
        # update cols
        self.get_cols(data)
        return data

    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        assert len(cols) == 24
        # clean
        data = self.clean(data,show=show)
        # verify
        self.verify(data, cols, Range(rtype='discrete', set_=set([i for i in range(0, 5+1)])), grp=grp)
        # score
        data = self.score(data)
        # verify again
        self.verify(data, self.cols, Range(rtype='continuous', start_=0, end_=5, spc_=[]), grp=grp)
        # show nan
        if show_nan: self.show_nan(data)
        return data

class ScoreTSPE(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)

    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        assert len(cols) == 2
        # clean
        data = self.clean(data,show=show)
        # verify
        self.verify(data, cols, Range(rtype='discrete', set_=set([i for i in range(10+1)])), grp=grp)
        # show nan
        if show_nan: self.show_nan(data)
        return data

class ScoreCOVIDWeb(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)

    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        assert len(cols) == 1
        # clean
        data = self.clean(data,show=show)
        # verify
        self.verify(data, [self.colname+'_imm_post_web_'+self.tp], Range(rtype='discrete', set_=set([1,2])), grp=grp)
        # show nan
        if show_nan: self.show_nan(data)
        return data

class ScoreCOVID(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)

    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        assert len(cols) == 6
        # clean
        data = self.clean(data,show=show)
        # verify
        self.verify(data, [self.colname+'_check_'+self.tp], Range(rtype='discrete', set_=set([1])), grp=grp)
        self.verify(data, [self.colname+'_affect_group_'+self.tp], Range(rtype='discrete', set_=set([i for i in range(1,5+1)])), grp=grp)
        self.verify(data, [self.colname+'_imm_post_'+self.tp], Range(rtype='discrete', set_=set([i for i in range(1,2+1)])), grp=grp)
        self.verify(data, [self.colname+'_cont_telhlth_'+self.tp], Range(rtype='discrete', set_=set([i for i in range(0,1+1)])), grp=grp)
        self.verify(
            data,
            [
                self.colname+'_telhlth_num_ses_'+self.tp,
                self.colname+'_inper_num_ses_'+self.tp,
            ],
            Range(rtype='discrete', set_=set([i for i in range(0,18+1)]))
        )
        # show nan
        if show_nan: self.show_nan(data)
        return data
    
class ScorePvAN(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)
        
    def fix_reverse(self, data):
        data = data.copy()
        cols = self.cols
        normal = [3,5,7]
        reverse = [1,2,4,6]
        normal = self.get_col_idx(normal)
        reverse = self.get_col_idx(reverse)
        # fix reverse coding
        reverse_code = {str(i): str(6-i) for i in range(1,6)}
        data.loc[:, cols[reverse]] = data[cols[reverse]].replace(reverse_code)
        return data
    
    def score(self, data):
        data = data.copy()
        cols = self.cols
        tp = self.tp
        colname = self.colname
        # get total score
        data.loc[:,cols] = data.loc[:,cols].astype(float)
        data[colname+'_score_'+tp] = data[cols].sum(axis=1) / data[cols].notnull().sum(axis=1) * len(cols)
        # % missing
        data[colname+'_score_missing_'+tp] = data[cols].isnull().sum(axis=1) / len(cols)
        # update cols
        self.get_cols(data)
        return data
    
    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        assert len(cols) == 7
        # clean
        data = self.clean(data,show=show)
        # fix reverse
        data = self.fix_reverse(data)
        # verify
        self.verify(data, cols, Range(rtype='discrete', set_=set([i for i in range(1, 5+1)])), grp=grp)
        # score
        data = self.score(data)
        # verify again
        self.verify(data, [self.colname+'_score_'+self.tp], Range(rtype='continuous', start_=7, end_=35, spc_=[], dtype='float', grp=grp))
        # show nan
        if show_nan: self.show_nan(data)
        return data

class ScoreYBC(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)
    
    def score(self, data):
        data = data.copy()
        self.get_cols(data)
        cols = self.cols
        tp = self.tp
        colname = self.colname
        data.loc[:,cols] = data.loc[:,cols].astype(float)
        preocc = [1, 3, 4, 7]
        ritual = [10, 12, 13, 16]
        preocc = self.get_col_idx(preocc)
        ritual = self.get_col_idx(ritual)
        # get score
        data[colname+'_preoc_score_'+tp] = data[cols[preocc]].sum(axis=1) / data[cols[preocc]].notnull().sum(axis=1) * len(cols[preocc])
        data[colname+'_rit_score_'+tp] = data[cols[ritual]].sum(axis=1) / data[cols[ritual]].notnull().sum(axis=1) * len(cols[ritual])
        data[colname+'_tot_score_'+tp] = data[colname+'_preoc_score_'+tp] + data[colname+'_rit_score_'+tp]
        # % missing
        data[colname+'_preoc_score_missing_'+tp] = data[cols[preocc]].isnull().sum(axis=1) / len(cols[preocc])
        data[colname+'_rit_score_missing_'+tp] = data[cols[ritual]].isnull().sum(axis=1) / len(cols[ritual])
        data[colname+'_tot_score_missing_'+tp] = data[cols[preocc + ritual]].isnull().sum(axis=1) / len(cols[preocc + ritual])
        # update cols
        self.get_cols(data)
        return data
        
    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        assert len(cols) == 21
        # clean
        data = self.clean(data,show=show)
        # GLOBAL SEVERITY AND RELIABILITY NOT USED
        # verify
        self.verify(data, cols[:19], Range(rtype='discrete', set_=set([i for i in range(0, 4+1)])), grp=grp)
        # score
        data = self.score(data)
        # show nan
        if show_nan: self.show_nan(data)
        return data
    
class ScoreHRQ(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)
        
    def get_coop_help_cols(self):
        cooperation = [1, *range(6,11)]
        helpfulness = [*range(2,6), 11]
        cooperation = self.get_col_idx(cooperation)
        helpfulness = self.get_col_idx(helpfulness)
        self.cooperation = cooperation
        self.helpfulness = helpfulness
        return cooperation, helpfulness
        
    def score(self, data):
        data = data.copy()
        cols = self.cols
        colname = self.colname
        tp = self.tp
        self.get_coop_help_cols()
        cooperation = self.cooperation
        helpfulness = self.helpfulness
        data.loc[:,cols.difference(cols[[11, 13]])] = data.loc[:,cols.difference(cols[[11, 13]])].astype(float)
        data[colname+'_cooperation_'+tp] = data[cols[cooperation]].sum(axis=1) / data[cols[cooperation]].notnull().sum(axis=1) * len(cols[cooperation])
        data[colname+'_helpfulness_'+tp] = data[cols[helpfulness]].sum(axis=1) / data[cols[helpfulness]].notnull().sum(axis=1) * len(cols[helpfulness])
        # % missing
        data[colname+'_cooperation_missing_'+tp] = data[cols[cooperation]].isnull().sum(axis=1) / len(cols[cooperation])
        data[colname+'_helpfulness_missing_'+tp] = data[cols[helpfulness]].isnull().sum(axis=1) / len(cols[helpfulness])
        # update cols
        self.get_cols(data)
        return data
    
    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        assert len(cols) == 14
        # clean
        data = self.clean(data,show=show)
        # verify
        self.verify(data, cols[:11], Range(rtype='discrete', set_=set([i for i in range(-3, 3+1)])), grp=grp)
        self.verify(data, cols[[13-1]], Range(rtype='discrete', set_=set([i for i in range(1, 5+1)])), grp=grp)
        # score
        data = self.score(data)
        # show nan
        if show_nan: self.show_nan(data)
        return data
    
class ScoreBDI(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)
        
    def score(self, data):
        data = data.copy()
        cols = self.cols
        colname = self.colname
        tp = self.tp
        # convert
        data.loc[:,cols] = data.loc[:,cols].astype(float)
        # score Q19 as 0 if Q20 == yes(1)
        data.loc[data[cols[20-1]] == 1, cols[19-1]] = 0
        # verify they all == 0
        assert (data[data[cols[20-1]] == 1][cols[19-1]] == 0).all()
        # score
        data[colname+'_score_'+tp] = data[cols].sum(axis=1) / data[cols].notnull().sum(axis=1) * len(cols)
        # % missing
        data[colname+'_score_missing_'+tp] = data[cols].isnull().sum(axis=1) / len(cols)
        # update cols
        self.get_cols(data)
        return data
    
    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        assert len(cols) == 22
        # clean
        data = self.clean(data,show=show)
        # verify
        self.verify(data, cols.difference([cols[20-1]]), Range(rtype='discrete', set_=set([i for i in range(0, 3+1)])), grp=grp)
        self.verify(data, [cols[20-1]], Range(rtype='discrete', set_=set([i for i in range(0, 1+1)])), grp=grp)
        # score
        data = self.score(data)
        # show nan
        if show_nan: self.show_nan(data)
        return data

class ScoreSDQ(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)
    
    def fix_reverse(self, data):
        data = data.copy()
        cols = self.cols
        reverse = [7, 21, 25, 11, 14]
        reverse = self.get_col_idx(reverse)
        reverse_code = {str(i): str(2-i) for i in range(0,3)}
        data.loc[:, cols[reverse]] = data[cols[reverse]].replace(reverse_code)
        return data
    
    def score(self, data):
        data = data.copy()
        cols = self.cols
        colname = self.colname
        tp = self.tp
        data.loc[:,cols] = data.loc[:,cols].astype(float)
        grps = {}
        grps['emotional'] = [3,8,13,16,24]
        grps['conduct'] = [5,7,12,18,22]
        grps['hyperactivity'] = [2,10,15,21,25]
        grps['peer'] = [6,11,14,19,23]
        grps['prosocial'] = [1,4,9,17,20]
        for grp in grps:
            grps[grp] = self.get_col_idx(grps[grp])
        data[colname+'_emotional_'+tp] = data[cols[grps['emotional']]].sum(axis=1) / data[cols[grps['emotional']]].notnull().sum(axis=1) * len(cols[grps['emotional']])
        data[colname+'_conduct_'+tp] = data[cols[grps['conduct']]].sum(axis=1) / data[cols[grps['conduct']]].notnull().sum(axis=1) * len(cols[grps['conduct']])
        data[colname+'_hyperactivity_'+tp] = data[cols[grps['hyperactivity']]].sum(axis=1) / data[cols[grps['hyperactivity']]].notnull().sum(axis=1) * len(cols[grps['hyperactivity']])
        data[colname+'_peer_'+tp] = data[cols[grps['peer']]].sum(axis=1) / data[cols[grps['peer']]].notnull().sum(axis=1) * len(cols[grps['peer']])
        data[colname+'_prosocial_'+tp] = data[cols[grps['prosocial']]].sum(axis=1) / data[cols[grps['prosocial']]].notnull().sum(axis=1) * len(cols[grps['prosocial']])
        data[colname+'_score_'+tp] = data[[colname+'_'+grp+'_'+tp for grp in grps if grp != 'prosocial']].sum(axis=1, skipna=False)
        # % missing
        data[colname+'_emotional_missing_'+tp] = data[cols[grps['emotional']]].isnull().sum(axis=1) / len(cols[grps['emotional']])
        data[colname+'_conduct_missing_'+tp] = data[cols[grps['conduct']]].isnull().sum(axis=1) / len(cols[grps['conduct']])
        data[colname+'_hyperactivity_missing_'+tp] = data[cols[grps['hyperactivity']]].isnull().sum(axis=1) / len(cols[grps['hyperactivity']])
        data[colname+'_peer_missing_'+tp] = data[cols[grps['peer']]].isnull().sum(axis=1) / len(cols[grps['peer']])
        data[colname+'_prosocial_missing_'+tp] = data[cols[grps['prosocial']]].isnull().sum(axis=1) / len(cols[grps['prosocial']])
        data[colname+'_score_missing_'+tp] = data[cols[grps['emotional']+grps['conduct']+grps['hyperactivity']+grps['peer']]].isnull().sum(axis=1) / len(cols[grps['emotional']+grps['conduct']+grps['hyperactivity']+grps['peer']])
        self.grps = grps
        # update cols
        self.get_cols(data)
        return data
        
    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        assert len(cols) == 25
        # clean
        data = self.clean(data,show=show)
        # verify
        self.verify(data, cols, Range(rtype='discrete', set_=set([i for i in range(0, 2+1)])), grp=grp)
        # fix reverse coding
        data = self.fix_reverse(data)
        # score
        data = self.score(data)
        # verify
        colname = self.colname
        tp = self.tp
        grps = self.grps
        self.verify(
            data,
            [colname+'_'+grp+'_'+tp for grp in grps],
            Range(rtype='continuous', start_=0, end_=10, spc_=[]),
            dtype='float', grp=grp
        )
        self.verify(
            data,
            [colname+'_score_'+tp],
            Range(rtype='continuous', start_=0, end_=40, spc_=[]),
            dtype='float', grp=grp
        )
        # show nan
        if show_nan: self.show_nan(data)
        return data
    
class ScoreBAI(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)
        
    def score(self, data):
        data = data.copy()
        cols = self.cols
        colname = self.colname
        tp = self.tp
        data.loc[:,cols] = data.loc[:,cols].astype(float)
        data[colname+'_score_'+tp] = data[cols].sum(axis=1) / data[cols].notnull().sum(axis=1) * len(cols)
        # % missing
        data[colname+'_score_missing_'+tp] = data[cols].isnull().sum(axis=1) / len(cols)
        # update cols
        self.get_cols(data)
        return data
    
    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        # clean
        data = self.clean(data,show=show)
        # verify
        self.verify(data, cols, Range(rtype='discrete', set_=set([i for i in range(0, 3+1)])), grp=grp)
        # score
        data = self.score(data)
        # show nan
        if show_nan: self.show_nan(data)
        return data
    
class ScoreCYBOCS(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)
    
    def score(self, data):
        data = data.copy()
        cols = self.cols
        colname = self.colname
        tp = self.tp
        data.loc[:,cols] = data.loc[:,cols].astype(float)
        data[colname+'_tot_score_'+tp] = data[cols].sum(axis=1) / data[cols].notnull().sum(axis=1) * len(cols)
        # sum Q1-5
        data[colname+'_obs_score_'+tp] = data[cols[:5]].sum(axis=1) / data[cols[:5]].notnull().sum(axis=1) * len(cols[:5])
        # sum Q6-10
        data[colname+'_comp_score_'+tp] = data[cols[5:]].sum(axis=1) / data[cols[5:]].notnull().sum(axis=1) * len(cols[5:])
        # % missing
        data[colname+'_tot_score_missing_'+tp] = data[cols].isnull().sum(axis=1) / len(cols)
        data[colname+'_obs_score_missing_'+tp] = data[cols[:5]].isnull().sum(axis=1) / len(cols[:5])
        data[colname+'_comp_score_missing_'+tp] = data[cols[5:]].isnull().sum(axis=1) / len(cols[5:])
        # update cols
        self.get_cols(data)
        return data
        
    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        # clean
        data = self.clean(data,show=show)
        # verify
        self.verify(data, cols, Range(rtype='discrete', set_=set([i for i in range(0, 4+1)])), grp=grp)
        # score
        data = self.score(data)
        # show nan
        if show_nan: self.show_nan(data)
        return data

class ScoreCheckOutsideTreatment(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)
        
    def verify_implications(self, data):
        data = data.copy()
        cols = self.cols
        colname = self.colname
        tp = self.tp
        # verify either yes or no
        trt_types = cols.str.extract('^'+colname+'_(.+)_.+_'+tp+'$')[0].unique()[:-1]
        yess = [colname+'_'+trt_type+'_yes_'+tp for trt_type in trt_types]
        nos = [colname+'_'+trt_type+'_no_'+tp for trt_type in trt_types]
        if not ((data[yess] == '1').values | (data[nos] == '1').values).all():
            display(
                data.loc[
                    ~((data[yess] == '1').values | (data[nos] == '1').values).any(axis=1),
                    [ID, *cols[cols.isin(yess + nos)]]
                ]
            )
            display("verify_implications: yes or no")
            # set_trace()
        # verify treatment implies yes
        cur = [colname+'_'+trt_type+'_cur_'+tp for trt_type in trt_types]
        ed = [colname+'_'+trt_type+'_ed_'+tp for trt_type in trt_types]
        wt = [colname+'_'+trt_type+'_wt_'+tp for trt_type in trt_types]
        trt = (data[cur] == '1').values | (data[ed] == '1').values | (data[wt] == '1').values
        if not (~trt | (data[yess] == '1').values).all():
            # !(p -> q) == p & !q
            display(
                data.loc[
                    (trt & ~(data[yess] == '1').values).any(axis=1),
                    [
                        ID,
                        *cols[cols.isin(yess + cur + ed + wt)]
                    ]
                ]
            )
            display("verify_implications: treatment without yes")
            # set_trace()
        
    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        # clean
        data = self.clean(data,show=show)
        # verify implications
        self.verify_implications(data)
        # verify all except specifying
        self.verify(data, cols[:-1], Range(rtype='discrete', set_=set({'1', '0'})), grp=grp)
        # show nan
        if show_nan: self.show_nan(data)
        return data
    
class ScoreIdentifier(Score):
    def __init__(self, tp, arm, colname, cleaners):
        if arm == 'parent_web':
            colname = colname+'_'+tp
        super().__init__(tp, arm, colname, cleaners)
        self.cols = [self.colname]
        
    def __repr__(self):
        return 'ScoreIdentifier('+self.colname+')'
    
    def verify_nan(self, data):
        colname = self.colname
        assert colname in data.columns
        if data[colname].isnull().sum() != 0:
            display(data[data[colname].isnull()])
            display('verify_nan: null id')
            # set_trace()
    
    def verify_duplicate(self, data):
        colname = self.colname
        assert colname in data.columns
        if data.duplicated(subset=colname).sum() != 0:
            display(data[data.duplicated(subset=colname, keep=False)])
            display('verify_nan: duplicate id')
            # set_trace()
            
    def verify_format(self, data):
        colname = self.colname
        assert colname in data.columns
        if colname == 'Intake_number':
            r1 = data[colname].str.match(r'^SU-\d\d\d$', na=False)
            r2 = data[colname].str.match(r'^UC-\d\d\d$', na=False)
        elif colname == 'ID_number':
            r1 = data[colname].str.match(r'^SU-\d\d\d\d$', na=False)
            r2 = data[colname].str.match(r'^UC-\d\d\d\d$', na=False)
        elif colname.startswith(PID):
            r1 = data[colname].str.match(r'^SU-\d\d\d\d_0(1|2|3)$', na=False)
            r2 = data[colname].str.match(r'^UC-\d\d\d\d_0(1|2|3)$', na=False)
        if not (r1 | r2).all():
            display(data[~r1 & ~r2])
            display('verify_format: invalid format')
            # set_trace()
    
    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # verify colname
        colname = self.colname
        assert colname in data.columns
        # clean
        data = self.clean(data,show=show)
        # verify
        self.verify_nan(data)
        self.verify_duplicate(data)
        self.verify_format(data)
        # show nan
        if show_nan: self.show_nan(data)
        return data
    
class ScoreEDE(Score):
    def __init__(self, tp, arm, colname, cleaners, ede_subscales, ede_colgrps, ede_cols):
        super().__init__(tp, arm, colname, cleaners)
        self.ede_subscales = ede_subscales
        self.ede_colgrps = ede_colgrps
        self.ede_cols = ede_cols
    
    def verify_implications(self, data):
        EDE_COLGRPS = self.ede_colgrps
        tp = self.tp
        colname = self.colname
        # subscale max(control, w/s) <= TOT <= control + w/s
        for colgrp in EDE_COLGRPS.values():
            if colgrp.subscale == 'restraint':
                cols = pd.Series([col.name+'_'+tp for col in colgrp.columns])
                tot = cols[cols.str.endswith('_TOT_'+tp)].values[0]
                con = cols[cols.str.endswith('_CON_'+tp)].values[0]
                ws = cols[~cols.str.endswith('_TOT_'+tp) & ~cols.str.endswith('_CON_'+tp)].values[0]
                p = (data[tot].astype(float) <= data[con].astype(float) + data[ws].astype(float)) | (data[[ws, con, tot]].isnull().all(axis=1))
                q = (data[[con, ws]].astype(float).max(axis=1) <= data[tot].astype(float)) | (data[[ws, con, tot]].isnull().all(axis=1))
                if not (p & q).all():
                    display(data[~p | ~q][[ID, ws, con, tot]])
                    display("verify_ede_implications: max <= TOT <= control + w/s")
                    # set_trace()

        # bulimic episodes 000 <-> 00 days
        # days <= episodes
        for day, epi in zip(EDE_COLGRPS['bulimic_episodes_days'].columns, EDE_COLGRPS['bulimic_episodes_epi'].columns):
            p_col = day.name+'_'+tp
            q_col = epi.name+'_'+tp
            p = (data[p_col] == '00') | data[p_col].isnull()
            q = (data[q_col] == '000') | data[q_col].isnull()
            if not ((p & q) | ((~p) & (~q))).all():
                display(data[~((p & q) | ((~p) & (~q)))][[ID, p_col, q_col]])
                display("verify_ede_implications: 000 episodes <-> 00 days")
                # set_trace()
            cond1 = (data[p_col].replace('99', np.nan).astype(float) <= data[q_col].astype(float)) | data[[p_col, q_col]].isnull().any(axis=1)
            cond2 = (data[p_col] == '99') & (data[q_col] == '999')
            if not (cond1 | cond2).all():
                display(data[~(cond1 | cond2)][[ID, p_col, q_col]])
                display("verify_ede_implications: days <= episodes")
                # set_trace()
                
        # OBE free for 12 weeks -> 000 OBE episodes
        p_col = colname+'_OBE_wk_free_'+tp
        q_col = data.columns[data.columns.str.startswith(colname+'_OBE_epi_')]
        p = data[p_col] == '12'
        q = (data[q_col] == '000').all(axis=1)
        if not ((~p) | q).all():
            display(data[~((~p) | q)][[ID, p_col, q_col]])
            display("verify_ede_implications: 12 weeks -> 000 episodes")
            # set_trace()

        # if episodes.sum() < 12 => BED module vars 999
        p_cols = [colname+col+tp for col in ['_OBE_epi_','_OBE_epi_mo2_','_OBE_epi_mo3_']]
        q_cols = [col.name+'_'+tp for col in EDE_COLGRPS['features_binge_eating'].columns]
        q_cols += [col.name+'_'+tp for col in EDE_COLGRPS['distress_binge_eating'].columns]
        # convert to float
        p = data[p_cols].copy().astype(float)
        # replace 999
        p = p.replace(999, np.nan)
        p = (p.sum(axis=1) < 12) | ((p.isnull()).all(axis=1))
        q = ((data[q_cols] == '9') | (data[q_cols].isnull())).all(axis=1)
        if not ((~p) | q).all():
            display(data[~((~p) | q)][[ID, *p_cols, *q_cols]])
            display("verify_ede_implications: < 12 OBE episodes -> 999 BED module vars")
            # set_trace()

        # laxative 00 episodes <-> 999 avg
        # 00 episodes <-> null laxative
        # null laxative <-> 999 avg
        p_col = colname+'_Laxative_'+tp
        q_col = colname+'_Laxative_Taken_'+tp
        r_col = colname+'_Laxative_Type_'+tp
        p = (data[p_col] == '00') | data[p_col].isnull()
        q = (data[q_col] == '999') | data[q_col].isnull()
        r = data[r_col].isnull()
        if not ((~p | q) & (~q | p)).all():
            display(data[~((~p | q) & (~q | p))][[ID, p_col, q_col]])
            display("verify_ede_implications: 00 episodes <-> 999 average")
            # set_trace()
        if not ((~p | r) & (~r | p)).all():
            display(data[~((~p | r) & (~r | p))][[ID, p_col, r_col]])
            display("verify_ede_implications: 00 episodes <-> null type")
            # set_trace()

        # diuretic 00 episodes <-> 999 avg
        # 00 episodes <-> null diuretic
        # null diuretic <-> 999 avg
        p_col = colname+'_Diuretic_'+tp
        q_col = colname+'_Diuretic_Taken_'+tp
        r_col = colname+'_Diuretic_Type_'+tp
        p = (data[p_col] == '00') | data[p_col].isnull()
        q = (data[q_col] == '999') | data[q_col].isnull()
        r = data[r_col].isnull()
        if not ((~p | q) & (~q | p)).all():
            display(data[~((~p | q) & (~q | p))][[ID, p_col, q_col]])
            display("verify_ede_implications: 00 episodes <-> 999 average")
            # set_trace()
        if not ((~p | r) & (~r | p)).all():
            display(data[~((~p | r) & (~r | p))][[ID, p_col, r_col]])
            display("verify_ede_implications: 00 episodes <-> null type")
            # set_trace()

        # diet pill 00 episodes <-> 999 avg
        # 00 episodes <-> null diuretic
        # null diuretic <-> 999 avg
        p_col = colname+'_Dietpill_'+tp
        q_col = colname+'_Dietpill_Taken_'+tp
        r_col = colname+'_Dietpill_Type_'+tp
        p = (data[p_col] == '00') | data[p_col].isnull()
        q = (data[q_col] == '999') | data[q_col].isnull()
        r = data[r_col].isnull()
        if not ((~p | q) & (~q | p)).all():
            display(data[~((~p | q) & (~q | p))][[ID, p_col, q_col]])
            display("verify_ede_implications: 00 episodes <-> 999 average")
            # set_trace()
        if not ((~p | r) & (~r | p)).all():
            display(data[~((~p | r) & (~r | p))][[ID, p_col, r_col]])
            display("verify_ede_implications: 00 episodes <-> null type")
            # set_trace()

        # driven exercising 0 days <-> 0 episodes
        # days <= episodes
        p_col = colname+'_Exercise_days_'+tp
        q_col = colname+'_Exercise_epi_'+tp
        p = (data[p_col] == '00') | data[p_col].isnull()
        q = (data[q_col] == '00') | data[q_col].isnull()
        if not ((~p | q) & (~q | p)).all():
            display(data[~((~p | q) & (~q | p))][[ID, p_col, q_col]])
            display("verify_ede_implications: 0 days <-> 0 episodes")
            # set_trace()
        cond1 = (data[p_col].astype(float) <= data[q_col].astype(float)) | data[[p_col, q_col]].isnull().any(axis=1)
        if not (cond1).all():
            display(data[~(cond1)][[ID, p_col, q_col]])
            display("verify_ede_implications: days <= episodes")
            # set_trace()
            
        # BMI vs height & weight
        bmi = colname+'_BMI_'+tp
        height = colname+'_Height_in_'+tp
        weight = colname+'_Wt_lb_'+tp
        cond = np.isclose(data[bmi].astype(float), data[weight].astype(float)*703/(data[height].astype(float)**2), atol=2)
        if not cond.all():
            display(data[~(cond)][[ID, bmi, height, weight]])
            display("verify_ede_implications: bmi != height & weight data")
            # set_trace()

        # other hw source (4) -> hw source other not null
        p_col = colname+'_HW_source_'+tp
        q_col = colname+'_HW_source_other_'+tp
        p = data[p_col] == '4'
        q = data[q_col].notnull()
        if not (~p | q).all():
            display(data[~(~p | q)][[ID, p_col, q_col]])
            display("verify_ede_implications: other hw source -> hw source other not null")
            # set_trace()

        # other weight control behavior 99 days <-> 0 episodes
        # days <= episodes
        p_col = colname+'_other_beh_day_'+tp
        q_col = colname+'_other_beh_epi_'+tp
        p = (data[p_col] == '99') | data[p_col].isnull()
        q = (data[q_col] == '00') | data[q_col].isnull()
        if not ((~p | q) & (~q | p)).all():
            display(data[~((~p | q) & (~q | p))][[ID, p_col, q_col]])
            display("verify_ede_implications: 99 days <-> 00 episodes")
            # set_trace()
        cond1 = (data[p_col].replace('99', np.nan).astype(float) <= data[q_col].astype(float)) | data[[p_col,q_col]].isnull().any(axis=1)
        cond2 = (data[p_col] == '99') | data[p_col].isnull()
        if not (cond1 | cond2).all():
            display(data[~(cond1 | cond2)][[ID, p_col, q_col]])
            display("verify_ede_implications: days <= episodes")
            # set_trace()

        # # male <-> no period (999)
        # p_col = colname+'_Mens_male_'+tp
        # q_col = colname+'_period_mo0to3_'+tp
        # r_col = colname+'_period_mo0to6_'+tp
        # p = data[p_col] == '1'
        # q = data[q_col] == '999'
        # r = data[r_col] == '999'
        # if not ((~p | (q & r)) & (~(q & r) | p)).all():
        #     display(data[~((~p | (q & r)) & (~(q & r) | p))][[ID, p_col, q_col, r_col]])
        #     display("verify_ede_implications: male -> 999 period")
        #     # set_trace()

        # # male -> 999 [norm, irreg, prim, sec]
        # p_col = colname+'_Mens_male_'+tp
        # q_col = colname+'_Mens_norm_'+tp
        # r_col = colname+'_Mens_irreg_'+tp
        # s_col = colname+'_Prim_amen_'+tp
        # t_col = colname+'_Sec_amen_'+tp
        # p = data[p_col] == '1'
        # q = data[q_col] == '999'
        # r = data[r_col] == '999'
        # s = data[s_col] == '999'
        # t = data[t_col] == '999'
        # if not (~p | (q & r & s & t)).all():
        #     display(data[~(~p | (q & r & s & t))][[ID, p_col, q_col, r_col, s_col, t_col]])
        #     display("verify_ede_implications: male -> 999 menstruation vars")
        #     # set_trace()

        # # male <-> 999 pregnant, gyno, birthcont
        # p_col = colname+'_Mens_male_'+tp
        # q_cols = [colname+i+tp for i in ['_Preg_', '_Gyno_', '_Birth_Cont_']]
        # p = data[p_col] == '1'
        # q = (data[q_cols] == '999').all(axis=1)
        # if not ((~p | q) & (~q | p)).all():
        #     display(data[~((~p | q) & (~q | p))][[ID, p_col, *q_cols]])
        #     display("verify_ede_implications: male <-> 999 pregnant, gyno, brith cont")
        #     # set_trace()

        # # female -> only one of [norm, irreg, prim, sec] checked or none at all
        # p_col = colname+'_Mens_male_'+tp
        # q_cols = [colname + i + tp for i in ['_Mens_norm_', '_Mens_irreg_', '_Prim_amen_', '_Sec_amen_']]
        # p = data[p_col] == '0'
        # q = data[q_cols].astype(float).sum(axis=1) <= 1
        # if not (~p | q).all():
        #     display(data[~(~p | q)][[ID, colname+'_period_mo0to3_'+tp, p_col, *q_cols]])
        #     display("verify_ede_implications: female -> only one of [norm, irreg, prim, sec] checked or none at all")
        #     # set_trace()

        # # if pregnant -> no period (no period every month)
        # p_col = colname+'_Preg_'+tp
        # q_col = colname+'_period_mo0to3_'+tp
        # r_col = colname+'_period_mo0to6_'+tp
        # p = data[p_col] == '1'
        # q = data[q_col].astype(float) < 3
        # r = data[r_col].astype(float) < 6
        # if not (~p | (q & r)).all():
        #     display(data[~(~p | (q & r))][[ID, p_col, q_col, r_col]])
        #     display("verify_ede_implications: pregnant -> no regular period")
        #     # set_trace()
            
    def score(self, data):
        data = data.copy()
        EDE_SUBSCALES = self.ede_subscales
        colname = self.colname
        tp = self.tp
        # get subscale scores
        for key in EDE_SUBSCALES:
            subscale_cols = EDE_SUBSCALES[key]
            temp = data[[col.name+'_'+tp for col in subscale_cols]].replace('9', np.nan).astype(float)
            # if more than half complete
            def calculate_subscale(ser):
                if ser.isna().sum() / len(ser) < 0.5:
                    return ser.mean(skipna=True)
                else:
                    return np.nan
            data[colname+'_'+key+'_sub_'+tp] = temp.apply(calculate_subscale, axis=1)
            data[colname+'_'+key+'_sub_missing_'+tp] = temp.isnull().sum(axis=1) / len(temp.columns)
        # get global scores
        data[colname+'_global_'+tp] = data[
            [colname+'_'+key+'_sub_'+tp for key in EDE_SUBSCALES]
        ].mean(axis=1, skipna=False)
        cols = [col.name+'_'+tp for key in EDE_SUBSCALES for col in EDE_SUBSCALES[key]]
        data[colname+'_global_missing_'+tp] = data[cols].isnull().sum(axis=1) / len(cols)
        # update cols
        self.get_cols(data)
        return data
        
    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        EDE_COLGRPS = self.ede_colgrps
        EDE_COLS = self.ede_cols
        tp = self.tp
        # verify processing all columns
        diff = set(cols) - set([col.name+'_'+tp for colgrp in EDE_COLGRPS for col in EDE_COLGRPS[colgrp].columns])
        if diff != set():
            display(diff)
            display("process: not all cols processed")
            # set_trace()
        # clean
        data = self.clean(data,show=show)
        # verify implications
        self.verify_implications(data)
        # verify
        for col in EDE_COLS:
            col = EDE_COLS[col]
            self.verify(data, [col.name+'_'+tp], set_range=col.range, grp=grp)
        # score
        data = self.score(data)
        # show nan
        if show_nan: self.show_nan(data)
        return data

class ScoreDate(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)

    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # get cols
        self.get_cols(data)
        cols = self.cols
        try:
            assert len(cols) == 1 and isinstance(cols, pd.Index)
        except AssertionError:
            cols = pd.Index([self.colname])
            # print(cols, self.colname)
            assert len(cols) == 1 and isinstance(cols, pd.Index)
        col = cols[0]
        # clean
        data = self.clean(data,show=show)
        # convert to date
        errs = []
        for i in data[col].index:
            try:
                pd.to_datetime(data[col].loc[i])
            except ValueError as e:
                errs.append(i)
        if len(errs) == 0:
            data[col].apply(pd.to_datetime)
        else:
            display(data.loc[errs])
            display('Invalid date')
        
        return data

class ScoreHWLog(Score):
    def __init__(self, tp, arm, colname, cleaners):
        super().__init__(tp, arm, colname, cleaners)

    def process(self, data, show_nan, show, grp):
        data = data.copy()
        # clean
        data = self.clean(data,show=show)

        # verify one to one
        assert not data["Intake_number"].duplicated().all()
        assert not data["ID_number"].duplicated().all()

        dfs = []
        # change type
        data['Session'] = data['Session'].astype(int)
        for (ses,df) in data.groupby('Session'):
            df = df.copy()
            # drop site & session
            df = df.drop(columns=['Session'])
            # rename
            d = {col: col+'_ses'+str(ses) if col != 'ID_number' and col != 'Intake_number' else col for col in df.columns}
            df = df.rename(columns=d)
            # add to list
            dfs.append(df)

        # merge
        for i,df in enumerate(dfs):
            if i == 0:
                df0 = df
            else:
                df0 = pd.merge(
                    df0,
                    df,
                    how='outer',
                    on=['ID_number', 'Intake_number']
                )

        assert len(df0) == len(data[ID].unique())
        data = df0

        # verify Y, N
        self.verify(data, data.columns[data.columns.str.startswith('Session_videotaped')], Range(rtype='discrete', set_={'Y', 'N'}), grp=grp)
        
        return data
    
class ScoreArgs:
    def __init__(self, colname, cleaners, **kwargs):
        assert isinstance(colname, str)
        assert isinstance(cleaners, list)
        assert isinstance(kwargs, dict)
        self.colname = colname
        self.cleaners = cleaners
        self.kwargs = kwargs
        