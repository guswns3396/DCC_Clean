from ..global_vars import INTAKE, ID, PID, pd, np
from ..Cleaning.Cleaner import Cleaner
from ..Cleaning.EDEColumn import setup_ede
from ..Cleaning.Score import \
    ScoreArgs, ScoreIdentifier, ScoreCheckOutsideTreatment, ScoreYBC, ScoreCYBOCS, ScoreBDI, ScoreBAI, ScoreHRQ, \
    ScorePvAN, ScoreSDQ, ScoreEDE, ScoreCOVID, ScoreCOVIDWeb, ScoreTSPE, ScoreCET, ScoreCES, ScoreDate, ScoreHWLog

from .EDE_SCALES import SUBSCALES, COLGRPS
from .cleaner_functions import clean_id_format, clean_ede_hw_only, clean_ede_menstruation, \
    convert_txt2num, convert_kg2lb, clean_eot_immediate, check_outside_no, clean_duplicate_unknown_id, rename_col

EDE_COLS, EDE_COLGRPS, EDE_SUBSCALES = setup_ede(SUBSCALES, COLGRPS)

SCOREARGS_DICT = {
    'child_int': {
        '3mo': (
            'data/Child_3mo_within_Tx_interview_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        INTAKE,
                        []
                    )
                ),
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        []
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreCheckOutsideTreatment,
                    ScoreArgs(
                        'Check',
                        [Cleaner('function', func_=check_outside_no, kwargs_={'idx':[54,55]})] # assume no is checked for UC-1018, UC-1017
                    )
                ),
                (
                    ScoreYBC,
                    ScoreArgs(
                        'YBC',
                        [
                            Cleaner( # shift for reverse coding
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        YBC1_3mo    YBC2_3mo    YBC3_3mo    YBC4_3mo    YBC5_3mo
                                        YBC6_3mo    YBC7_3mo    YBC8_3mo    YBC9_3mo    YBC10_3mo
                                        YBC11_3mo   YBC12_3mo   YBC13_3mo   YBC14_3mo   YBC15_3mo
                                        YBC16_3mo   YBC17_3mo   YBC18_3mo   YBC19_3mo
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,5+1)}
                            )
                        ]
                    )
                ),
                (
                    ScoreCYBOCS,
                    ScoreArgs(
                        'CYBOCS',
                        []
                    )
                ),
                (
                    ScoreEDE,
                    ScoreArgs(
                        'EDE',
                        [
                            # replace
                            Cleaner('replace', dict_={'00':'0'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['importance_of_shape'].columns]),
                            Cleaner('replace', dict_={'999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['flat_stomach'].columns]),
                            Cleaner('replace', dict_={'0':'00','999':'99'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['bulimic_episodes_days'].columns]),
                            Cleaner('replace', dict_={'0':'000'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['bulimic_episodes_epi'].columns]),
                            Cleaner('replace', dict_={'999':'99','0':'00','666':'99'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['continuous_OBE_free'].columns]),
                            Cleaner('replace', dict_={'999':'9','666':'9'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['OBE_avg_week'].columns]),
                            Cleaner('replace', dict_={'999':'9','666':'9'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['features_binge_eating'].columns]),
                            Cleaner('replace', dict_={'999':np.nan,'9':np.nan,'666':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['distress_binge_eating'].columns]),
                            Cleaner('replace', dict_={'999':'9','99':'9'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['dietary_restriction_out_bulimic'].columns]),
                            Cleaner('replace', dict_={'0':'000'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['self_induced_vomiting'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['laxative_misuse_epi'].columns]), 
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['laxative_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['laxative_type'].columns]), 
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['diuretic_misuse_epi'].columns]), 
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['diuretic_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['diuretic_type'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['diet_pill_misuse_epi'].columns]),
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['diet_pill_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['diet_pill_type'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['driven_exercising_days'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['driven_exercising_time'].columns]),
                            Cleaner('replace', dict_={'0':'99','00':'99','000':'99','999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['other_weight_control_behavior_day'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['other_weight_control_behavior_epi'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['other_weight_control_behavior_sp'].columns]),
                            Cleaner('replace', dict_={'999':'99','000':'0'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['absence_of_weight_control_behavior'].columns]),
                            Cleaner('replace', dict_={'9999':'9'}, cols_=[col.name+'_3mo' for col in EDE_COLGRPS['maintained_low_weight'].columns]),
                            Cleaner('replace', dict_={'yes':'1', 'Yes':'1', 'Y':'1', 'y':'1'}, cols_=['EDE_Mens_male_3mo']),
                            Cleaner('replace', dict_={'no':'0', 'No':'0', 'N':'0', 'n':'0'}, cols_=['EDE_Mens_male_3mo']),

                            Cleaner('overwrite', idx_=[7,67], val_=['00','3.5'], col_='EDE_Exercise_days_3mo'), # fix to just numeric from string
                            Cleaner('overwrite', idx_=[7], val_=['00'], col_='EDE_Exercise_epi_3mo'), # fix to just numeric from string
                            Cleaner('overwrite', idx_=[7], val_=['00'], col_='EDE_Exercise_mo2_3mo'), # fix to just numeric from string
                            Cleaner('overwrite', idx_=[7], val_=['00'], col_='EDE_Exercise_mo3_3mo'), # fix to just numeric from string
                            Cleaner('overwrite', idx_=[7], val_=['00'], col_='EDE_Exercise_mo4to6_3mo'), # fix to just numeric from string
                            Cleaner('overwrite', idx_=[48], val_=['124.45'], col_='EDE_Wt_lb_3mo'), # fix to just numeric from string
                            Cleaner('overwrite', idx_=[48], val_=['63.62'], col_='EDE_Height_in_3mo'), # fix to just numeric from string
                            Cleaner('overwrite', idx_=[67], val_=['3.5'], col_='EDE_other_beh_day_3mo'), # fix to just numeric from string
                            *[
                                Cleaner('overwrite', idx_=[20,21,35,36,51,54,55], val_=['9']*7, col_=col) for col in [
                                'EDE_Eat_rapid_3mo', 'EDE_Uncomf_full_3mo', 'EDE_Lg_amt_3mo', 'EDE_Eat_alone_3mo', 'EDE_Disgusted_3mo', 'EDE_Distress_3mo'
                                ]
                            ], # < 12 OBE episodes -> 9 BED module vars for UC-1020, 1021, 1014, 1003, 1019, 1018, 1017
                            Cleaner('overwrite', idx_=[61,62], val_=['1','2'], col_='EDE_Laxative_Taken_3mo'), # fix to just numeric from string
                            Cleaner('overwrite', idx_=[62], val_=['1'], col_='EDE_Dietpill_Taken_3mo'), # fix to just numeric from string
                            Cleaner('overwrite', idx_=[35], val_=['99'], col_='EDE_Free_beh_3mo'), # fix to just numeric from string
                            Cleaner('overwrite', idx_=[31], val_=['0'], col_='EDE_Restraint_eat_TOT_3mo'), # fix to match max <= TOT <= control + w/s
                            Cleaner('overwrite', idx_=[17], val_=['3'], col_='EDE_Empty_stom_TOT_3mo'), # fix to match max <= TOT <= control + w/s
                            Cleaner('overwrite', idx_=[67], val_=['3.5'], col_='EDE_other_beh_epi_3mo'), # fix to match days <= episodes
                            Cleaner('overwrite', idx_=[55], val_=['21.6'], col_='EDE_BMI_3mo'), # get correct BMI
                            Cleaner('overwrite', idx_=[35], val_=['1'], col_='EDE_Avoidance_eat_TOT_3mo'), # fix to match max <= TOT <= control + w/s
                            Cleaner('overwrite', idx_=[35], val_=['1'], col_='EDE_Empty_stom_TOT_3mo'), # fix to match max <= TOT <= control + w/s
                            Cleaner('overwrite', idx_=[61,62], val_=['999','999'], col_='EDE_Laxative_Taken_3mo'), # fix to match 00 episodes <-> 999 average (avg refer to months other than month 1)
                            Cleaner('overwrite', idx_=[61,62], val_=[np.nan,np.nan], col_='EDE_Laxative_Type_3mo'), # fix to match 00 episodes <-> null type (type refer to months other than month 1)
                            Cleaner('overwrite', idx_=[62], val_=['999'], col_='EDE_Dietpill_Taken_3mo'), # fix to match 00 episodes <-> 999 average (avg refer to months other than month 1)
                            Cleaner('overwrite', idx_=[62], val_=[np.nan], col_='EDE_Dietpill_Type_3mo'), # fix to match 00 episodes <-> null type (type refer to months other than month 1)
                            Cleaner('overwrite', idx_=[3], val_=['99'], col_='EDE_Free_beh_3mo'), # scored wrong 23 => 99
                            Cleaner('function', func_=convert_txt2num, kwargs_={'col':'EDE_Desired_wt_lb_3mo'}), # convert text to number
                            Cleaner('function', func_=convert_kg2lb, kwargs_={'col':'EDE_Desired_wt_lb_3mo','site':'UC'}), # convert kg to lb for all UC
                            Cleaner('function', func_=convert_txt2num, kwargs_={'col':'EDE_EBW_3mo'}), # convert text to number
                            Cleaner('function', func_=clean_ede_hw_only, kwargs_={'idx': [68, 71],'cols':[col+'_3mo' for col in EDE_COLS]}) # convert 999 to np.nan
                        ],
                        ede_subscales=EDE_SUBSCALES,
                        ede_colgrps=EDE_COLGRPS,
                        ede_cols=EDE_COLS
                    )
                )
            ]
        ),
        'eot': (
            'data/Child_EOT_interview_2022.11.02.csv',
            [
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreCOVID,
                    ScoreArgs(
                        'Covid19',
                        []
                    )
                ),
                (
                    ScoreCheckOutsideTreatment,
                    ScoreArgs(
                        'Check',
                        [
                            Cleaner('function', func_=check_outside_no, kwargs_={'idx':[52]}) # assume no is checked for UC-1026
                        ]
                    )
                ),
                (
                    ScoreCYBOCS,
                    ScoreArgs(
                        'CYBOCS',
                        []
                    )
                ),
                (
                    ScoreYBC,
                    ScoreArgs(
                        'YBC',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        YBC1_eot    YBC2_eot    YBC3_eot    YBC4_eot    YBC5_eot
                                        YBC6_eot    YBC7_eot    YBC8_eot    YBC9_eot    YBC10_eot
                                        YBC11_eot   YBC12_eot   YBC13_eot   YBC14_eot   YBC15_eot
                                        YBC16_eot   YBC17_eot   YBC18_eot   YBC19_eot
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,5+1)}
                            )
                        ]
                    )
                ),
                (
                    ScoreEDE,
                    ScoreArgs(
                        'EDE',
                        [
                            Cleaner('replace', dict_={'00':'0'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['importance_of_shape'].columns]),
                            Cleaner('replace', dict_={'999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['flat_stomach'].columns]),
                            Cleaner('replace', dict_={'0':'00','999':'99'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['bulimic_episodes_days'].columns]),
                            Cleaner('replace', dict_={'0':'000'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['bulimic_episodes_epi'].columns]),
                            Cleaner('replace', dict_={'999':'99','0':'00','666':'99'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['continuous_OBE_free'].columns]),
                            Cleaner('replace', dict_={'999':'9','666':'9'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['OBE_avg_week'].columns]),
                            Cleaner('replace', dict_={'999':'9','666':'9'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['features_binge_eating'].columns]),
                            Cleaner('replace', dict_={'999':np.nan,'9':np.nan,'666':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['distress_binge_eating'].columns]),
                            Cleaner('replace', dict_={'999':'9','99':'9'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['dietary_restriction_out_bulimic'].columns]),
                            Cleaner('replace', dict_={'0':'000'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['self_induced_vomiting'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['laxative_misuse_epi'].columns]), 
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['laxative_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['laxative_type'].columns]), 
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['diuretic_misuse_epi'].columns]), 
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['diuretic_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['diuretic_type'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['diet_pill_misuse_epi'].columns]),
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['diet_pill_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['diet_pill_type'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['driven_exercising_days'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['driven_exercising_time'].columns]),
                            Cleaner('replace', dict_={'0':'99','00':'99','000':'99','999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['other_weight_control_behavior_day'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['other_weight_control_behavior_epi'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['other_weight_control_behavior_sp'].columns]),
                            Cleaner('replace', dict_={'999':'99','000':'0'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['absence_of_weight_control_behavior'].columns]),
                            Cleaner('replace', dict_={'9999':'9'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['maintained_low_weight'].columns]),
                            Cleaner('replace', dict_={'666':'9'}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['dissatisfaction_with_weight'].columns]),
                            Cleaner('replace', dict_={'66':np.nan}, cols_=[col.name+'_eot' for col in EDE_COLGRPS['dissatisfaction_with_weight'].columns]),
                            Cleaner('replace', dict_={'yes':'1', 'Yes':'1', 'Y':'1', 'y':'1'}, cols_=['EDE_Mens_male_eot']),
                            Cleaner('replace', dict_={'no':'0', 'No':'0', 'N':'0', 'n':'0'}, cols_=['EDE_Mens_male_eot']),

                            Cleaner('overwrite', idx_=[103], val_=['3/25/2021'], col_='EDE_DateHW_eot'), # fix 3/35/2021 to 3/25/2021
                            *[
                                Cleaner('overwrite', idx_=[21,36,37,40,45,47,48,70], val_=['9']*8, col_=col) for col in [
                                'EDE_Eat_rapid_eot', 'EDE_Uncomf_full_eot', 'EDE_Lg_amt_eot', 'EDE_Eat_alone_eot', 'EDE_Disgusted_eot', 'EDE_Distress_eot'
                                ]
                            ], # < 12 OBE episodes -> 9 BED module vars for UC-1017, 1010, 1007, 1031, 1014, 1008, 1009, 1043
                            Cleaner('overwrite', idx_=[21], val_=[np.nan], col_='EDE_Dietpill_Type_eot'), # fix type 00 => nan
                            Cleaner('overwrite', idx_=[109], val_=[np.nan], col_='EDE_Midmorn_snack_eot'),
                            Cleaner('overwrite', idx_=[48,65], val_=['0','9'], col_='EDE_OBE_avg_eot'),
                            Cleaner('overwrite', idx_=[17], val_=['1.3'], col_='EDE_Laxative_Taken_eot'),
                            Cleaner('overwrite', idx_=[63], val_=['999'], col_='EDE_period_mo0to3_eot'),
                            Cleaner('overwrite', idx_=[63], val_=['999'], col_='EDE_period_mo0to6_eot'),
                            Cleaner('overwrite', idx_=[45], val_=['12'], col_='EDE_Free_beh_eot'),
                            Cleaner('overwrite', idx_=[31], val_=['0'], col_='EDE_Fear_LOC_eot'),
                            Cleaner('overwrite', idx_=[46], val_=['19.4'], col_='EDE_BMI_eot'),
                            Cleaner('overwrite', idx_=[73], val_=['00'], col_='EDE_other_beh_epi_eot'),
                            Cleaner('overwrite', idx_=[45], val_=['1'], col_='EDE_Avoidance_eat_TOT_eot'),
                            Cleaner('overwrite', idx_=[10], val_=['999'], col_='EDE_Laxative_Taken_eot'),
                            Cleaner('function', func_=convert_txt2num, kwargs_={'col':'EDE_Desired_wt_lb_eot'}),
                            Cleaner('function', func_=convert_txt2num, kwargs_={'col':'EDE_Wt_lb_eot'}),
                            Cleaner('function', func_=convert_txt2num, kwargs_={'col':'EDE_EBW_eot'}),
                            Cleaner('function', func_=clean_ede_menstruation, kwargs_={
                                'mens_col': 'EDE_Menstration' + '_eot',
                                'period03': 'EDE_period_mo0to3'+'_eot',
                                'male_col': 'EDE_Mens_male'+'_eot',
                                'norm_col': 'EDE_Mens_norm'+'_eot',
                                'irreg_col': 'EDE_Mens_irreg'+'_eot',
                                'primam_col': 'EDE_Prim_amen'+'_eot',
                                'secam_col': 'EDE_Sec_amen'+'_eot',
                                'bircont_col': 'EDE_Birth_Cont'+'_eot'
                                })
                        ],
                        ede_subscales=EDE_SUBSCALES,
                        ede_colgrps=EDE_COLGRPS,
                        ede_cols=EDE_COLS
                    )
                ),
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        [Cleaner('function', func_=clean_eot_immediate, kwargs_={'idcols':[ID, INTAKE], 'datecol': 'Date', 'covidcol': 'Covid19_imm_post_eot'})]
                    )
                ),
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        INTAKE,
                        []
                    )
                )
            ]
        ),
        '6moFU': (
            'data/Child_6moFUint_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        INTAKE,
                        [
                            Cleaner('drop', idx_=[91,92,93,94]), # duplicates
                            Cleaner('overwrite', idx_=[75], val_=['SU-122'], col_='Intake_number'),
                            Cleaner('overwrite', idx_=[60], val_=['UC-105'], col_='Intake_number')
                        ]
                    )
                ),
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        [Cleaner('overwrite', idx_=[75], val_=['SU-1064'], col_='ID_number')]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreCheckOutsideTreatment,
                    ScoreArgs(
                        'Check',
                        [Cleaner('function', func_=check_outside_no, kwargs_={'idx':[85]})]
                    )
                ),
                (
                    ScoreYBC,
                    ScoreArgs(
                        'YBC',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        YBC1_6moFU    YBC2_6moFU    YBC3_6moFU    YBC4_6moFU    YBC5_6moFU
                                        YBC6_6moFU    YBC7_6moFU    YBC8_6moFU    YBC9_6moFU    YBC10_6moFU
                                        YBC11_6moFU   YBC12_6moFU   YBC13_6moFU   YBC14_6moFU   YBC15_6moFU
                                        YBC16_6moFU   YBC17_6moFU   YBC18_6moFU   YBC19_6moFU
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,5+1)}
                            )
                        ]
                    )
                ),
                (
                    ScoreCYBOCS,
                    ScoreArgs(
                        'CYBOCS',
                        []
                    )
                ),
                (
                    ScoreEDE,
                    ScoreArgs(
                        'EDE',
                        [
                            Cleaner('replace', dict_={'00':'0'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['importance_of_shape'].columns]),
                            Cleaner('replace', dict_={'999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['flat_stomach'].columns]),
                            Cleaner('replace', dict_={'0':'00','999':'99'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['bulimic_episodes_days'].columns]),
                            Cleaner('replace', dict_={'0':'000'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['bulimic_episodes_epi'].columns]),
                            Cleaner('replace', dict_={'999':'99','0':'00','666':'99'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['continuous_OBE_free'].columns]),
                            Cleaner('replace', dict_={'999':'9','666':'9'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['OBE_avg_week'].columns]),
                            Cleaner('replace', dict_={'999':'9','666':'9'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['features_binge_eating'].columns]),
                            Cleaner('replace', dict_={'999':np.nan,'9':np.nan,'666':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['distress_binge_eating'].columns]),
                            Cleaner('replace', dict_={'999':'9','99':'9'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['dietary_restriction_out_bulimic'].columns]),
                            Cleaner('replace', dict_={'0':'000'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['self_induced_vomiting'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['laxative_misuse_epi'].columns]), 
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['laxative_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['laxative_type'].columns]), 
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['diuretic_misuse_epi'].columns]), 
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['diuretic_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['diuretic_type'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['diet_pill_misuse_epi'].columns]),
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['diet_pill_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['diet_pill_type'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['driven_exercising_days'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['driven_exercising_time'].columns]),
                            Cleaner('replace', dict_={'0':'99','00':'99','000':'99','999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['other_weight_control_behavior_day'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['other_weight_control_behavior_epi'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['other_weight_control_behavior_sp'].columns]),
                            Cleaner('replace', dict_={'999':'99','000':'0'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['absence_of_weight_control_behavior'].columns]),
                            Cleaner('replace', dict_={'9999':'9'}, cols_=[col.name+'_6moFU' for col in EDE_COLGRPS['maintained_low_weight'].columns]),
                            Cleaner('replace', dict_={'yes':'1', 'Yes':'1', 'Y':'1', 'y':'1'}, cols_=['EDE_Mens_male_6moFU']),
                            Cleaner('replace', dict_={'no':'0', 'No':'0', 'N':'0', 'n':'0'}, cols_=['EDE_Mens_male_6moFU']),
                            Cleaner('replace', dict_={'missing':np.nan}, cols_=['EDE_Height_in_6moFU','EDE_Wt_lb_6moFU','EDE_EBW_6moFU','EDE_BMI_6moFU']),
                            *[
                                Cleaner('overwrite', idx_=[5,6], val_=['9']*2, col_=col) for col in [
                                'EDE_Eat_rapid_6moFU', 'EDE_Uncomf_full_6moFU', 'EDE_Lg_amt_6moFU', 'EDE_Eat_alone_6moFU', 'EDE_Disgusted_6moFU', 'EDE_Distress_6moFU'
                                ]
                            ],
                            *[
                                Cleaner('overwrite', idx_=[55], val_=[np.nan], col_=col) for col in [
                                'EDE_Fear_gain_6moFU', 'EDE_Fat_6moFU', 'EDE_Lose_wt_6moFU', 'EDE_Wt_gain_6moFU', 'EDE_Import_contol_6moFU', 'EDE_Reg_fat_6moFU'
                                ]
                            ],
                            Cleaner('overwrite', idx_=[6], val_=[np.nan], col_='EDE_Desired_wt_lb_6moFU'),
                            Cleaner('overwrite', idx_=[55], val_=[np.nan], col_='EDE_Vig_shp_6moFU'),
                            Cleaner('overwrite', idx_=[55], val_=[np.nan], col_='EDE_Body_comp_6moFU'),
                            Cleaner('overwrite', idx_=[78], val_=['1'], col_='EDE_Restraint_eat_TOT_6moFU'),
                            Cleaner('overwrite', idx_=[16, 53], val_=['0','0'], col_='EDE_Empty_stom_TOT_6moFU'),
                            Cleaner('overwrite', idx_=[76], val_=['2'], col_='EDE_Food_avoid_TOT_6moFU'),
                            Cleaner('overwrite', idx_=[27], val_=['19.6'], col_='EDE_BMI_6moFU'),
                            Cleaner('overwrite', idx_=[44,50], val_=['00','00'], col_='EDE_other_beh_epi_6moFU'),
                            Cleaner('overwrite', idx_=[49], val_=['2'], col_='EDE_Food_avoid_TOT_6moFU'),
                            Cleaner('function', func_=convert_txt2num, kwargs_={'col':'EDE_Desired_wt_lb_6moFU'}),
                            Cleaner('function', func_=convert_txt2num, kwargs_={'col':'EDE_EBW_6moFU'}),
                            Cleaner('function', func_=clean_ede_menstruation, kwargs_={
                                'mens_col': 'EDE_Menstration' + '_6moFU',
                                'period03': 'EDE_period_mo0to3'+'_6moFU',
                                'male_col': 'EDE_Mens_male'+'_6moFU',
                                'norm_col': 'EDE_Mens_norm'+'_6moFU',
                                'irreg_col': 'EDE_Mens_irreg'+'_6moFU',
                                'primam_col': 'EDE_Prim_amen'+'_6moFU',
                                'secam_col': 'EDE_Sec_amen'+'_6moFU',
                                'bircont_col': 'EDE_Birth_Cont'+'_6moFU'
                                })
                        ],
                        ede_subscales=EDE_SUBSCALES,
                        ede_colgrps=EDE_COLGRPS,
                        ede_cols=EDE_COLS
                    )
                )
            ]
        ),
        '12moFU': (
            'data/Child_12moFUint_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        INTAKE,
                        [
                            Cleaner('replace', dict_={'UC-130': 'UC-1056'}, cols_=['ID_number']), # Intake and ID switched
                            Cleaner('replace', dict_={'UC-1056': 'UC-130'}, cols_=['Intake_number']), # Intake and ID switched
                        ]
                    )
                ),
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        []
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreCheckOutsideTreatment,
                    ScoreArgs(
                        'Check',
                        []
                    )
                ),
                (
                    ScoreYBC,
                    ScoreArgs(
                        'YBC',
                        [
                            Cleaner('function', func_=rename_col, kwargs_={'replace_from':'YBC22_12moFU', 'replace_to':'YBC21_12moFU'}),
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        YBC1_12moFU    YBC2_12moFU    YBC3_12moFU    YBC4_12moFU    YBC5_12moFU
                                        YBC6_12moFU    YBC7_12moFU    YBC8_12moFU    YBC9_12moFU    YBC10_12moFU
                                        YBC11_12moFU   YBC12_12moFU   YBC13_12moFU   YBC14_12moFU   YBC15_12moFU
                                        YBC16_12moFU   YBC17_12moFU   YBC18_12moFU   YBC19_12moFU
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,5+1)}
                            )
                        ]
                    )
                ),
                (
                    ScoreCYBOCS,
                    ScoreArgs(
                        'CYBOCS',
                        []
                    )
                ),
                (
                    ScoreEDE,
                    ScoreArgs(
                        'EDE',
                        [
                            Cleaner('replace', dict_={'00':'0'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['importance_of_shape'].columns]),
                            Cleaner('replace', dict_={'999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['flat_stomach'].columns]),
                            Cleaner('replace', dict_={'0':'00','999':'99'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['bulimic_episodes_days'].columns]),
                            Cleaner('replace', dict_={'0':'000'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['bulimic_episodes_epi'].columns]),
                            Cleaner('replace', dict_={'999':'99','0':'00','666':'99'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['continuous_OBE_free'].columns]),
                            Cleaner('replace', dict_={'999':'9','666':'9'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['OBE_avg_week'].columns]),
                            Cleaner('replace', dict_={'999':'9','666':'9'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['features_binge_eating'].columns]),
                            Cleaner('replace', dict_={'999':np.nan,'9':np.nan,'666':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['distress_binge_eating'].columns]),
                            Cleaner('replace', dict_={'999':'9','99':'9'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['dietary_restriction_out_bulimic'].columns]),
                            Cleaner('replace', dict_={'0':'000'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['self_induced_vomiting'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['laxative_misuse_epi'].columns]), 
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['laxative_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['laxative_type'].columns]), 
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['diuretic_misuse_epi'].columns]), 
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['diuretic_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['diuretic_type'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['diet_pill_misuse_epi'].columns]),
                            Cleaner('replace', dict_={'0':'999','00':'999','000':'999'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['diet_pill_avg'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['diet_pill_type'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['driven_exercising_days'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['driven_exercising_time'].columns]),
                            Cleaner('replace', dict_={'0':'99','00':'99','000':'99','999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['other_weight_control_behavior_day'].columns]),
                            Cleaner('replace', dict_={'0':'00','000':'00','999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['other_weight_control_behavior_epi'].columns]),
                            Cleaner('replace', dict_={'0':np.nan,'000':np.nan,'999':np.nan}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['other_weight_control_behavior_sp'].columns]),
                            Cleaner('replace', dict_={'999':'99','000':'0'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['absence_of_weight_control_behavior'].columns]),
                            Cleaner('replace', dict_={'9999':'9'}, cols_=[col.name+'_12moFU' for col in EDE_COLGRPS['maintained_low_weight'].columns]),
                            Cleaner('replace', dict_={'yes':'1', 'Yes':'1', 'Y':'1', 'y':'1'}, cols_=['EDE_Mens_male_12moFU']),
                            Cleaner('replace', dict_={'no':'0', 'No':'0', 'N':'0', 'n':'0'}, cols_=['EDE_Mens_male_12moFU']),
                            Cleaner('replace', dict_={'missing':np.nan}, cols_=['EDE_Height_in_12moFU','EDE_Wt_lb_12moFU','EDE_EBW_12moFU','EDE_BMI_12moFU']),
                            Cleaner('replace', dict_={'PENDING':np.nan}, cols_=['EDE_DateHW_12moFU','EDE_Height_in_12moFU','EDE_Wt_lb_12moFU','EDE_EBW_12moFU','EDE_BMI_12moFU']),
                            Cleaner('replace', dict_={r"1/10/2020 - most recent weight taken. Family does not own a scale and is unable to see UCSF adol med or patients PMD due to COVID-19":'1/10/2020'}, cols_=['EDE_DateHW_12moFU']),
                            Cleaner('overwrite', idx_=[51], val_=['9'], col_='EDE_Soc_eat_12moFU'),
                            Cleaner('overwrite', idx_=[51], val_=['9'], col_='EDE_Eat_secret_12moFU'),
                            Cleaner('overwrite', idx_=[51], val_=['9'], col_='EDE_Guilt_12moFU'),
                            Cleaner('overwrite', idx_=[67], val_=['9'], col_='EDE_Dissat_wt_12moFU'),
                            Cleaner('overwrite', idx_=[9], val_=['9'], col_='EDE_React_weighing_12moFU'),
                            Cleaner('overwrite', idx_=[23], val_=['999'], col_='EDE_Vomit_mo2_12moFU'),
                            Cleaner('overwrite', idx_=[23], val_=['999'], col_='EDE_Vomit_mo3_12moFU'),
                            Cleaner('overwrite', idx_=[23], val_=['999'], col_='EDE_Vomit_mo4to6_12moFU'),
                            Cleaner('overwrite', idx_=[47], val_=[np.nan], col_='EDE_Wt_gain_12moFU'),
                            Cleaner('overwrite', idx_=[28], val_=[np.nan], col_='EDE_Height_in_12moFU'),
                            Cleaner('overwrite', idx_=[28], val_=[np.nan], col_='EDE_Wt_lb_12moFU'),
                            Cleaner('overwrite', idx_=[52], val_=[np.nan], col_='EDE_Weighing_12moFU'),
                            Cleaner('overwrite', idx_=[43,68], val_=['0','0'], col_='EDE_Avoidance_eat_TOT_12moFU'),
                            Cleaner('overwrite', idx_=[9], val_=['23.9'], col_='EDE_BMI_12moFU'),
                            Cleaner('overwrite', idx_=[50], val_=['6/3/2021'], col_='EDE_DateHW_12moFU'),
                            Cleaner('overwrite', idx_=[78], val_=['20.08'], col_='EDE_BMI_12moFU'), # wrong bmi
                            # Cleaner('overwrite', idx_=[68], val_=['999'], col_='EDE_OBE_epi_12moFU'),
                            # Cleaner('overwrite', idx_=[68], val_=['999'], col_='EDE_OBE_epi_mo2_12moFU'),
                            # Cleaner('overwrite', idx_=[68], val_=['999'], col_='EDE_OBE_epi_mo3_12moFU'),
                            # Cleaner('overwrite', idx_=[68], val_=['999'], col_='EDE_SBE_epi_12moFU'),
                            # Cleaner('overwrite', idx_=[68], val_=['999'], col_='EDE_SBE_epi_mo2_12moFU'),
                            # Cleaner('overwrite', idx_=[68], val_=['999'], col_='EDE_SBE_epi_mo3_12moFU'),
                            # Cleaner('overwrite', idx_=[68], val_=['999'], col_='EDE_OOE_epi_12moFU'),
                            Cleaner('function', func_=convert_txt2num, kwargs_={'col':'EDE_Desired_wt_lb_12moFU'}),
                            Cleaner('function', func_=convert_txt2num, kwargs_={'col':'EDE_Wt_lb_12moFU'}),
                            Cleaner('function', func_=convert_txt2num, kwargs_={'col':'EDE_Height_in_12moFU'}),
                            Cleaner('function', func_=convert_txt2num, kwargs_={'col':'EDE_EBW_12moFU'}),
                            Cleaner('function', func_=clean_ede_menstruation, kwargs_={
                                'mens_col': 'EDE_Menstration' + '_12moFU',
                                'period03': 'EDE_period_mo0to3'+'_12moFU',
                                'male_col': 'EDE_Mens_male'+'_12moFU',
                                'norm_col': 'EDE_Mens_norm'+'_12moFU',
                                'irreg_col': 'EDE_Mens_irreg'+'_12moFU',
                                'primam_col': 'EDE_Prim_amen'+'_12moFU',
                                'secam_col': 'EDE_Sec_amen'+'_12moFU',
                                'bircont_col': 'EDE_Birth_Cont'+'_12moFU'
                                })
                        ],
                        ede_subscales=EDE_SUBSCALES,
                        ede_colgrps=EDE_COLGRPS,
                        ede_cols=EDE_COLS
                    )
                )
            ]
        )
    },
    'child_web': {
        '3mo': (
            'data/Child_3mo_within_Tx_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        [
                            Cleaner('replace', dict_={'Duplicate': 'UC-1003'}, cols_=[ID]),
                            Cleaner('drop', idx_=[25]) # all nans
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreHRQ,
                    ScoreArgs(
                        'C_HRQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        C_HRQ1_3mo  C_HRQ2_3mo  C_HRQ3_3mo  C_HRQ4_3mo  C_HRQ5_3mo
                                        C_HRQ6_3mo  C_HRQ7_3mo  C_HRQ8_3mo  C_HRQ9_3mo  C_HRQ10_3mo
                                        C_HRQ11_3mo
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-4) if i < 4 else str(i-3) for i in range(1,6+1)}
                            )
                        ]
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                )
            ]
        ),
        'eot': (
            'data/Child_EOT_web_2022.11.02.csv',
            [
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                ),
                (
                    ScoreCOVIDWeb,
                    ScoreArgs(
                        'C_Covid19',
                        []
                    )
                ),
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        [Cleaner('function', func_=clean_eot_immediate, kwargs_={'idcols':[ID], 'datecol':'Date', 'covidcol': 'C_Covid19_imm_post_web_eot'})]
                    )
                )
            ]
        ),
        '6moFU': (
            'data/Child_6moFUweb_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        [
                            Cleaner('drop', idx_=[68]) # use Feb date
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                )
            ]
        ),
        '12moFU': (
            'data/Child_12moFUweb_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        []
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                )
            ]
        ),
        'ses1': (
            'data/Child_Session_1_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        []
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreTSPE,
                    ScoreArgs(
                        'C_TSPE',
                        []
                    )
                ),
                (
                    ScoreHRQ,
                    ScoreArgs(
                        'C_HRQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        C_HRQ1_ses1    C_HRQ2_ses1  C_HRQ3_ses1  C_HRQ4_ses1  C_HRQ5_ses1
                                        C_HRQ6_ses1    C_HRQ7_ses1  C_HRQ8_ses1  C_HRQ9_ses1  C_HRQ10_ses1
                                        C_HRQ11_ses1
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-4) if i < 4 else str(i-3) for i in range(1,6+1)}
                            )
                        ]
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                )
            ]
        ),
        'ses4': (
            'data/Child_Session_4_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        []
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreCET,
                    ScoreArgs(
                        'CET',
                        []
                    )
                ),
                (
                    ScoreCES,
                    ScoreArgs(
                        'CES',
                        []
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                )
            ]
        ),
        'ses2': (
            'data/Child_Session_2_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        [
                            Cleaner('drop', idx_=[100]) # all nan
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                )
            ]
        ),
        'ses3': (
            'data/Child_Session_3_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        []
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                )
            ]
        ),
        'ses5': (
            'data/Child_Session_5_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        []
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                )
            ]
        ),
        'ses6': (
            'data/Child_Session_6_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        []
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                )
            ]
        ),
        'ses7': (
            'data/Child_Session_7_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        [
                            Cleaner('drop', idx_=[30]), # duplicate
                            Cleaner('drop', idx_=[78]) # nan
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                )
            ]
        ),
        'ses8': (
            'data/Child_Session_8_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        [
                            Cleaner('drop', idx_=[31]) # duplicate
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        []
                    )
                ),
                (
                    ScoreBDI,
                    ScoreArgs(
                        'C_BDI',
                        []
                    )
                ),
                (
                    ScoreBAI,
                    ScoreArgs(
                        'C_BAI',
                        []
                    )
                )
            ]
        ),
    },
    'parent_web': {
        '3mo': (
            'data/Parent_3mo_within_Tx_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('drop', idx_=[90, 121]), # all nans
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_3mo'}),
                            Cleaner(
                                'replace',
                                dict_={
                                    'If-1054_02': 'UC-1054_02',
                                    'UC1056_02': 'UC-1056_02'
                                },
                                cols_=[PID+'_3mo']
                            ),
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[], 'idcol': 'P_ID_number_3mo', 'varname': 'duplicateID_parent_3mo'})
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '03042021': '03/04/2021'
                                },
                                cols_=['Date_3mo']
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_3mo  P_SDQ2_3mo  P_SDQ3_3mo  P_SDQ4_3mo  P_SDQ5_3mo
                                        P_SDQ6_3mo  P_SDQ7_3mo  P_SDQ8_3mo  P_SDQ9_3mo  P_SDQ10_3mo
                                        P_SDQ11_3mo P_SDQ12_3mo P_SDQ13_3mo P_SDQ14_3mo P_SDQ15_3mo
                                        P_SDQ16_3mo P_SDQ17_3mo P_SDQ18_3mo P_SDQ19_3mo P_SDQ20_3mo
                                        P_SDQ21_3mo P_SDQ22_3mo P_SDQ23_3mo P_SDQ24_3mo P_SDQ25_3mo
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScoreHRQ,
                    ScoreArgs(
                        'P_HRQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_HRQ1_3mo  P_HRQ2_3mo  P_HRQ3_3mo  P_HRQ4_3mo
                                        P_HRQ5_3mo  P_HRQ6_3mo  P_HRQ7_3mo  P_HRQ8_3mo
                                        P_HRQ9_3mo  P_HRQ10_3mo P_HRQ11_3mo
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-4) if i < 4 else str(i-3) for i in range(1,6+1)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                )
            ]
        ),
        'eot': (
            'data/Parent_EOT_web_2022.11.02.csv',
            [
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '7152021': '7/15/2021',
                                    '8172021': '8/17/2021',
                                    '07152021': '07/15/2021',
                                    '08172021': '08/17/2021'
                                },
                                cols_=['Date_eot']
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner( # shift for reverse coding
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_eot  P_SDQ2_eot  P_SDQ3_eot  P_SDQ4_eot  P_SDQ5_eot
                                        P_SDQ6_eot  P_SDQ7_eot  P_SDQ8_eot  P_SDQ9_eot  P_SDQ10_eot
                                        P_SDQ11_eot P_SDQ12_eot P_SDQ13_eot P_SDQ14_eot P_SDQ15_eot
                                        P_SDQ16_eot P_SDQ17_eot P_SDQ18_eot P_SDQ19_eot P_SDQ20_eot
                                        P_SDQ21_eot P_SDQ22_eot P_SDQ23_eot P_SDQ24_eot P_SDQ25_eot
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                ),
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('drop', idx_=[134, 106]), # rows with all nans
                            Cleaner('drop', idx_=[73, 145]), # wrong dates (may need to check again)
                            Cleaner('overwrite', idx_=[156,163], val_=['7/15/2021','08/17/2021'], col_='Date_eot'), # fix dates
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_eot'}), # fix invalid ids
                            Cleaner( # fix invalid ids
                                'replace',
                                dict_={
                                    '(UC-1051_01': 'UC-1051_01',
                                    'S_104001': 'SU-1040_01',
                                    'Uc-1050_02': 'UC-1050_02',
                                    'SU_1045': 'SU-1045_02'
                                },
                                cols_=[PID+'_eot']
                            ),
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[86,111], 'idcol': PID+'_eot', 'varname': 'duplicateID_parent_eot'}),
                            Cleaner('function', func_=clean_eot_immediate, kwargs_={'idcols':[PID+'_eot'], 'datecol':'Date_eot', 'covidcol': 'P_Covid19_imm_post_web_eot'}) # get immediate eot
                        ]
                    )
                )
            ]
        ),
        '6moFU': (
            'data/Parent_6moFU_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('drop', idx_=[83,84]), # invalid subject
                            Cleaner('drop', idx_=[73]), # all nans
                            Cleaner('drop', idx_=[146,147]), # use Feb dates
                            Cleaner('overwrite', idx_=[51], val_=['UC-1019_01'], col_='P_ID_number_6moFU'),
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_6moFU'}),
                            Cleaner(
                                'replace',
                                dict_={
                                    'UC1038_01': 'UC-1038_01',
                                    'Su-1064_01': 'SU-1064_01',
                                    'UC-1051-2)': 'UC-1051_02',
                                    'UC1056_01': 'UC-1056_01',
                                    'ronkasper': 'SU-1028_02',
                                    'Steve': 'UC-1018_02',
                                    'UC_1032': 'UC-1032',
                                    'UC1054_01': 'UC-1054_01'
                                },
                                cols_=[PID+'_6moFU']
                            ),
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[74], 'idcol': 'P_ID_number_6moFU', 'varname': 'duplicateID_parent_6moFU'})
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '04222020': '4/22/2020',
                                    '09182020': '09/18/2020',
                                    '06152021': '06/15/2021',
                                    '10212021': '10/21/2021',
                                    '02082022': '02/08/2022',
                                    '02272022': '02/27/2022',
                                    '04062022': '04/06/2022',
                                    'O4/21/2022': '04/21/2022',
                                    '09222022': '09/22/2022'
                                },
                                cols_=['Date_6moFU']
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_6moFU  P_SDQ2_6moFU  P_SDQ3_6moFU  P_SDQ4_6moFU  P_SDQ5_6moFU
                                        P_SDQ6_6moFU  P_SDQ7_6moFU  P_SDQ8_6moFU  P_SDQ9_6moFU  P_SDQ10_6moFU
                                        P_SDQ11_6moFU P_SDQ12_6moFU P_SDQ13_6moFU P_SDQ14_6moFU P_SDQ15_6moFU
                                        P_SDQ16_6moFU P_SDQ17_6moFU P_SDQ18_6moFU P_SDQ19_6moFU P_SDQ20_6moFU
                                        P_SDQ21_6moFU P_SDQ22_6moFU P_SDQ23_6moFU P_SDQ24_6moFU P_SDQ25_6moFU
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                )
            ]
        ),
        '12moFU': (
            'data/Parent_12moFU_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('drop', idx_=[112]), # duplicate (go with second one)
                            Cleaner('overwrite', idx_=[84], val_=['UC-1036_02'], col_='P_ID_number_12moFU'),
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_12moFU'}),
                            Cleaner(
                                'replace',
                                dict_={
                                    'UC1041_01': 'UC-1041_01',
                                    'Uc-1050_02': 'UC-1050_02',
                                    'UseIDSU-1049_01': 'SU-1049_01',
                                    'Uc1054_01': 'UC-1054_01'
                                },
                                cols_=[PID+'_12moFU']
                            ),
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[13,14], 'idcol': PID+'_12moFU', 'varname': 'duplicateID_parent_12moFU'})
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '04192019': '04/19/2019',
                                    '07052019': '07/05/2019',
                                    '12062019': '12/06/2019',
                                    '01082020': '01/08/2020',
                                    '05162022': '05/16/2022',
                                    '08282022': '08/28/2022',
                                    '10122022': '10/12/2022',
                                    '10192022': '10/19/2022'
                                },
                                cols_=['Date_12moFU']
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_12moFU  P_SDQ2_12moFU  P_SDQ3_12moFU  P_SDQ4_12moFU  P_SDQ5_12moFU
                                        P_SDQ6_12moFU  P_SDQ7_12moFU  P_SDQ8_12moFU  P_SDQ9_12moFU  P_SDQ10_12moFU
                                        P_SDQ11_12moFU P_SDQ12_12moFU P_SDQ13_12moFU P_SDQ14_12moFU P_SDQ15_12moFU
                                        P_SDQ16_12moFU P_SDQ17_12moFU P_SDQ18_12moFU P_SDQ19_12moFU P_SDQ20_12moFU
                                        P_SDQ21_12moFU P_SDQ22_12moFU P_SDQ23_12moFU P_SDQ24_12moFU P_SDQ25_12moFU
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                )
            ]
        ),
        'ses1': (
            'data/Parent_Session_1_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('drop', idx_=[127,146]), # all nans
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_ses1'}),
                            Cleaner(
                                'replace',
                                dict_={
                                    'SU_105701': 'SU-1057_01',
                                    'UC1056_01': 'UC-1056_01',
                                    'UC1056_02': 'UC-1056_02',
                                    'SU-10641_01': 'SU-1064_01',
                                    'SU_1049': 'SU-1049'
                                },
                                cols_=[PID+'_ses1']
                            ),
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[158,176,177,137,138,186,187], 'idcol': PID+'_ses1', 'varname': 'duplicateID_parent_ses1'})
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'P_Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '12/4/19x': '12/4/19',
                                    '3182020': '3/18/2020',
                                    '9252020': '9/25/2020',
                                    '12102020': '12/10/2020',
                                    '01/2102021': '01/21/2021',
                                    '03182020': '03/18/2020',
                                    '09252020': '09/25/2020'
                                },
                                cols_=['P_Date_ses1']
                            )
                        ]
                    )
                ),
                (
                    ScoreTSPE,
                    ScoreArgs(
                        'P_TSPE',
                        []
                    )
                ),
                (
                    ScoreHRQ,
                    ScoreArgs(
                        'P_HRQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_HRQ1_ses1    P_HRQ2_ses1  P_HRQ3_ses1  P_HRQ4_ses1  P_HRQ5_ses1
                                        P_HRQ6_ses1    P_HRQ7_ses1  P_HRQ8_ses1  P_HRQ9_ses1  P_HRQ10_ses1
                                        P_HRQ11_ses1
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-4) if i < 4 else str(i-3) for i in range(1,6+1)}
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_ses1  P_SDQ2_ses1  P_SDQ3_ses1  P_SDQ4_ses1  P_SDQ5_ses1
                                        P_SDQ6_ses1  P_SDQ7_ses1  P_SDQ8_ses1  P_SDQ9_ses1  P_SDQ10_ses1
                                        P_SDQ11_ses1 P_SDQ12_ses1 P_SDQ13_ses1 P_SDQ14_ses1 P_SDQ15_ses1
                                        P_SDQ16_ses1 P_SDQ17_ses1 P_SDQ18_ses1 P_SDQ19_ses1 P_SDQ20_ses1
                                        P_SDQ21_ses1 P_SDQ22_ses1 P_SDQ23_ses1 P_SDQ24_ses1 P_SDQ25_ses1
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                )
            ]
        ),
        'ses4': (
            'data/Parent_Session_4_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_ses4'}),
                            Cleaner(
                                'replace',
                                dict_={
                                    'Uc-1047_01': 'UC-1047_01',
                                    'Uc-1048_02': 'UC-1048_02',
                                    'IC-1054_02': 'UC-1054_02',
                                    'SU-053_01': 'SU-1053_01',
                                    'SU-053_02': 'SU-1053_02',
                                    'SU1055_01': 'SU-1055_01',
                                    'SU-1058_00': 'SU-1058_01'
                                },
                                cols_=[PID+'_ses4']
                            ),
                            Cleaner('drop', idx_=[145,187,124,125]), # all nans
                            Cleaner('drop', idx_=[106,107]), # duplicates invalid dates
                            # Cleaner('drop', idx_=[200]), # ses1 data transferred to ses4 (variables different)
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[138,152], 'idcol': PID+'_ses4', 'varname': 'duplicateID_parent_ses4'})
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'P_Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '9/9/190': '9/9/19',
                                    '01142021': '01/14/2021',
                                    '01/272021': '01/27/2021',
                                    '1142021': '1/14/2021'
                                },
                                cols_=['P_Date_ses4']
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_ses4  P_SDQ2_ses4  P_SDQ3_ses4  P_SDQ4_ses4  P_SDQ5_ses4
                                        P_SDQ6_ses4  P_SDQ7_ses4  P_SDQ8_ses4  P_SDQ9_ses4  P_SDQ10_ses4
                                        P_SDQ11_ses4 P_SDQ12_ses4 P_SDQ13_ses4 P_SDQ14_ses4 P_SDQ15_ses4
                                        P_SDQ16_ses4 P_SDQ17_ses4 P_SDQ18_ses4 P_SDQ19_ses4 P_SDQ20_ses4
                                        P_SDQ21_ses4 P_SDQ22_ses4 P_SDQ23_ses4 P_SDQ24_ses4 P_SDQ25_ses4
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                )
            ]
        ),
        'ses2': (
            'data/Parent_Session_2_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('overwrite', idx_=[201], val_=['UC-1054_01'], col_='P_ID_number_ses2'),
                            Cleaner('overwrite', idx_=[156], val_=['UC-1048_02'], col_='P_ID_number_ses2'),
                            Cleaner('replace', dict_={'1059-01':'SU-1059_01'}, cols_=[PID+'_ses2']),
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_ses2'}),
                            Cleaner(
                                'replace',
                                dict_={
                                    'Uc-1031_01': 'UC-1031_01',
                                    'UC-1048-1)': 'UC-1048_01',
                                    'Uc-1055_02': 'UC-1055_02',
                                    'UC1056_01': 'UC-1056_01',
                                    'U_10572': 'UC-1057_02',
                                    'UC-10540_01': 'UC-1054_01',
                                    'DSU-1045_01': 'SU-1045_01',
                                    'SU1049_01': 'SU-1049_01',
                                    'SU1052_01': 'SU-1052_01'
                                },
                                cols_=[PID+'_ses2']
                            ),
                            Cleaner('drop', idx_=[152,198,199]), # all nans,
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[133,201,202,170,171], 'idcol': PID+'_ses2', 'varname': 'duplicateID_parent_ses2'})
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'P_Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '0917-2020': '09/17/2020',
                                    '01042021': '01/04/2021',
                                    '01/22/021': '01/22/2021',
                                    '1042021': '1/04/2021'
                                },
                                cols_=['P_Date_ses2']
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_ses2  P_SDQ2_ses2  P_SDQ3_ses2  P_SDQ4_ses2  P_SDQ5_ses2
                                        P_SDQ6_ses2  P_SDQ7_ses2  P_SDQ8_ses2  P_SDQ9_ses2  P_SDQ10_ses2
                                        P_SDQ11_ses2 P_SDQ12_ses2 P_SDQ13_ses2 P_SDQ14_ses2 P_SDQ15_ses2
                                        P_SDQ16_ses2 P_SDQ17_ses2 P_SDQ18_ses2 P_SDQ19_ses2 P_SDQ20_ses2
                                        P_SDQ21_ses2 P_SDQ22_ses2 P_SDQ23_ses2 P_SDQ24_ses2 P_SDQ25_ses2
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                )
            ]
        ),
        'ses3': (
            'data/Parent_Session_3_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('drop', idx_=[124,133,196]), # rows with all nans
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_ses3'}),
                            Cleaner(
                                'replace',
                                dict_={
                                    'Uc-1048_02': 'UC-1048_02',
                                    'U-1051_02': 'UC-1051_02',
                                    'UC1056_01': 'UC-1056_01',
                                    'SO-1052_01': 'SU-1052_01',
                                    'SU1055_01': 'SU-1055_01',
                                    'SU_127': 'SU-1067'
                                },
                                cols_=[PID+'_ses3']
                            ),
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[127,128,114,115,161,197], 'idcol': PID+'_ses3', 'varname': 'duplicateID_parent_ses3'})
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'P_Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '9/4/19q': '9/4/2019',
                                    '04032020': '04/03/2020',
                                    '01112021': '01/11/2021',
                                    '4032020': '4/03/2020',
                                    '1112021': '1/11/2021'
                                },
                                cols_=['P_Date_ses3']
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_ses3  P_SDQ2_ses3  P_SDQ3_ses3  P_SDQ4_ses3  P_SDQ5_ses3
                                        P_SDQ6_ses3  P_SDQ7_ses3  P_SDQ8_ses3  P_SDQ9_ses3  P_SDQ10_ses3
                                        P_SDQ11_ses3 P_SDQ12_ses3 P_SDQ13_ses3 P_SDQ14_ses3 P_SDQ15_ses3
                                        P_SDQ16_ses3 P_SDQ17_ses3 P_SDQ18_ses3 P_SDQ19_ses3 P_SDQ20_ses3
                                        P_SDQ21_ses3 P_SDQ22_ses3 P_SDQ23_ses3 P_SDQ24_ses3 P_SDQ25_ses3
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                )
            ]
        ),
        'ses5': (
            'data/Parent_Session_5_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_ses5'}),
                            Cleaner(
                                'replace',
                                dict_={
                                    'SU=1054_01': 'SU-1054_01',
                                    'U_10562': 'UC-1056_02',
                                    'UC-1049-c': 'UC-1049_02',
                                    'UC_1034': 'UC-1034_02'
                                },
                                cols_=[PID+'_ses5']
                            ),
                            Cleaner('drop', idx_=[94,156]), # all nans
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[133,134,101,159,160], 'idcol': PID+'_ses5', 'varname': 'duplicateID_parent_ses5'})
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'P_Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '09/2402020': '09/24/2020',
                                    '10/072020': '10/07/2020',
                                    '12/3/3030': '12/3/2020',
                                    '01212021': '01/21/2021',
                                    '1212021': '1/21/2021'
                                },
                                cols_=['P_Date_ses5']
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_ses5  P_SDQ2_ses5  P_SDQ3_ses5  P_SDQ4_ses5  P_SDQ5_ses5
                                        P_SDQ6_ses5  P_SDQ7_ses5  P_SDQ8_ses5  P_SDQ9_ses5  P_SDQ10_ses5
                                        P_SDQ11_ses5 P_SDQ12_ses5 P_SDQ13_ses5 P_SDQ14_ses5 P_SDQ15_ses5
                                        P_SDQ16_ses5 P_SDQ17_ses5 P_SDQ18_ses5 P_SDQ19_ses5 P_SDQ20_ses5
                                        P_SDQ21_ses5 P_SDQ22_ses5 P_SDQ23_ses5 P_SDQ24_ses5 P_SDQ25_ses5
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                )
            ]
        ),
        'ses6': (
            'data/Parent_Session_6_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_ses6'}),
                            Cleaner(
                                'replace',
                                dict_={
                                    'Uc-1050_02': 'UC-1050_02',
                                    'SU_1056': 'SU-1056_02'
                                },
                                cols_=[PID+'_ses6']
                            ),
                            Cleaner('drop', idx_=[33,108,109,161]), # all nans
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[114,115], 'idcol': PID+'_ses6', 'varname': 'duplicateID_parent_ses6'})

                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'P_Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '9/23/': '9/23/19'
                                },
                                cols_=['P_Date_ses6']
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_ses6  P_SDQ2_ses6  P_SDQ3_ses6  P_SDQ4_ses6  P_SDQ5_ses6
                                        P_SDQ6_ses6  P_SDQ7_ses6  P_SDQ8_ses6  P_SDQ9_ses6  P_SDQ10_ses6
                                        P_SDQ11_ses6 P_SDQ12_ses6 P_SDQ13_ses6 P_SDQ14_ses6 P_SDQ15_ses6
                                        P_SDQ16_ses6 P_SDQ17_ses6 P_SDQ18_ses6 P_SDQ19_ses6 P_SDQ20_ses6
                                        P_SDQ21_ses6 P_SDQ22_ses6 P_SDQ23_ses6 P_SDQ24_ses6 P_SDQ25_ses6
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                )
            ]
        ),
        'ses7': (
            'data/Parent_Session_7_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('drop', idx_=[62,147,148]), # all nans
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_ses7'}),
                            Cleaner(
                                'replace',
                                dict_={
                                    'UC1030_01': 'UC-1030_01',
                                    'Uc-1032_01': 'UC-1032_01',
                                    'Uc-1047_01': 'UC-1047_01',
                                    'Uc-1050_02': 'UC-1050_02',
                                    'SU-1060_02a': 'SU-1060_02',
                                    'UC1056_01': 'UC-1056_01',
                                    'UC-1008UnknownParent': 'UC-1008'
                                },
                                cols_=[PID+'_ses7']
                            ),
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[42,47,48], 'idcol': PID+'_ses7', 'varname': 'duplicateID_parent_ses7'})
                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'P_Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '05/o6/2020': '05/06/2020',
                                    '05072020': '05/07/2020',
                                    '02042021': '02/04/2021',
                                    '5072020': '5/07/2020',
                                    '2042021': '2/04/2021'
                                },
                                cols_=['P_Date_ses7']
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_ses7  P_SDQ2_ses7  P_SDQ3_ses7  P_SDQ4_ses7  P_SDQ5_ses7
                                        P_SDQ6_ses7  P_SDQ7_ses7  P_SDQ8_ses7  P_SDQ9_ses7  P_SDQ10_ses7
                                        P_SDQ11_ses7 P_SDQ12_ses7 P_SDQ13_ses7 P_SDQ14_ses7 P_SDQ15_ses7
                                        P_SDQ16_ses7 P_SDQ17_ses7 P_SDQ18_ses7 P_SDQ19_ses7 P_SDQ20_ses7
                                        P_SDQ21_ses7 P_SDQ22_ses7 P_SDQ23_ses7 P_SDQ24_ses7 P_SDQ25_ses7
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                )
            ]
        ),
        'ses8': (
            'data/Parent_Session_8_web_2022.11.02.csv',
            [
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        PID,
                        [
                            Cleaner('overwrite', idx_=[117], val_=['UC-1049_01'], col_='P_ID_number_ses8'),
                            Cleaner('function', func_=clean_id_format, kwargs_={'colname':PID+'_ses8'}),
                            Cleaner(
                                'replace',
                                dict_={
                                    'Uc-1050_02': 'UC-1050_02',
                                    'Su-1064_01': 'SU-1064_01',
                                    'UC-1005_02Duplicate': 'UC-1005_02',
                                    'UC-1005_01Duplicate': 'UC-1005_01',
                                    'UC-1022_01Duplicate': 'UC-1022_01'
                                },
                                cols_=[PID+'_ses8']
                            ),
                            Cleaner('function', func_=clean_duplicate_unknown_id, kwargs_={'idx':[9,10,53], 'idcol': PID+'_ses8', 'varname': 'duplicateID_parent_ses8'})

                        ]
                    )
                ),
                (
                    ScoreDate,
                    ScoreArgs(
                        'P_Date',
                        [
                            Cleaner(
                                'replace',
                                dict_={
                                    '2/5/2020@1': '2/5/2020'
                                },
                                cols_=['P_Date_ses8']
                            )
                        ]
                    )
                ),
                (
                    ScoreSDQ,
                    ScoreArgs(
                        'P_SDQ',
                        [
                            Cleaner(
                                'shift',
                                cols_=[
                                    *(
                                        '''
                                        P_SDQ1_ses8  P_SDQ2_ses8  P_SDQ3_ses8  P_SDQ4_ses8  P_SDQ5_ses8
                                        P_SDQ6_ses8  P_SDQ7_ses8  P_SDQ8_ses8  P_SDQ9_ses8  P_SDQ10_ses8
                                        P_SDQ11_ses8 P_SDQ12_ses8 P_SDQ13_ses8 P_SDQ14_ses8 P_SDQ15_ses8
                                        P_SDQ16_ses8 P_SDQ17_ses8 P_SDQ18_ses8 P_SDQ19_ses8 P_SDQ20_ses8
                                        P_SDQ21_ses8 P_SDQ22_ses8 P_SDQ23_ses8 P_SDQ24_ses8 P_SDQ25_ses8
                                        '''.split()
                                    )
                                ],
                                shift_={str(i): str(i-1) for i in range(1,4)}
                            )
                        ]
                    )
                ),
                (
                    ScorePvAN,
                    ScoreArgs(
                        'P_PVA',
                        []
                    )
                )
            ]
        )
    }
    ,'form': {
        'HWLog': (
            'data/Height_and_Weight_Log_2022.11.02.csv',
            [
                (
                    ScoreHWLog,
                    ScoreArgs(
                        '',
                        [
                            Cleaner('replace', dict_={'y':'Y','n':'N','yes':'Y','no':'N','Yes':'Y','No':'N'}, cols_=['Session_videotaped']),
                            Cleaner('replace', dict_={'Partially':'Y'}, cols_=['Session_videotaped'])
                        ]
                    )
                ),
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        INTAKE,
                        []
                    )
                ),
                (
                    ScoreIdentifier,
                    ScoreArgs(
                        ID,
                        []
                    )
                ),
                *[(
                    ScoreDate,
                    ScoreArgs(
                        'Date_ses'+str(ses),
                        []
                    )
                ) for ses in range(1,19)]
            ]
        )
    }
}

MERGEARGS_DICT = {
    'parent_web': {
        tp: (PID + '_' + tp, ['P_SDQ', 'P_PVA'], 'duplicateID_parent_' + tp) for tp in ['3mo','eot','6moFU','12moFU'] + ['ses' + str(i) for i in range(1,9)]
    }
}

for arm in SCOREARGS_DICT:
    print(arm)
    for tp in SCOREARGS_DICT[arm]:
        print('\t'+tp)
        for tup in SCOREARGS_DICT[arm][tp][1]:
            print('\t\t',tup[0])