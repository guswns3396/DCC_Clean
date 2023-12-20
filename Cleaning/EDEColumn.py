class EDEColumnGroup:
    def __init__(self, column_group, set_range, subscale, colobj_list):
        self.name = column_group
        self.range = set_range
        self.columns = colobj_list
        self.subscale = subscale
        
    def __repr__(self):
        return "EDEColumnGroup('" + self.name + "')"
    
class EDEColumn:
    def __init__(self, column_name, column_group, set_range, subscale=None):
        self.name = column_name
        self.group = column_group
        self.range = set_range
        self.subscale = subscale
        
    def __repr__(self):
        return "EDEColumn('" + self.name + ", " + repr(self.group) + ", " + str(self.subscale) + "')"

def setup_ede(subscales, colgrps):
    # verify all the cols are lists
    assert all([isinstance(value[0], list) for value in colgrps.values()])
    assert all([isinstance(subscales[subscale][element][0], list) \
        for subscale in subscales for element in subscales[subscale]])

    # make column objects
    EDE_COLS = {} # map column name to column obj
    EDE_COLGRPS = {} # map column group name to column group objc
    EDE_SUBSCALES = {} # map ede subscale name to list of column objc

    # for each subscale
    for subscale in subscales:
        # for each element in subscale
        for element in subscales[subscale]:
            column_group = element
            set_range = subscales[subscale][element][1]
            column_names = subscales[subscale][element][0]
            colobj_list = []
            # create empty list for columns that are used calculate subscale score
            EDE_SUBSCALES[subscale] = []
            # for each column in column group
            for column_name in column_names:
                # make column object
                colobj = EDEColumn(column_name, column_group, set_range, subscale)
                # add to EDE_COLS
                EDE_COLS[column_name] = colobj
                # append to colobj_list
                colobj_list.append(colobj)
                # add to EDE_SUBSCALES if used to calculate score
                if subscale == 'restraint':
                    if '_TOT' in column_name:
                        EDE_SUBSCALES[subscale].append(colobj)
                else:
                    EDE_SUBSCALES[subscale].append(colobj)
            # make column group object
            colgrpobj = EDEColumnGroup(column_group, set_range, subscale, colobj_list)
            # add to EDE_COLGRPS
            EDE_COLGRPS[column_group] = colgrpobj

    # for each column group
    for colgrp in colgrps:
        column_names = colgrps[colgrp][0]
        column_group = colgrp
        set_range = colgrps[colgrp][1]
        subscale = None
        colobj_list = []
        # for each column in column group
        for column_name in column_names:
            # make column object
            colobj = EDEColumn(column_name, column_group, set_range, subscale)
            # add to EDE_COLS
            EDE_COLS[column_name] = colobj
            # append to colobj_list
            colobj_list.append(colobj)
        # make column group object
        colgrpobj = EDEColumnGroup(column_group, set_range, subscale, colobj_list)
        # add to EDE_COLGRPS
        EDE_COLGRPS[column_group] = colgrpobj
        
    return EDE_COLS, EDE_COLGRPS, EDE_SUBSCALES
