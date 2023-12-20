import re

from ..global_vars import pd, np, ID, PID

def check_outside_no(data, show, idx):
    data_cor = data.copy()

    # check all no columns
    no_cols = data_cor.columns[data_cor.columns.str.match(r'Check_.+_no_')]
    data_cor.loc[idx, no_cols] = '1'
    return data_cor


def clean_id_format(data, show, colname):
    data_cor = data.copy()
    
    if colname == 'Intake_number':
        r1 = data[colname].str.match(r'^SU-\d\d\d$', na=False)
        r2 = data[colname].str.match(r'^UC-\d\d\d$', na=False)
    elif colname == 'ID_number':
        r1 = data[colname].str.match(r'^SU-\d\d\d\d$', na=False)
        r2 = data[colname].str.match(r'^UC-\d\d\d\d$', na=False)
    elif colname.startswith(PID):
        r1 = data[colname].str.match(r'^SU-\d\d\d\d_0\d$', na=False)
        r2 = data[colname].str.match(r'^UC-\d\d\d\d_0\d$', na=False)

    # fix having lowercase
    r = data_cor[colname].str.contains('^[su|uc]', na=False)
    data_cor[colname].loc[r] = data_cor[colname].loc[r].apply(lambda x: "{}{}".format(x[:2].upper(), x[2:]))
    
    # starts with ID
    r = data_cor[colname].str.contains('^ID', na=False)
    data_cor[colname].loc[r] = data_cor[colname].loc[r].apply(lambda x: x[2:])
    
    # get rid of whitespace
    def strip(x):
        s = ''
        for i in x:
            if i != ' ':
                s+=i
        return s
    r = data_cor[colname].str.contains(' ', na=False)
    data_cor[colname].loc[r] = data_cor[colname].loc[r].apply(strip)
    
    # replace wrong dash before \d\d\d\d
    r = data_cor[colname].str.contains(r'[_|—]\d{4}', na=False)
    def fix_dash(x):
        p = re.compile(r'[_|—]\d{4}')
        i = next(p.finditer(x)).start()
        return "{}-{}".format(x[:i], x[i+1:])
    data_cor[colname].loc[r] = data_cor[colname].loc[r].apply(fix_dash)
    
    # no site ID => I believe those are all UCSF's.
    r = data_cor[colname].str.contains(r'^\d+', na=False)
    data_cor[colname].loc[r] = data_cor[colname].loc[r].apply(lambda x: "UC-{}".format(x))
    
    # for PID
    if colname.startswith(PID):
    
        # fix only having one digit at the end
        r = data_cor[colname].str.contains(r'[^\d]\d$', na=False)
        data_cor[colname].loc[r] = data_cor[colname].loc[r].apply(lambda x: "{}{}{}".format(x[:-1], '0', x[-1]))
        
        # fix non "_" before digits
        r = data_cor[colname].str.contains(r'[^_|^\d]\d+$', na=False)
        def fix_underscore(x):
            p = re.compile(r'[^_|^\d]\d+$')
            i = next(p.finditer(x)).start()
            return "{}_{}".format(x[:i], x[i+1:])
        data_cor[colname].loc[r] = data_cor[colname].loc[r].apply(fix_underscore)

    if show:
        print('Showing Function', 'ID Format')
        display(pd.concat(
            [
                data[~r1 & ~r2][colname],
                data_cor[~r1 & ~r2][colname]
            ],
            axis=1
        ))
        
    return data_cor

def convert_kg2lb(data, show, col, site):
    data_cor = data.copy()
    # convert kg to lbs
    site = data_cor[ID].str.startswith(site+'-')
    wt = ~data_cor[col].isin(['888', '777', '666', '555'])
    data_cor.loc[data_cor[site & wt].index, col] = (data_cor.loc[data_cor[site & wt].index, col].astype(float)*2.2).astype(str)
    if show:
        print('Showing Function', 'Convert Kg to Lb')
        display(pd.concat(
            [
                data[ID],
                data[col],
                data_cor[col]
            ],
            axis=1
        ))
    return data_cor

def convert_txt2num(data, show, col):
    data_cor = data.copy()
    # convert to pure number
    data_cor.loc[:, col] = data.loc[:, col].str.extract(r'(\d+[.]*\d*)')[0]
    if show:
        print('Showing Function', 'Convert Text to Num')
        display(pd.concat(
            [
                data[ID],
                data[col],
                data[col].str.extract(r'(\d+[.]*\d*)'),
                data_cor[col]
            ],
            axis=1
        ))
    return data_cor

def clean_ede_hw_only(data, show, idx, cols):
    data_cor = data.copy()
    data_cor.loc[idx, cols] = data.loc[idx, cols].replace(['999', 999], [np.nan, np.nan])
    if show:
        print('Showing Function', 'HW only')
        display(pd.concat(
            [
                data.loc[idx,ID],
                data.loc[idx,cols],
                data_cor.loc[idx,cols]
            ],
            axis=1
        ))
    return data_cor

