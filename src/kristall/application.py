from werkzeug.routing import Map


class Application:

    def __init__(self):
        self.url_map = Map()

    def __call__(self, application, start_response):
        pass
