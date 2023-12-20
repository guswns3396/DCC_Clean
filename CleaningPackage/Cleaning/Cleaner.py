from ..global_vars import pd, ID, PID

class Cleaner:
    def __init__(self, clean_type, **kwargs):
        self.type = clean_type
        if self.type == 'replace':
            for arg in ['dict_', 'cols_']:
                assert arg in kwargs
            assert isinstance(kwargs['dict_'], dict)
            assert isinstance(kwargs['cols_'], list)
        elif self.type == 'overwrite':
            for arg in ['idx_', 'val_', 'col_']:
                assert arg in kwargs
            assert isinstance(kwargs['idx_'], list)
            assert isinstance(kwargs['val_'], list)
            assert isinstance(kwargs['col_'], str)
        elif self.type == 'function':
            for arg in ['func_', 'kwargs_']:
                assert arg in kwargs
            assert isinstance(kwargs['kwargs_'], dict)
        elif self.type == 'shift':
            for arg in ['shift_', 'cols_']:
                assert arg in kwargs
            assert isinstance(kwargs['shift_'], dict)
            assert isinstance(kwargs['cols_'], list)
        elif self.type == 'drop':
            for arg in ['idx_']:
                assert arg in kwargs
            assert isinstance(kwargs['idx_'], list)
        else:
            raise ValueError
        self.kwargs = kwargs
        
    def __repr__(self):
        return self.type + ', ' + str(self.kwargs)
    
    def clean(self, data, show):
        data_raw = data.copy()
        if self.type == 'replace':
            for col in self.kwargs['cols_']:
                data.loc[:, col] = data.loc[:, col].replace(self.kwargs['dict_'], value=None)
                if show:
                    if data_raw[col].isin(self.kwargs['dict_'].keys()).sum() > 0:
                        print('Showing Replacement')
                        idx = data_raw[data_raw[col].isin(self.kwargs['dict_'].keys())].index
                        display(pd.concat(
                            [
                                *(
                                    [data.loc[idx, ID] if not col.startswith(PID) else data.loc[idx, col]] + \
                                    [
                                        data_raw.loc[idx, col],
                                        data.loc[idx, col]
                                    ]
                                )
                            ],
                            axis=1
                        ))
        elif self.type == 'overwrite':
            col = self.kwargs['col_']
            data.loc[self.kwargs['idx_'], col] = self.kwargs['val_']
            if show:
                print('Showing Overwrite')
                display(pd.concat(
                    [
                        *(
                            [data.loc[self.kwargs['idx_'], ID] if not col.startswith(PID) else data.loc[self.kwargs['idx_'], col]] + \
                            [
                                data_raw.loc[self.kwargs['idx_'], col],
                                data.loc[self.kwargs['idx_'], col]
                            ]
                        )
                    ],
                    axis=1
                ))
        elif self.type == 'function':
            data = self.kwargs['func_'](data=data, show=show, **self.kwargs['kwargs_'])
        elif self.type == 'shift':
            data.loc[:, self.kwargs['cols_']] = data[self.kwargs['cols_']].replace(self.kwargs['shift_'])
            if show:
                print('Showing Shift')
                display(data_raw.loc[:,self.kwargs['cols_']], data.loc[:,self.kwargs['cols_']])
        elif self.type == 'drop':
            if show:
                print('Showing Drop')
                display(data.loc[self.kwargs['idx_'], :])
            data = data.drop(index=self.kwargs['idx_'])
        else:
            raise ValueError
        
        return data