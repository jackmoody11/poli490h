from functools import wraps


def community(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.st == 'Community':
            return f
        else:
            pass
    return wrapper


def intermediate(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.st == 'Intermediate':
            return f
        else:
            pass
    return wrapper


def active(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.st == 'Active':
            return f
        else:
            pass
    return wrapper
