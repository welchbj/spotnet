"""An implementation for interacting with the Spotnet web client."""

from ..utils import WebSocketWrapper


class SpotnetWebClient(WebSocketWrapper):

    def __init__(self, ws):
        super(SpotnetWebClient, self).__init__(ws)

    async def send_state(self, state_json):
        """Send the system state over the WebSocket connection.

        Args:
            state_json (dict): A JSON-like dict representing the state of the
                system.

        """
        state_json['status'] = 'send-state'
        state_json['sender'] = 'master'
        await self.send_json(state_json)
