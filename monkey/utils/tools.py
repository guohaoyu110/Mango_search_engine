from functions import wraps 

def singleton(cls):
    '''
    a singleton created by using decorator
    :param cls: cls
    :return: instance
    '''
    _instances = {}
    
    @wraps(cls)
    def instance(*args, **kw):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kw)
        return _instances[cls]
    return instance