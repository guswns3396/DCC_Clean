from ..global_vars import pd,np
from .TimePoint import Arm, TimePoint
from functools import reduce

class Pipeline:
    def __init__(self, scoreargs_dict, mergeargs_dict):
        def verify_sad(s):
            for arm in s:
                for tp in s[arm]:
                    assert isinstance(s[arm][tp], tuple)

        def verify_mad(m):
            for arm in m:
                for tp in m[arm]:
                    assert isinstance(m[arm][tp], tuple)
                    assert len(m[arm][tp]) == 3
                
        verify_sad(scoreargs_dict)
        verify_mad(mergeargs_dict)
        
        self.sad = scoreargs_dict
        self.mad = mergeargs_dict
        
    def read_data(self, fname):
        try:
            data = pd.read_csv(fname)
        except UnicodeDecodeError:
            data = pd.read_csv(fname, encoding='latin-1')
        return data.loc[2:].copy()
        
    def make_timepoints(self):
        scoreargs_dict = self.sad
        # making objects
        arms = {}
        # iterate through each arm
        for arm in scoreargs_dict:
            tps = {}
            # iterate through each tp
            for tp in scoreargs_dict[arm]:
                score_list = []
                # read data
                data = self.read_data(scoreargs_dict[arm][tp][0])
                # iterate through each score
                for score in scoreargs_dict[arm][tp][1]:
                    # create score object & append to list
                    scoreobj = score[0]
                    scoreargs = score[1]
                    score_list.append(scoreobj(
                        tp=tp,
                        arm=arm,
                        colname=scoreargs.colname,
                        cleaners=scoreargs.cleaners,
                        **scoreargs.kwargs
                    ))
                # create tp object
                tps[tp] = TimePoint(data, tp, arm, score_list)
            # create timepoint object
            arms[arm] = Arm(arm, tps)
        self.arms = arms
    
    def run(self, show_nan=False, show=False, grp=False):
        self.make_timepoints()
        arms = self.arms
        for arm in arms:
            armobj = arms[arm]
            armobj.process(show_nan=show_nan, show=show, grp=grp)

    def merge_parents(self, show=False):

        def merge(idcol, avgcols, varcol, data, show):
            assert isinstance(avgcols, list)
            assert isinstance(idcol, str)
            assert isinstance(varcol, str)
            
            data_cor = data.copy()
            
            # groupby parent
            df = data[idcol].str.extract('(?P<ID_number>(?:SU|UC)-\d\d\d\d)_(?P<parent>0[1|2|3])')
            
            # add id & parent info to df
            data_cor = pd.concat([data_cor, df], axis=1)
            
            # get dfs according to parent (assume no parent more than 3)
            df1 = data_cor[data_cor['parent'] == '01'].drop(columns=['parent', idcol])
            df2 = data_cor[data_cor['parent'] == '02'].drop(columns=['parent', idcol])
            df3 = data_cor[data_cor['parent'] == '03'].drop(columns=['parent', idcol])
            
            # rename df columns according to parent
            for df,parent in zip([df1,df2,df3],['01','02','03']):
                d = {col: col+'_'+parent if col != 'ID_number' else col for col in df.columns}
                df.rename(columns=d, inplace=True)
            if show:
                display(df1,df2,df3)
            
            # merge
            df = pd.merge(
                df1, df2, how='outer', on='ID_number'
            )
            data_cor = pd.merge(
                df, df3, how='outer', on='ID_number'
            )
            if show:
                display(data_cor)
            
            # change first column
            first_column = data_cor.pop('ID_number')
            data_cor.insert(0, 'ID_number', first_column)
            
            # rename columns to be var_parent_timepoint
            tps = ['bl','3mo','eot','immediate_eot','6moFU','12moFU'] + ['ses'+str(i) for i in range(1,19)]
            tps = '|'.join(tps)
            df = data_cor.columns.str.extract('(?P<var>.+?)(?:_(?P<timepoint>'+tps+'))(?:_(?P<parent>\d\d))$')
            # display(pd.concat([pd.Series(data_cor.columns), df], axis=1))
            # get tp
            tp = df['timepoint'][df['timepoint'].notnull()].unique()
            try:
                if len(tp) == 1:
                    assert (df['timepoint'][df['timepoint'].notnull()] == tp[-1]).all()
                elif len(tp) == 2:
                    assert (df['timepoint'][df['timepoint'].notnull()].isin(tp)).all()
                else:
                    raise ValueError('more than 2 timepoints detected (eot, immediate eot)', tp)
            except AssertionError as e:
                print('Check if unnamed column in raw data')
                raise e
            # rename
            d = {col: row['var']+'_parent'+row['parent']+'_'+row['timepoint'] if col != 'ID_number' else col for col,(i,row) in zip(data_cor.columns,df.iterrows())}
            data_cor = data_cor.rename(columns=d)
            if show:
                display(d)
                display(data_cor)
            
            # get avg scores
            for col in avgcols:
                scorecols = data_cor.columns[data_cor.columns.str.startswith(col+'_score_parent')]
                missingcols = data_cor.columns[data_cor.columns.str.startswith(col+'_score_missing_parent')]
                if len(tp) == 1:
                    data_cor[col+'_score_'+tp[-1]] = data_cor[scorecols].mean(axis=1)
                    data_cor[col+'_score_missing_'+tp[-1]] = data_cor[missingcols].mean(axis=1)
                elif len(tp) == 2:
                    data_cor[col+'_score_immediate_eot'] = data_cor[scorecols[scorecols.str.endswith('immediate_eot')]].mean(axis=1)
                    data_cor[col+'_score_eot'] = data_cor[scorecols[~scorecols.str.endswith('immediate_eot')]].mean(axis=1)

                    data_cor[col+'_score_missing_immediate_eot'] = data_cor[missingcols[missingcols.str.endswith('immediate_eot')]].mean(axis=1)
                    data_cor[col+'_score_missing_eot'] = data_cor[missingcols[~missingcols.str.endswith('immediate_eot')]].mean(axis=1)
                else:
                    raise ValueError('more than 2 timepoints detected (eot, immediate eot)', tp)
                if show:
                    display(data_cor[[*cols, col+'_score_'+tp]])
            
            # make sure number of rows match
            ids = data[idcol].str.extract('(?P<ID_number>(?:SU|UC)-\d\d\d\d)_(?:0[1|2|3])')['ID_number']
            try:
                assert len(ids.unique()) == len(data_cor['ID_number'])
                assert set(ids) == set(data_cor['ID_number'])
            except AssertionError as e:
                display(ids, len(ids.unique()), data_cor, len(data_cor['ID_number']))
                display(data_cor[data_cor['ID_number'].duplicated()])
                display(set(ids)-set(data_cor['ID_number']), set(data_cor['ID_number'])-set(ids))
                raise e

            return data_cor

        m = self.mad
        for arm in m:
            print('ARM:', arm)
            for tp in m[arm]:
                print('\tTIMEPOINT:', tp)
                idcol = m[arm][tp][0]
                avgcols = m[arm][tp][1]
                varcol = m[arm][tp][2]
                try:
                    self.arms[arm].tps[tp].data = merge(idcol, avgcols, varcol, self.arms[arm].tps[tp].data, show=show)
                except TypeError as e:
                    print('Check if unnamed column in raw data')
                    raise e

    def combine_data(self):
        # combine all timepoints & arms
        dfs = []
        for arm in self.arms:
            for tp in self.arms[arm].tps:
                df = self.arms[arm].tps[tp].data
                # get varname format
                tps = ['bl','3mo','eot','immediate_eot','6moFU','12moFU', 'HWLog'] + ['ses'+str(i) for i in range(1,19)]
                tps = '|'.join(tps)
                arms = self.arms.keys()
                arms = '|'.join(arms)
                exp = r'^(?P<varname>.+?)(?:_(?P<arm>'+arms+'))?(?:_(?P<parent>parent0\d))?(?:_(?P<timepoint>' + tps + '))?$'
                varnames = pd.concat([pd.Series(df.columns, name='variable'), df.columns.str.extract(exp)], axis=1)

                # make sure all cols follow var_arm_parent_tp
                varnames.loc[varnames['arm'].isnull(), 'arm'] = arm
                varnames.loc[varnames['timepoint'].isnull(), 'timepoint'] = tp
                varnames = varnames.set_index('variable')
                d = {var: '_'.join(str(e) for e in varnames.loc[var][varnames.loc[var].notnull()].tolist()) if var != 'ID_number' else var for var in varnames.index}
                df = df.rename(columns=d)
                if tp != 'HWLog':
                    # make sure all cols end in tp except ID
                    d = {col: col+'_'+tp if not col.endswith(tp) and col != 'ID_number' else col for col in df.columns}
                    df = df.rename(columns=d)
                dfs.append(df)
        data = reduce(lambda x, y: pd.merge(x, y, on='ID_number', how='outer'), dfs)
        # see which columns do not end with tp
        idx = pd.DataFrame(
            [data.columns.str.endswith('_'+tp) for tp in (['3mo', 'eot', '6moFU', '12moFU', 'HWLog'] + ['ses'+str(i) for i in range(1,19)])],
            index=(['3mo', 'eot', '6moFU', '12moFU', 'HWLog'] + ['ses'+str(i) for i in range(1,19)])
        ).any(axis=0)
        display(data.columns[~idx])
        self.data = data

    def get_clean_bl(self, bl, cb):
        # rename vars
        bl = bl.rename(columns={
            'Intake_number': 'Intake_number_child_int_bl',
            'Rater_initials_BL':'Rater_initials_bl',
            'YBC21_BL': 'YBC21_bl',
            'Date': 'Date_child_web_bl',
            'Date_parent01_bl': 'Date_parent_web_parent01_bl',
            'Date_parent02_bl': 'Date_parent_web_parent02_bl',
            'Date_parent03_bl': 'Date_parent_web_parent03_bl',
            'C_Demo_age': 'C_Demo_age_bl',
            'KSADS_DXADD': 'KSADS_DXADD_bl',
            'KSADS_DXADD_list': 'KSADS_DXADD_list_bl',
            'EDE_Height_in_original_window_6mo': 'EDE_Height_in_original_window_child_int_6moFU',
            'EDE_Wt_lb_original_window_6mo': 'EDE_Wt_lb_original_window_child_int_6moFU',
            'EDE_Height_in_original_window_12mo': 'EDE_Height_in_original_window_child_int_12moFU',
            'EDE_Wt_lb_original_window_12mo': 'EDE_Wt_lb_original_window_child_int_12moFU'
        })
        bl = bl.rename(columns={
            'Med'+str(i)+'_ind_bl': 'Med'+str(i)+'_indication_bl' for i in range(1,11)    
        })
        var = self.get_columns(bl)
        new_var = pd.merge(
            var[var['arm'].isnull()][['variable', 'varname', 'parent', 'timepoint']],
            cb[['varname', 'form']],
            how='left',
            on='varname'
        )
        new_var = new_var[new_var['timepoint'].notnull()]
        new_var = new_var.fillna('')
        assert not new_var['form'].str.contains(',').all()
        new_var['new_variable'] = new_var[['varname','form','parent','timepoint']].apply(
            lambda x: '_'.join(list(filter(lambda y: False if y == '' else True, x))),
            axis=1
        )
        return bl.rename(columns=new_var[['variable', 'new_variable']].set_index('variable').to_dict()['new_variable'])

    def combine_bl(self, bl):
        self.data = pd.merge(
            self.data, bl,
            on='ID_number',
            how='outer'
        )
        print(len(self.data), len(bl))
        assert len(self.data) == len(bl)

    def get_columns(self, data=None):
        if data is None:
            data = self.data
        tps = ['bl','3mo','eot','immediate_eot','6moFU','12moFU', 'HWLog'] + ['ses'+str(i) for i in range(1,19)]
        tps = '|'.join(tps)
        arms = self.arms.keys()
        arms = '|'.join(arms)
        exp = r'^(?P<varname>.+?)(?:_(?P<arm>'+arms+'))?(?:_(?P<parent>parent0\d))?(?:_(?P<timepoint>' + tps + '))?$'
        return pd.concat([pd.Series(data.columns, name='variable'), data.columns.str.extract(exp)], axis=1)

    def clean_columns(self):
        data = self.data.copy()
        # drop duplicate intake numbers

        # combine duplicate ID columns & drop the extra
        data['duplicateID_child'] = data[data.columns[data.columns.str.contains('duplicateID_child')]].fillna(0).any(axis=1)
        data['duplicateID_parent'] = data[data.columns[data.columns.str.contains('duplicateID_parent')]].fillna(0).any(axis=1)
        data = data.drop(
            columns=data.columns[data.columns.str.contains('duplicateID_child') & (data.columns != 'duplicateID_child')]
        )
        data = data.drop(
            columns=data.columns[data.columns.str.contains('duplicateID_parent') & (data.columns != 'duplicateID_parent')]
        )

        # rename vars
        data = data.rename(columns={
            'Rater_initials_BL':'Rater_initials_bl',
            'YBC21_BL': 'YBC21_bl',
            'Date': 'Date_child_web_bl',
            'Date_parent01_bl': 'Date_parent_web_parent01_bl',
            'Date_parent02_bl': 'Date_parent_web_parent02_bl',
            'Date_parent03_bl': 'Date_parent_web_parent03_bl',
            'C_Demo_age': 'C_Demo_age_bl',
            'KSADS_DXADD': 'KSADS_DXADD_bl',
            'KSADS_DXADD_list': 'KSADS_DXADD_list_bl',
            'EDE_Height_in_original_window_6mo': 'EDE_Height_in_original_window_child_int_6moFU',
            'EDE_Wt_lb_original_window_6mo': 'EDE_Wt_lb_original_window_child_int_6moFU',
            'EDE_Height_in_original_window_12mo': 'EDE_Height_in_original_window_child_int_12moFU',
            'EDE_Wt_lb_original_window_12mo': 'EDE_Wt_lb_original_window_child_int_12moFU'
        })
        data = data.rename(columns={
            'Med'+str(i)+'_ind_bl': 'Med'+str(i)+'_indication_bl' for i in range(1,11)    
        })

        # clean bl date
        data['Date_child_int_bl'] = data['Date_child_web_bl']
        data['Date_child_int_bl'] = pd.to_datetime(data['Date_child_int_bl'].replace({'9/3/ 20': '9/3/2020'}))
        # make col for all telehealth vs all in person vs hybrid
        all_person = set(data[data['Date_child_int_eot'] < pd.to_datetime('3/1/2020')]['ID_number'])
        all_tele = set(data[data['Date_child_int_bl'] > pd.to_datetime('4/30/2020')]['ID_number'])
        assert (all_tele | all_person).issubset(set(data['ID_number']))
        assert all_tele & all_person == set()
        mapper = {
            **{id: '1' for id in all_person},
            **{id: '2' for id in all_tele},
            **{
                'UC-1012': '1',
                'UC-1015': '1',
                'UC-1006': '1',
                'UC-1002': '1',
                'UC-1004': '1',
                'UC-1035': '1',
                'UC-1028': '1',
                'UC-1040': '1',
                'UC-1044': '1',
                'UC-1013': '1',
                'UC-1037': '1',
                'UC-1033': '3',
                'UC-1034': '3',
                'UC-1038': '3',
                'UC-1042': '3',
                'UC-1036': '3',
                'UC-1041': '3',
                'UC-1043': '3',
                'UC-1046': '2',
                'UC-1045': '2',
                'SU-1009': '1',
                'SU-1011': '1',
                'SU-1001': '1',
                'SU-1034': '1',
                'SU-1032': '1',
                'SU-1035': '3',
                'SU-1033': '1',
                'SU-1036': '3',
                'SU-1037': '3',
                'SU-1038': '3',
                'SU-1039': '3',
                'SU-1040': '3',
                'SU-1047': '2'
            }
        }
        data['Treatment_location'] = data['ID_number'].map(mapper)

        # put ede cols in range
        grps = [
            ['EDE_Fear_LOC', 'EDE_Soc_eat', 'EDE_Eat_secret', 'EDE_Guilt', 'EDE_Discomf_expose'],
            '''
            EDE_Break
            EDE_Midmorn_snack
            EDE_Lunch
            EDE_Midaft_snack
            EDE_Eve_meal
            EDE_Eve_snack
            EDE_Noc_eat
            '''.split(),
            '''
            EDE_OBE_days
            EDE_OBE_days_mo2
            EDE_OBE_days_mo3
            EDE_SBE_days
            EDE_SBE_days_mo2
            EDE_SBE_days_mo3
            EDE_OOE_days
            '''.split(),
            '''
            EDE_OBE_epi
            EDE_OBE_epi_mo2
            EDE_OBE_epi_mo3
            EDE_SBE_epi
            EDE_SBE_epi_mo2
            EDE_SBE_epi_mo3
            EDE_OOE_epi
            '''.split(),
            ['EDE_OBE_wk_free'],
            ['EDE_OBE_avg'],
            '''
            EDE_Eat_rapid
            EDE_Uncomf_full
            EDE_Lg_amt
            EDE_Eat_alone
            EDE_Disgusted
            '''.split(),
            ['EDE_Distress'],
            ['EDE_DIET_outBN'],
            '''
            EDE_Vomit
            EDE_Vomit_mo2
            EDE_Vomit_mo3
            EDE_Vomit_mo4to6
            '''.split(),
            '''
            EDE_Laxative
            EDE_Lax_mo2
            EDE_Lax_mo3
            EDE_Lax_mo4to6
            '''.split(),
            '''
            EDE_Diuretic
            EDE_Diur_mo2
            EDE_Diur_mo3
            EDE_Diur_mo4to6
            '''.split(),
            '''
            EDE_Dietpill
            EDE_Dietp_mo2
            EDE_Dietp_mo3
            EDE_Dietp_mo4to6
            '''.split(),
            ['EDE_Exercise_days'],
            '''
            EDE_Exercise_epi
            EDE_Exercise_mo2
            EDE_Exercise_mo3
            EDE_Exercise_mo4to6
            '''.split(),
            ['EDE_other_beh_day'],
            '''
            EDE_other_beh_epi
            EDE_other_beh_mo2
            EDE_other_beh_mo3
            EDE_other_beh_mo4to6
            '''.split(),
            ['EDE_Free_beh'],
        ]
        ds = [
            {'9':np.nan},
            {'8':np.nan},
            {'00': '0', '99': '999'},
            {'000':'0'},
            {'00':np.nan,'99':'999'},
            {'9':'999'},
            {'9':'999'},
            {'9':'999'},
            {'9':'999'},
            {'000':'0','999':np.nan},
            {'00':'0'},
            {'00':'0'},
            {'00':'0'},
            {'00':'0'},
            {'00':'0'},
            {'99':np.nan},
            {'00':'0'},
            {'99':'999'}
        ]
        assert len(ds) == len(grps)
        for d,grp in zip(ds,grps):
            cols = data.columns[data.columns.str.startswith(tuple(grp))]
            data[cols] = data[cols].replace(d)

        self.data = data

    # def get_data(self, data_dict=None):
    #     df = data_dict
    #     data = self.data.copy()
        

    #     # subset necessary columns
    #     assert len(df) == len(df.drop_duplicates())
    #     acct = pd.DataFrame(
    #         index=[var for var in df['varname']],
    #         columns=['variables', 'accounted']
    #     )
    #     for var in df['varname']:
    #         varnames = data.columns[data.columns.str.contains(var)]
    #         if len(varnames) == 0:
    #             acct.loc[var, 'accounted'] = False
    #         else:
    #             acct.loc[var, 'variables'] = varnames
    #             acct.loc[var, 'accounted'] = True
    #     # assert acct['accounted'].all()
    #     variables = acct['variables'][acct['variables'].notnull()].explode().drop_duplicates().values
    #     data = data.loc[:,variables]


    #     assert not data.columns.duplicated().all()
    #     assert not data['ID_number'].duplicated().all()

    #     return data

