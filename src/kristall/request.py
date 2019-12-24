from typing import Union

from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.wrappers import Request as WRequest


class Request(WRequest):

    MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # four megabytes

    def get_data(
                self, cache: bool = True, as_text: bool = True,
                parse_form_data: bool = False,
            ) -> Union[str, bytes]:
        if self.content_length > self.MAX_CONTENT_LENGTH:
            raise RequestEntityTooLarge(
                f'Request size exceeds allowed {self.MAX_CONTENT_LENGTH} bytes'
            )
        return super().get_data(cache, as_text, parse_form_data)
