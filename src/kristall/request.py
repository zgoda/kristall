import json
from typing import Optional, Type, Union

from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.wrappers import Request as WRequest


class Request(WRequest):
    """Wrapper over :class:`~werkzeug.wrappers.Request` that has built in
    support for JSON content. Maximum content length is set to 4 megabytes.
    """

    MAX_CONTENT_LENGTH = 4 * 1024 * 1024  # four megabytes

    def __init__(
                self, environ: dict, populate_request: bool = True,
                shallow: bool = False, json_decoder: Optional[Type] = None,
            ):
        """Object initializer that allows setting JSON decoder class to be used
        when decoding JSON content. For complete description of other arguments
        see Werkzeug documentation for :class:`~werkzeug.wrappers.BaseRequest`.
        """
        super().__init__(environ, populate_request, shallow)
        self.decoder = json_decoder
        if self.decoder is None:
            self.decoder = json.JSONDecoder

    def get_data(
                self, cache: bool = True, as_text: bool = True,
                parse_form_data: bool = False,
            ) -> Union[str, bytes]:
        """Overwritten method that retrieves request data. Difference is that
        by default it fetches data as text. For complete description of call
        arguments see Werkzeug documentation for
        :meth:`~werkzeug.wrappers.BaseRequest.get_data`. This method raises
        :exc:`~werkzeug.exceptions.RequestEntityTooLarge` if content length
        exceeds allowed size (default is 4 megabytes).
        """
        if self.content_length > self.MAX_CONTENT_LENGTH:
            raise RequestEntityTooLarge(
                f'Request size exceeds allowed {self.MAX_CONTENT_LENGTH} bytes'
            )
        return super().get_data(cache, as_text, parse_form_data)

    def get_json(self, decoder: Optional[Type] = None) -> dict:
        """A method to retrieve JSON from request data, optionally using
        specified JSON decoder class. If not provided default decoder class
        is used.

        :param decoder: JSON decoder class, defaults to None
        :type decoder: Optional[Type], optional
        :return: request data as parsed JSON
        :rtype: dict
        """
        if decoder is None:
            decoder = self.decoder
        data = self.get_data()
        return json.loads(data, cls=decoder)
