"""A client implementation for the Spotnet slave server."""

import uuid

from ..utils import WebSocketWrapper


class SpotnetSlaveClient(WebSocketWrapper):

    """A client for interacting with a Spotnet slave server.

    Attributes:
        name (str): The user friendly name of the slave node.
        uuid (str): The unique identifier for the slave node.
        is_connected (bool): Boolean indicating whether or not this instance
            has been connected with Spotfiy credentials.
        track_queue (List[Tuple(str,str)]): A list of tuples containing the
            Spotify id and uri of each track in the queue for this slave
            node.
        votes_for_skip (int): The current number of votes towards skipping
            the currently playing song.

    """

    def __init__(self, ws):
        super(SpotnetSlaveClient, self).__init__(ws)

        self.name = None
        self.uuid = str(uuid.uuid1())
        self.is_connected = False
        self.track_queue = []
        self.votes_for_skip = 0