def clean_ede_menstruation(data, show, mens_col, period03, male_col, norm_col, irreg_col, primam_col, secam_col, bircont_col):
    data_cor = data.copy()
    for param in [period03, male_col, norm_col, irreg_col, primam_col, secam_col, bircont_col]:
        assert isinstance(param, str)
    # other columns 0 if irregular (irregular period past 3 months)
    irreg = (data_cor[period03].astype(float) == 1) | (data_cor[period03].astype(float) == 2)
    idx = data_cor[irreg].index
    data_cor.loc[idx, [norm_col, primam_col, secam_col]] = '0'
    data_cor.loc[idx, irreg_col] = '1'
    # other columns 0 if secondary amenorrhea (no period past 3 months)
    secam = data_cor[period03].astype(float) == 0
    idx = data_cor[secam].index
    data_cor.loc[idx, [norm_col, irreg_col, primam_col]] = '0'
    data_cor.loc[idx, secam_col] = '1'
    # primary amenorrhea (no menstruation at 15 yrs old)
    ...
    # no menstruation due to under 15
    ...
    # all columns 999 if male
    male = data_cor[male_col].astype(float) == 1
    idx = data_cor[male].index
    data_cor.loc[idx, [norm_col, irreg_col, primam_col, secam_col]] = '999'

    # create new variable based on other columns
    # if birth control => 999 rating
    conditions = [
        ((data_cor[male_col] == '1') | (data_cor[bircont_col] == '1')),
        (data_cor[norm_col] == '1'),
        (data_cor[irreg_col] == '1'),
        (data_cor[primam_col] == '1'),
        (data_cor[secam_col] == '1'),
        (data_cor[[norm_col, irreg_col, primam_col, secam_col]] == '0').all(axis=1)
    ]
    choices = [
        '999',
        '1',
        '2',
        '3',
        '4',
        '5'
    ]
    data_cor[mens_col] = pd.Series(np.select(conditions, choices, default=np.nan), dtype=str)
    
    if show:
        ...
    
    return data_cor

def clean_eot_immediate(idcols, datecol, covidcol, data, show):
    data_cor = data.copy()
    # convert to date
    data_cor.loc[:,datecol] = data_cor.loc[:,datecol].apply(pd.to_datetime)
    # get duplicated rows
    df = data_cor[data_cor[idcols].duplicated(keep=False)]
    # make sure only 1 duplicate (2 total)
    for i,f in df.groupby(idcols):
        if not len(f) == 2:
            display(f)
            print('clean_eot_immediate: more than 2 duplicate IDs for EOT')
    # get immediate eot
    df_immediate = data_cor[data_cor[covidcol] == '1'].copy()
    # get others
    df = data_cor.loc[~data_cor.index.isin(df_immediate.index)].copy()
    # display('BEFORE MERGE')
    # display(df)
    # display(df_immediate)
    print('Merging on:', datecol, idcols)
    # merge
    data_cor = pd.merge(
        df,
        df_immediate,
        how='outer',
        on=idcols,
        suffixes=("", "_immediate")
    )
    # display('AFTER MERGE')
    # display(data_cor)
    assert len(df) + len(df_immediate) >= len(data_cor)
    assert not data_cor[idcols[0]].duplicated().all()

    # rename cols
    cols = data_cor.columns[data_cor.columns.str.endswith('_eot_immediate')]
    mapper = {col+'_eot_immediate': col+'_immediate_eot' for col in cols.str.extract('(.+)_eot_immediate$')[0]}
    data_cor = data_cor.rename(mapper, axis=1)
    # rename date
    mapper = {'Date': 'Date_eot', 'Date_immediate': 'Date_immediate_eot'}
    data_cor = data_cor.rename(columns=mapper)
    return data_cor
    
def clean_duplicate_unknown_id(data, show, idx, idcol, varname):
    assert idcol in data.columns
    data_cor = data.copy()
    # create variable for no duplicate / unknown
    data_cor[varname] = 0
    # remember IDs 
    ids = data_cor.loc[idx, idcol]

    if 'parent' in varname:
        parent = True
        parent_infos = ids.str.extract('(?P<ID>(?:UC|SU)-\d\d\d\d)_*(?P<parent>\d\d)*')
    else:
        parent = False


    # drop duplicates
    data_cor = data_cor.drop(index=idx)
    # flag problem
    for id in ids:
        # if id remains
        if (data_cor[idcol].str.startswith(id)).any():
            data_cor.loc[data_cor[idcol].str.startswith(id), varname] = 1
        else:
            # create row
            row = pd.Series(
                [np.nan]*len(data_cor.columns),
                index=data_cor.columns
            )
            # if no parent info
            # display(id, parent_infos['ID'], id in parent_infos['ID'].values)
            if parent and id in parent_infos['ID'].values:
                # create dummy parent
                row[idcol] = id + '_01'
            else:
                row[idcol] = id
            row[varname] = 1
            # add row
            data_cor.loc[data_cor.index[-1]+1] = row

    return data_cor

def rename_col(data, show, replace_from, replace_to):
    data_cor = data.copy()
    d = {col: replace_to if col == replace_from else col for col in data_cor.columns}
    data_cor = data_cor.rename(columns=d)
    return data_cor
