from werkzeug.wrappers import Response as WResponse


class Response(WResponse):

    default_mimetype = 'application/json'
