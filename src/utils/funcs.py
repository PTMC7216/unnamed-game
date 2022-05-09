from math import floor


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


def truncate(f, v):
    return floor(f * 10 ** v) / 10 ** v
