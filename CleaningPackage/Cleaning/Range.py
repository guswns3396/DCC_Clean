from ..global_vars import pd

class Range:
    def __init__(self, rtype, **kwargs):
        if rtype == 'discrete':
            assert 'set_' in kwargs
            self.set = kwargs['set_']
            if 'spc_' in kwargs:
                self.spc = kwargs['spc_']
            else:
                self.spc = set()
        elif rtype == 'continuous':
            for key in ['start_', 'end_', 'spc_']:
                assert key in kwargs
            self.start = kwargs['start_']
            self.end = kwargs['end_']
            self.spc = kwargs['spc_']
        elif rtype == 'date':
            for key in ['start_', 'end_', 'spc_']:
                assert key in kwargs
            self.start = pd.to_datetime(kwargs['start_'])
            self.end = pd.to_datetime(kwargs['end_'])
            self.spc = kwargs['spc_']
        elif rtype == 'any':
            pass
        else:
            raise ValueError

        # special

        self.rtype = rtype
    