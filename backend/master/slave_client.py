"""A client implementation for the Spotnet slave server."""

import asyncio
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

    @asyncio.coroutine
    def send_pause(self):
        """Coroutine to tell the slave server to pause audio playback."""
        yield from self.send_json({
            'status': 'pause-audio',
            'sender': 'master'})

    @asyncio.coroutine
    def send_play(self):
        """Coroutine to tell the slave server to resume audio playback."""
        yield from self.send_json({
            'status': 'play-audio',
            'sender': 'master'})

    @asyncio.coroutine
    def add_track(self, track, position):
        """Coroutine to add a track to the mopidy tracklist.

        Args:
            track (dict): JSON-like dict with 'id' and 'uri' keys.
            position (str): Either 'current' or 'next'.

        """
        uri = track['uri']
        if position == 'current':
            if not self.track_queue:
                self.track_queue.append(track)
            else:
                self.track_queue = [track] + self.track_queue
            yield from self._send_uri(uri, 0)
        elif position == 'next':
            if not self.track_queue:
                self.track_queue.append(track)
                yield from self._send_uri(uri, 0)
            else:
                self.track_queue = (self.track_queue[:1] + [track] +
                                    self.track_queue[1:])
                yield from self._send_uri(uri, 1)

    @asyncio.coroutine
    def remove_track(self, position):
        """Coroutine to remove a track from the mopidy tracklist.

        Args:
            position (int): The position in the queue to remove.

        """
        track = self.track_queue.pop(position)
        if not self.track_queue:
            self.is_paused = True

        uri = track['uri']
        is_last_track = not self.track_queue
        yield from self._remove_uri(uri, position, is_last_track=is_last_track)

    @asyncio.coroutine
    def _send_uri(self, uri, position):
        """Coroutine to send a URI at a specified position.

        Args:
            uri (str): The Spotify track uri.
            position (int): The position in the slave mopidy queue to insert
                the track.

        """
        yield from self.send_json({
            'status': 'add-track',
            'sender': 'slave',
            'data': {
                'uri': uri,
                'position': position
            }})

    @asyncio.coroutine
    def _remove_uri(self, uri, position, is_last_track=False):
        """Coroutine to send a uri to remove from the slave's mopidy tracklist.

        Args:
            uri (str): The uri to remove.
            position (int): The position of the song to remove.

        """
        yield from self.send_json({
            'status': 'remove-track',
            'sender': 'slave',
            'data': {
                'uri': uri,
                'position': position,
                'is-last-track': is_last_track
            }})

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
