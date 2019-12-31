import json
from typing import Any, Optional, Union

from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.wrappers import Request as WRequest


class Request(WRequest):

    MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # four megabytes

    def __init__(
                self, environ, populate_request: bool = True, shallow: bool = False,
                json_decoder: Optional[Any] = None,
            ):
        super().__init__(environ, populate_request, shallow)
        self.decoder = json_decoder
        if self.decoder is None:
            self.decoder = json.JSONDecoder

    def get_data(
                self, cache: bool = True, as_text: bool = True,
                parse_form_data: bool = False,
            ) -> Union[str, bytes]:
        if self.content_length > self.MAX_CONTENT_LENGTH:
            raise RequestEntityTooLarge(
                f'Request size exceeds allowed {self.MAX_CONTENT_LENGTH} bytes'
            )
        return super().get_data(cache, as_text, parse_form_data)

    def get_json(self, decoder: Optional[Any] = None) -> dict:
        if decoder is None:
            decoder = self.decoder
        data = self.get_data()
        return json.loads(data, cls=decoder)
