import inspect


def endpoint(item):
    if inspect.isclass(item):
        mname = item.__module__
        cqname = item.__qualname__
    else:
        mname = item.__class__.__module__
        cqname = item.__class__.__qualname__
    return f'{mname}.{cqname}'
