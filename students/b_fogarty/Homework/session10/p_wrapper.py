
@wrapper
def p_wrapper(return_string,sym='p'):
    '<{}> ' + string + ' </{}>'.format(sym,sym)
    def return_string(string):
        return string


c = wrap(return_string)

def p_wrapper(func):
    def return_string(*args, **kwargs):
        results = func(*args, **kwargs)
        print(result)
        return '<p> {} </p>'.format(result)
    return return_string

    print(return_string('tstiks'))

import time
class Timer:
    def __init__(self, file_like):
        self.file_like = file_like
    def __enter__(self):
        self.start = time.clock()
    def __exit__(self,*args, **kwargs):
        #exit returns true or false
        elapse = time.clock - self.start
        msg = '{} seconds'.format(elapse)
        self.file_like.write(msg)
        return False