"""A class for wrapping a WebSocket."""

import json
import websockets


class WebSocketWrapper(object):

    """A class that wraps a client WebSocket.

    Attributes:
        ws (websockets.client.WebSocketClientProtocol): The websocket object
            representing the WebSocket wrapped by this class. This attribute
            will be set to None when a WebSocket connection is not open.

    """

    def __init__(self, ws=None):
        self.ws = ws

    async def open_ws(self, address):
        """Coroutine to open a WebSocket to the specified address.

        This method sets the ``ws`` attribute of this class to an open
        WebSocketClientProtocol object. If this class already has a

        Args:
            address (str): The address to connect to.

        """
        if self.ws is not None:
            return
        else:
            self.ws = await websockets.connect('ws://' + address)

    async def close_ws(self):
        """Coroutine to close the current WebSocket connection."""
        if self.ws is None:
            return
        else:
            await self.ws.close()
            self.ws = None

    async def send_json(self, json_dict):
        """Send JSON over this class's WebSocket.

        Args:
            json_dict (dict): A JSON-like dict.

        """
        json_payload = json.dumps(json_dict)
        await self.ws.send(json_payload)

    async def recv_json(self):
        """Receive JSON over this class's WebScoket.

        Returns:
            dict: A JSON-like dict.

        """
        resp = await self.ws.recv()
        json_resp = json.loads(resp)
        return json_resp
