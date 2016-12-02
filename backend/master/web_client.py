"""An implementation for interacting with the Spotnet web client."""

from ..utils import WebSocketWrapper


class SpotnetWebClient(WebSocketWrapper):

    def __init__(self, ws):
        super(SpotnetWebClient, self).__init__(ws)
