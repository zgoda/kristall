class ResourceMixin:

    @property
    def endpoint(self):
        mname = self.__class__.__module__
        cqname = self.__class__.__qualname__
        return f'{mname}.{cqname}'
