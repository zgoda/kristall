import inspect
from typing import Type, Union


def endpoint(item: Union[object, Type]) -> str:
    """Endpoint generation function. Returns fully qualified class name in
    dotted notation.

    :param item: item to generate endpoint for, may be either instance or
                 class
    :type item: Union[object, Type]
    :return: fully qualified class name, suitable for use as endpoint name
    :rtype: str
    """
    if inspect.isclass(item):
        mname = item.__module__
        cqname = item.__qualname__
    else:
        mname = item.__class__.__module__
        cqname = item.__class__.__qualname__
    return f'{mname}.{cqname}'
