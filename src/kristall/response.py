from werkzeug.wrappers import Response as WResponse
from werkzeug.wrappers.json import JSONMixin


class Response(JSONMixin, WResponse):
    pass
