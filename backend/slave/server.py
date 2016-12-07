"""The Spotnet slave server implementation."""

import asyncio
import spotify

from spotify import SessionEvent as SpotifyEvent
from websockets.exceptions import ConnectionClosed

from ..utils import get_configured_logger, WebSocketWrapper
from .config import SPOTNET_SLAVE_LOGGER_NAME


class SpotnetSlaveServer(object):

    """A server for Spotify audio playback.

    Attributes:
        master_address (str): The address pointing to the master server.
        is_connected (bool): Boolean indicating whether this slave has
            successfully set up its Spotify credentials and is ready for
            playback.
        logger (logging.Logger): A logger instance for this server.

    Raises:
        ValueError: If discovery mode is disabled and no master address is
            specified.

    """

    def __init__(self, do_discover, master_address=None):
        self.is_connected = False
        self.logger = get_configured_logger(SPOTNET_SLAVE_LOGGER_NAME)

        self._spotify_session = None
        self._init_spotify_session()
        self._spotify_login_failed = asyncio.Event()
        self._spotify_login_passed = asyncio.Event()
        self._spotify_track_ended = asyncio.Event()
        self._master_server_ws = WebSocketWrapper()

        if do_discover:
            self.master_address = self._discover_master_server()
        elif master_address is None:
            raise ValueError('Must specify master server address if '
                             'discovery mode is disabled.')
        else:
            self.master_address = master_address

    @asyncio.coroutine
    def run_forever(self):
        """Run the slave server."""
        self.logger.info('Beginning execution of Spotnet slave server.')
        was_forcibly_closed = False

        try:
            yield from self._master_server_ws.open_ws(self.master_address)

            while not self.is_connected:
                yield from self._await_connected()

            # TODO: send status message to master about being actually connected

            while True:
                yield from self._run()
        except ConnectionClosed as e:
            self.logger.warn('Master server unexpectedly closed WebSocket '
                             'connection.')
            was_forcibly_closed = True
        except ValueError as e:
            self.logger.error('Invalid message received: ' + repr(e))
        except Exception as e:
            self.logger.error('Received unexpected error: ' + repr(e))
        finally:
            if not was_forcibly_closed:
                self.logger.info('Closing WebSocket connection.')
                # TODO: may have to close other ws
                yield from self._master_server_ws.close_ws()

            self.logger.info('Done running.')

    @asyncio.coroutine
    def _await_connected(self):
        """Coroutine to perform the slave connection flow."""
        yield from self._master_server_ws.send_json({
            'status': 'request-connect',
            'sender': 'slave'})

        # wait for credentials to be sent from the master server
        self.logger.info('Established connection to master sever; awaiting '
                         'credentials.')
        resp = yield from self._master_server_ws.recv_json()

        status = resp.get('status')
        if status != 'send-credentials':
            raise ValueError(
                'Invalid "status" received in slave connection flow.')

        self.logger.info('Received "send-credentials" directive from master.')

        data = resp['data']
        username = data['username']
        password = data['password']

        self.logger.info('Received Spotify username "{}" from master; not '
                         'displaying password here.'.format(username))

        self._spotify_session.login(username, password)

        # wait for login pass/fail
        login_passed_task = asyncio.async(self._spotify_login_passed.wait())
        login_failed_task = asyncio.async(self._spotify_login_failed.wait())
        done, pending = yield from asyncio.wait(
            [login_passed_task, login_failed_task],
            return_when=asyncio.FIRST_COMPLETED)

        if login_passed_task in done:
            # login passed
            login_failed_task.cancel()
            self.is_connected = True
        else:
            # login failed
            login_passed_task.cancel()
            self.logger.info('Login failed.')

        self._spotify_login_failed.clear()
        self._spotify_login_passed.clear()

    @asyncio.coroutine
    def _run(self):
        """Coroutine to run the slave server's main functionality."""
        pass

    def _discover_master_server(self):
        """Run service discovery to get the master server address.

        Returns:
            str: The master server address.

        """
        # TODO
        return None

    def _init_spotify_session(self):
        """Configure the Libspotify session."""
        self._spotify_session = spotify.Session()

        loop = spotify.EventLoop()
        loop.start()

        spotify.AlsaSink(self._spotify_session)
        self._spotify_session.on(
            SpotifyEvent.LOGGED_IN, self._on_login)
        self._spotify_session.on(
            SpotifyEvent.END_OF_TRACK, self._on_end_of_track)

    @asyncio.coroutine
    def _wait_for_login_passed(self):
        pass

    def _on_login(self, session, error_type):
        """Libspotify login event handler."""
        if error_type is spotify.ErrorType.Ok:
            self._spotify_login_passed.set()
        else:
            self._spotify_login_failed.set()

    def _on_end_of_track(self, session):
        """Libspotify end of track event handler."""
        self._on_end_of_track.set()
