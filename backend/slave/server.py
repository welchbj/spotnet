"""The Spotnet slave server implementation."""

import asyncio
import locale

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
        mopidy_port (int): The port on which to run the mopidy process.
        logger (logging.Logger): A logger instance for this server.

    Raises:
        ValueError: If discovery mode is disabled and no master address is
            specified.

    """

    def __init__(self, do_discover, master_address=None, mopidy_port=8888):
        self.is_connected = False
        self.mopidy_port = mopidy_port
        self.logger = get_configured_logger(SPOTNET_SLAVE_LOGGER_NAME)

        self._master_ws = WebSocketWrapper()
        self._mopidy_ws = WebSocketWrapper()
        self._mopidy_proc = None

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

        try:
            yield from self._master_ws.open_ws(self.master_address)

            # send message to master to join the network
            yield from self._master_ws.send_json({
                'status': 'request-connect',
                'sender': 'slave'})

            # wait for credentials
            while not self.is_connected:
                yield from self._await_connected()

            # TODO: handle main requests
            while True:
                yield from self._run()
        except ConnectionClosed as e:
            self.logger.warn('Master server unexpectedly closed WebSocket '
                             'connection.')
        except ValueError as e:
            self.logger.error('Invalid message received: ' + repr(e))
        except Exception as e:
            self.logger.error('Received unexpected error: ' + repr(e))
        finally:
            self.logger.info('Closing open WebSocket connections and '
                             'terminating spawned mopidy process.')
            asyncio.wait(
                [self._master_ws.close_ws(),
                 self._mopidy_ws.close_ws(),
                 self._terminate_mopidy_proc()],
                return_when=asyncio.ALL_COMPLETED)
            self.logger.info('Done running.')

    @asyncio.coroutine
    def _await_connected(self):
        """Coroutine to perform the slave connection flow."""
        # wait for credentials to be sent from the master server
        self.logger.info('Established initial connection with master sever; '
                         'awaiting credentials.')
        resp = yield from self._master_ws.recv_json()

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

        login_passed = asyncio.Event()
        login_failed = asyncio.Event()

        args = ['mopidy', '-o', 'http/port={}'.format(self.mopidy_port),
                          '-o', 'spotify/username={}'.format(username),
                          '-o', 'spotify/password={}'.format(password)]

        loop = asyncio.get_event_loop()
        self._mopidy_proc, _ = yield from loop.subprocess_exec(
            lambda: MopidySpotifyProtocol(login_passed, login_failed),
            *args)

        self.logger.info('Spawned mopidiy subprocess; awaiting login status.')

        wait_for_login_passed = asyncio.async(login_passed.wait())
        wait_for_login_failed = asyncio.async(login_failed.wait())
        done, pending = yield from asyncio.wait(
            [wait_for_login_passed, wait_for_login_failed],
            return_when=asyncio.FIRST_COMPLETED)

        if wait_for_login_passed in done:
            wait_for_login_failed.cancel()
            self.logger.info('Login passed; notifiying master.')

            yield from self._master_ws.send_json({
                'status': 'login-passed',
                'sender': 'slave'})

            self.logger.info('Opening WebSocket with mopidy.')
            addr = 'ws://localhost:{}/mopidy/ws'.format(self.mopidy_port)
            yield from self._mopidy_ws.open_ws(addr)
            self.logger.info('mopidy WebSocket successfully opened.')
            self.is_connected = True
        else:
            wait_for_login_passed.cancel()
            self.logger.info('Login failed; notifying master.')

            yield from self._master_ws.send_json({
                'status': 'login-failed',
                'sender': 'slave'})

            self.logger.info('Terminating mopidy process.')
            yield from self._terminate_mopidy_proc()
            self.is_connected = False

    @asyncio.coroutine
    def _terminate_mopidy_proc(self):
        """Terminate the spawned mopidy process."""
        if self._mopidy_proc is not None:
            self._mopidy_proc.terminate()
            self._mopidy_proc = None

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


class MopidySpotifyProtocol(asyncio.SubprocessProtocol):

    """A class to process mopidy output streams to determine login status.

    Notes:
        This class is a great example of how poor system design and planning
        makes your life harder in the long run.

    Attributes:
        login_passed_event (asyncio.Event): An event to be set if login
            passes.
        login_failed_Event (asyncio.Event): An event to be set if login
            fails.
        done_checking (bool): Boolean flag that indicates we don't need
            to be checking the stream anymore.

    """

    def __init__(self, login_passed_event, login_failed_event):
        self.login_passed_event = login_passed_event
        self.login_failed_event = login_failed_event
        self.done_checking = False

    def pipe_data_received(self, fd, data):
        """Parse Spotify login info from the process's stream."""
        if self.done_checking:
            return

        text = data.decode(locale.getpreferredencoding(False))

        print(text)

        if 'Spotify login error' in text:
            self.login_failed_event.set()
            self.done_checking = True
        elif 'Logged in to Spotify in online mode' in text:
            self.login_passed_event.set()
            self.done_checking = True

