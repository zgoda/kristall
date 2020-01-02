from werkzeug.wrappers import Response as WResponse


class Response(WResponse):
    """Thin wrapper over :class:`~werkzeug.wrappers.Response`. The only
    difference is predefined response content type which is set to
    ``application/json``.
    """

    default_mimetype = 'application/json'
