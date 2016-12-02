"""A client implementation for the Spotnet slave server."""

import datetime
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
        counted_votes_for_skip (int): The current number of votes towards
            skipping the currently playing song.
        first_connected_at (str): An isoformat string indicating the time
            tht the slave first made connection with the master server.

    """

    def __init__(self, ws):
        super(SpotnetSlaveClient, self).__init__(ws)

        self.name = None
        self.uuid = str(uuid.uuid1())
        self.is_connected = False
        self.track_queue = []
        self.counted_votes_for_skip = 0
        self.first_connected_at = datetime.datetime.now().isoformat()

    def get_state(self):
        """Return the state of this slave as a JSON-like dict.

        Returned dicts will have the form::

            {
                'uuid': str,
                'name': str,
                'is-connected': bool,
                'counted-votes-for-skip': int,
                'first-connected-at': string,
                'track-queue': [
                    {
                        'id': str,
                        'uri': str
                    },

                    ...
                ]
            }

        """
        json_like_track_queue = [
            {'id': track_id, 'uri': track_uri} for track_id, track_uri in
            self.track_queue]

        return {
            'uuid': self.uuid,
            'name': self.name,
            'is-connected': self.is_connected,
            'counted-votes-for-skip': self.counted_votes_for_skip,
            'first-connected-at': self.first_connected_at,
            'track-queue': json_like_track_queue
        }
