def p_wrapper(func):    
    def paragraph(*args, **kwargs):
        result = "<p> {} </p>".format(func(*args))
        return result
    return paragraph


def tag_wrapper(tag):   
    def tagged(*args):
        result = "<{}> {} </{}>".format(tag, func(*args), tag)
        return result
    return tagged
