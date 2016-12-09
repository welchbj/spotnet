"""A client implementation for the Spotnet slave server."""

import asyncio
import datetime
import uuid

from ..utils import WebSocketWrapper


DELAY = 0.1


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
            'sender': 'master'
        })

    @asyncio.coroutine
    def send_play(self):
        """Coroutine to tell the slave server to resume audio playback."""
        yield from self.send_json({
            'status': 'play-audio',
            'sender': 'master'
        })

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
                yield from self._send_add_track(uri)
            elif self.is_paused:
                self.track_queue = [track] + self.track_queue
                yield from self._send_clear_tracks()
                yield from self._send_add_track(uri)
            else:
                self.track_queue[0] = track
                yield from self._send_pause_audio()
                yield from self._send_clear_tracks()
                yield from self._send_add_track(uri)
                yield from self._send_play_audio()
        elif position == 'next':
            if not self.track_queue:
                self.track_queue.append(track)
                yield from self._send_add_track(uri)
            else:
                self.track_queue = (self.track_queue[:1] + [track] +
                                    self.track_queue[1:])

    @asyncio.coroutine
    def remove_track(self, position, from_transition=False):
        """Coroutine to remove a track from the mopidy tracklist.

        Args:
            position (int): The position in the queue to remove.
            from_transition (bool): Indicating if this call is resultant from
                the end of a track into another.
        """
        self.track_queue.pop(position)

        if position == 0:
            if self.is_paused:
                yield from self._send_clear_tracks()
                if self.track_queue:
                    # send the next uri to be played (but we are still paused)
                    new_uri = self.track_queue[0]['uri']
                    yield from self._send_add_track(new_uri)
            else:
                # was playing a track
                if not self.track_queue:
                    yield from self._send_pause_audio()
                    self.is_paused = True
                    yield from self._send_clear_tracks()
                else:
                    if from_transition:
                        yield from self._send_stop_playback()
                    else:
                        yield from self._send_pause_audio()

                    yield from self._send_clear_tracks()
                    new_uri = self.track_queue[0]['uri']
                    yield from self._send_add_track(new_uri)
                    yield from self._send_play_audio()

    @asyncio.coroutine
    def _send_play_audio(self):
        """Coroutine to tell slave to play audio."""
        yield from asyncio.sleep(DELAY)
        yield from self.send_json({
            'status': 'play-audio',
            'sender': 'master'
        })

    @asyncio.coroutine
    def _send_pause_audio(self):
        """Coroutine to tell slave to pause audio."""
        yield from asyncio.sleep(DELAY)
        yield from self.send_json({
            'status': 'pause-audio',
            'sender': 'master'
        })

    @asyncio.coroutine
    def _send_stop_playback(self):
        """Coroutine to tell slave to stop playback."""
        yield from asyncio.sleep(DELAY)
        yield from self.send_json({
            'status': 'stop-playback',
            'sender': 'master'
        })

    @asyncio.coroutine
    def _send_clear_tracks(self):
        """Coroutine to tell slave to clear tracks."""
        yield from asyncio.sleep(DELAY)
        yield from self.send_json({
            'status': 'clear-tracks',
            'sender': 'master'
        })

    @asyncio.coroutine
    def _send_add_track(self, uri):
        """Coroutine to tell slave to add a track by uri."""
        yield from asyncio.sleep(DELAY)
        yield from self.send_json({
            'status': 'add-track',
            'sender': 'master',
            'data': {
                'uri': uri
            }
        })

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
