import inspect
from typing import Type, Union


def endpoint(item: Union[object, Type]) -> str:
    if inspect.isclass(item):
        mname = item.__module__
        cqname = item.__qualname__
    else:
        mname = item.__class__.__module__
        cqname = item.__class__.__qualname__
    return f'{mname}.{cqname}'
