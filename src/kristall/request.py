from werkzeug.wrappers import Request as WRequest
from werkzeug.wrappers.json import JSONMixin


class Request(JSONMixin, WRequest):
    pass
