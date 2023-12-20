from ..global_vars import np
from ..Cleaning.Range import Range

SUBSCALES = {
    'restraint': {
        'restraint_over_eating': (
            '''
            EDE_Restraint_eat
            EDE_Restraint_eat_CON
            EDE_Restraint_eat_TOT
            '''.split(),
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'avoidance_of_eating': (
            '''
            EDE_Avoidance_eat
            EDE_Avoidance_eat_CON
            EDE_Avoidance_eat_TOT
            '''.split(),
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'empty_stomach': (
            '''
            EDE_Empty_stom
            EDE_Empty_stom_CON
            EDE_Empty_stom_TOT
            '''.split(),
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'food_avoidance': (
            '''
            EDE_Food_avoid
            EDE_Food_avoid_CON
            EDE_Food_avoid_TOT
            '''.split(),
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'dietary_rules': (
            '''
            EDE_Diet_rules
            EDE_Diet_rules_CON
            EDE_Diet_rules_TOT
            '''.split(),
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        )
    },
    'eating': {
        'preoccupation_with_food': (
            ['EDE_Preoc_food'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'fear_of_losing_control': (
            ['EDE_Fear_LOC'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]), spc_=set([9]))
        ),
        'social_eating': (
            ['EDE_Soc_eat'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]), spc_=set([9]))
        ),
        'eating_in_secret': (
            ['EDE_Eat_secret'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]), spc_=set([9]))
        ),
        'guilt_about_eating': (
            ['EDE_Guilt'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]), spc_=set([9]))
        )
    },
    'shape': {
        'dissatisfaction_with_shape': (
            ['EDE_Dissat_shp'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'preoccupation_with_shape_weight': (
            ['EDE_Preoc_shp'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'importance_of_shape': (
            ['EDE_Import_shp'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'fear_of_weight_gain': (
            ['EDE_Fear_gain'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'discomfort_seeing_body': (
            ['EDE_Discomf_body'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'discomfort_about_exposure': (
            ['EDE_Discomf_expose'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]), spc_=set([9]))
        ),
        'feeling_fat': (
            ['EDE_Fat'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'flat_stomach': (
            ['EDE_Flat_stom'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        )
    },
    'weight': {
        'dissatisfaction_with_weight': (
            ['EDE_Dissat_wt'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]), spc_=set([9]))
        ),
        'desire_to_lose_weight': (
            ['EDE_Lose_wt'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]), spc_=set([9]))
        ),
        'reaction_to_weight': (
            ['EDE_React_weighing'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]), spc_=set([9]))
        ),
        'preoccupation_with_shape_weight': (
            ['EDE_Preoc_shp'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        ),
        'importance_of_weight': (
            ['EDE_Import_wt'],
            Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
        )
    }
}
    
# column groups & ranges
COLGRPS = {
    'pattern_of_eating': (
        '''
        EDE_Break
        EDE_Midmorn_snack
        EDE_Lunch
        EDE_Midaft_snack
        EDE_Eve_meal
        EDE_Eve_snack
        EDE_Noc_eat
        '''.split(),
        Range(rtype='discrete', set_=set([i for i in range(0,6+1)]), spc_=set([8]))
    ),
    'picking': (
        ['EDE_Picking'],
        Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
    ),
    'bulimic_episodes_days': (
        '''
        EDE_OBE_days
        EDE_OBE_days_mo2
        EDE_OBE_days_mo3
        EDE_SBE_days
        EDE_SBE_days_mo2
        EDE_SBE_days_mo3
        EDE_OOE_days
        '''.split(),
        Range(rtype='discrete', set_=set([str(i) for i in range(1,28+1)]), spc_=set(['00', '99']))
    ),
    'bulimic_episodes_epi': (
        '''
        EDE_OBE_epi
        EDE_OBE_epi_mo2
        EDE_OBE_epi_mo3
        EDE_SBE_epi
        EDE_SBE_epi_mo2
        EDE_SBE_epi_mo3
        EDE_OOE_epi
        '''.split(),
        Range(rtype='discrete', set_=set([str(i) for i in range(1,999+1)]), spc_=set(['000', '777', '999']))
    ),
    'continuous_OBE_free': (
        ['EDE_OBE_wk_free'],
        Range(rtype='discrete', set_=set([str(i) for i in range(1,12+1)]), spc_=set(['00', '99']))
    ),
    'OBE_avg_week': (
        ['EDE_OBE_avg'],
        Range(rtype='discrete', set_=set([str(i) for i in range(0,7+1)]), spc_=set(['9']))
    ),
    'features_binge_eating': (
        '''
        EDE_Eat_rapid
        EDE_Uncomf_full
        EDE_Lg_amt
        EDE_Eat_alone
        EDE_Disgusted
        '''.split(),
        Range(rtype='discrete', set_=set([str(i) for i in range(0,1+1)]), spc_=set(['9']))
    ),
    'distress_binge_eating': (
        ['EDE_Distress'],
        Range(rtype='discrete', set_=set([str(i) for i in range(0,1+1)]), spc_=set(['9']))
    ),
    'dietary_restriction_out_bulimic': (
        ['EDE_DIET_outBN'],
        Range(rtype='discrete', set_=set([str(i) for i in range(0,2+1)]), spc_=set(['9']))
    ),
    'self_induced_vomiting': (
        '''
        EDE_Vomit
        EDE_Vomit_mo2
        EDE_Vomit_mo3
        EDE_Vomit_mo4to6
        '''.split(),
        Range(rtype='discrete', set_=set([str(i) for i in range(1,100+1)]), spc_=set(['000', '777', '999']))
    ),
    'laxative_misuse_epi': (
        '''
        EDE_Laxative
        EDE_Lax_mo2
        EDE_Lax_mo3
        EDE_Lax_mo4to6
        '''.split(),
        Range(rtype='continuous', start_=1, end_=200, spc_=['00'])
    ),
    'laxative_avg': (
        ['EDE_Laxative_Taken'],
        Range(rtype='continuous', start_=1, end_=200, spc_=['777', '999'])
    ),
    'laxative_type': (
        ['EDE_Laxative_Type'],
        Range(rtype='any')
    ),
    'diuretic_misuse_epi': (
        '''
        EDE_Diuretic
        EDE_Diur_mo2
        EDE_Diur_mo3
        EDE_Diur_mo4to6
        '''.split(),
        Range(rtype='continuous', start_=1, end_=200, spc_=['00'])
    ),
    'diuretic_avg': (
        ['EDE_Diuretic_Taken'],
        Range(rtype='continuous', start_=1, end_=200, spc_=['999'])
    ),
    'diuretic_type': (
        ['EDE_Diuretic_Type'],
        Range(rtype='any')
    ),
    'diet_pill_misuse_epi': (
        '''
        EDE_Dietpill
        EDE_Dietp_mo2
        EDE_Dietp_mo3
        EDE_Dietp_mo4to6
        '''.split(),
        Range(rtype='continuous', start_=1, end_=200, spc_=['00'])
    ),
    'diet_pill_avg': (
        ['EDE_Dietpill_Taken'],
        Range(rtype='continuous', start_=1, end_=200, spc_=['999'])
    ),
    'diet_pill_type': (
        ['EDE_Dietpill_Type'],
        Range(rtype='any')
    ),
    'driven_exercising_days': (
        ['EDE_Exercise_days'],
        Range(rtype='continuous', start_=1, end_=28, spc_=['00'])
    ),
    'driven_exercising_time': (
        '''
        EDE_Exercise_epi
        EDE_Exercise_mo2
        EDE_Exercise_mo3
        EDE_Exercise_mo4to6
        '''.split(),
        Range(rtype='continuous', start_=1, end_=np.inf, spc_=['00'])
    ),
    'other_weight_control_behavior_day': (
        ['EDE_other_beh_day'],
        Range(rtype='continuous', start_=1, end_=28, spc_=['99'])
    ),
    'other_weight_control_behavior_epi': (
        '''
        EDE_other_beh_epi
        EDE_other_beh_mo2
        EDE_other_beh_mo3
        EDE_other_beh_mo4to6
        '''.split(),
        Range(rtype='continuous', start_=1, end_=200, spc_=['00'])
    ),
    'other_weight_control_behavior_sp': (
        ['EDE_other_beh_sp'],
        Range(rtype='any')
    ),
    'absence_of_weight_control_behavior': (
        ['EDE_Free_beh'],
        Range(rtype='discrete', set_=set([str(i) for i in range(0,12+1)]), spc_=set(['99']))
    ),
    'desired_weight': (
        ['EDE_Desired_wt_lb'],
        Range(rtype='continuous', start_=0, end_=200, spc_=['888', '777', '666', '555'])
    ),
    'weighing': (
        ['EDE_Weighing'],
        Range(rtype='continuous', start_=0, end_=200, spc_=['777'])
    ),
    'sensitivity_to_weight': (
        ['EDE_Wt_gain'],
        Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
    ),
    'strict_control_over_eating': (
        ['EDE_Import_contol'],
        Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
    ),
    'regional_fatness': (
        ['EDE_Reg_fat'],
        Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
    ),
    'vigilance_about_shape': (
        ['EDE_Vig_shp'],
        Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
    ),
    'body_composition': (
        ['EDE_Body_comp'],
        Range(rtype='discrete', set_=set([i for i in range(0,6+1)]))
    ),
    'maintained_low_weight': (
        ['EDE_Main_Low_wt'],
        Range(rtype='discrete', set_=set([str(i) for i in range(0,2+1)]), spc_=set(['9']))
    ),
    # 'menstruation_0to3': (
    #     ['EDE_period_mo0to3'],
    #     Range(rtype='continuous', start_=0, end_=4, spc_=['999'])
    # ),
    # 'menstruation_0to6': (
    #     ['EDE_period_mo0to6'],
    #     Range(rtype='continuous', start_=0, end_=7, spc_=['999'])
    # ),
    # 'menstruation_dcc': (
    #     ['EDE_Menstration'],
    #     Range(rtype='discrete', set_=set(['1', '2', '3', '4', '5', '999']))
    # ),
    # 'menstruation_dcc_cat': (
    #     '''
    #     EDE_Mens_male
    #     EDE_Mens_norm
    #     EDE_Mens_irreg
    #     EDE_Prim_amen
    #     EDE_Sec_amen
    #     EDE_Preg
    #     EDE_Gyno
    #     EDE_Birth_Cont
    #     '''.split(),
    #     Range(rtype='discrete', set_=set(['0', '1', '999']))
    # ),
    # 'menstruation_dcc_sp': (
    #     ['EDE_Gyno_specify', 'EDE_Sec_amen_lastperiod'],
    #     Range(rtype='any')
    # ),
    'hw_source': (
        ['EDE_HW_source'],
        Range(rtype='discrete', set_=set([str(i) for i in range(1,5+1)]))
    ),
    'hw_source_other': (
        ['EDE_HW_source_other'],
        Range(rtype='any')
    ),
    'hw_gowned': (
        ['EDE_Wt_gowned'],
        Range(rtype='discrete', set_=set(['0', '1']))
    ),
    'hw_date': (
        ['EDE_DateHW'],
        Range(rtype='date', start_='1/1/2017', end_=None, spc_=[])
    ),
    'hw_bmi': (
        ['EDE_BMI'],
        Range(rtype='continuous', start_=0, end_=None, spc_=[])
    ),
    'hw_weight': (
        ['EDE_Wt_lb'],
        Range(rtype='continuous', start_=0, end_=None, spc_=[])
    ),
    'hw_height': (
        ['EDE_Height_in'],
        Range(rtype='continuous', start_=0, end_=None, spc_=[])
    ),
    'hw_ebw': (
        ['EDE_EBW'],
        Range(rtype='continuous', start_=0, end_=None, spc_=[])
    )
}
