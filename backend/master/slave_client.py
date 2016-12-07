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
        is_paused (bool): Boolean indicating whether or not this slave
            instance is paused; instances are initialized with audio paused.
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
        self.is_paused = True
        self.track_queue = []
        self.counted_votes_for_skip = 0
        self.first_connected_at = datetime.datetime.now().isoformat()

    @asyncio.coroutine
    def send_credentials(self, name, username, password):
        """Coroutine to send credentials and node name to connect the slave.

        Args:
            name (str): The name to assign the slave node.
            username (str): The Spotify username to use in authentication.
            password (str): The Spotify password to use in authentication.abs

        """
        yield from self.send_json({
            'status': 'send-credentials',
            'sender': 'master',
            'data': {
                'username': username,
                'password': password
            }})

        self.name = name
        self.is_connected = True

    @asyncio.coroutine
    def send_pause(self):
        """Coroutine to tell the slave server to pause audio playback."""
        # TODO
        pass

    @asyncio.coroutine
    def send_play(self):
        """Coroutine to tell the slave server to resume audio playback."""
        # TODO
        pass

    @asyncio.coroutine
    def send_track(self):
        """Coroutine to send the slave server the next track to play."""
        # TODO
        pass

    def prepend_track(self, track):
        """Add a track to the beginnig of the queue."""
        self.track_queue = [track] + self.track_queue

    def replace_first_track(self, track):
        if not self.track_queue:
            self.track_queue.append(track)
        else:
            self.track_queue[0] = track

    def set_next_track(self, track):
        if not self.track_queue:
            self.track_queue.append(track)
        else:
            self.track_queue = (self.track_queue[:1] +
                                [track] +
                                self.track_queue[1:])

    def remove_track(self, position):
        """Remove a track from the specified position.

        Notes:
            Assumes that position is a valid index within this class's
            ``track_queue`` attribute.

        """
        self.track_queue.pop(position)

    def get_state(self):
        """Return the state of this slave as a JSON-like dict.

        Returned dicts will have the form::

            {
                'uuid': str,
                'name': str,
                'is-connected': bool,
                'is-paused': bool,
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
        return {
            'uuid': self.uuid,
            'name': self.name,
            'is-connected': self.is_connected,
            'is-paused': self.is_paused,
            'counted-votes-for-skip': self.counted_votes_for_skip,
            'first-connected-at': self.first_connected_at,
            'track-queue': self.track_queue
        }
