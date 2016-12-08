"""The Spotnet slave server implementation."""

import asyncio
import json

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
            self.logger.info('Established WebSocket with master server.')

            # send message to master to join the network
            yield from self._master_ws.send_json({
                'status': 'request-connect',
                'sender': 'slave'})

            # wait for credentials
            while not self.is_connected:
                yield from self._await_connected()

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
            yield from asyncio.wait(
                [self._master_ws.close_ws(),
                 self._mopidy_ws.close_ws(),
                 self._terminate_mopidy_proc()],
                return_when=asyncio.ALL_COMPLETED)
            self.logger.info('Done running.')

    @asyncio.coroutine
    def _await_connected(self):
        """Coroutine to perform the slave connection flow."""
        # wait for credentials to be sent from the master server
        self.logger.info('Awaiting credentials from master server.')
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

        args = ['mopidy', '-o', 'http/port={}'.format(self.mopidy_port),
                          '-o', 'spotify/username={}'.format(username),
                          '-o', 'spotify/password={}'.format(password)]

        self._mopidy_proc = yield from asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT)

        self.logger.info('Spawned mopidiy subprocess; awaiting login status.')

        did_login = False
        while True:
            line = yield from self._mopidy_proc.stdout.readline()
            print(line)
            if b'Spotify login error' in line:
                break
            elif b'Logged in to Spotify in online mode' in line:
                did_login = True
                break

        if did_login:
            self.logger.info('Login passed; notifiying master.')

            yield from self._master_ws.send_json({
                'status': 'login-passed',
                'sender': 'slave'})

            addr = 'localhost:{}/mopidy/ws'.format(self.mopidy_port)
            self.logger.info('Attempting to open WebSocket with mopidy at '
                             'address ws://{}'.format(addr))

            yield from asyncio.sleep(3)
            yield from self._mopidy_ws.open_ws(addr)

            self.logger.info('mopidy WebSocket successfully opened.')
            self.is_connected = True
        else:
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
            yield from self._mopidy_proc.wait()
            self._mopidy_proc = None

    @asyncio.coroutine
    def _run(self):
        """Coroutine to run the slave server's main functionality."""
        mopidy_recv = asyncio.async(self._mopidy_ws.recv_json())
        master_recv = asyncio.async(self._master_ws.recv_json())
        done, pending = yield from asyncio.wait(
                            [mopidy_recv, master_recv],
                            return_when=asyncio.FIRST_COMPLETED)

        if mopidy_recv in done:
            # received something from the mopidy process
            master_recv.cancel()
            resp = mopidy_recv.result()
            self.logger.info('Received message from mopidy:')
            print(json.dumps(resp, indent=2))
        else:
            # received something from the master server
            mopidy_recv.cancel()
            resp = master_recv.result()

            status = resp['status']
            if status == 'play-audio':
                yield from self._send_play_playback()
            elif status == 'pause-audio':
                yield from self._mopidy_ws.send_json({
                    'jsonrpc': '2.0',
                    'id': 1,
                    'method': 'core.playback.pause'})
            elif status == 'add-track':
                data = resp['data']
                uri = data['uri']
                position = data['position']

                self.logger.info('Received request to add track with '
                                 'uri {0} and position {1}.'
                                 .format(uri, position))
                yield from self._mopidy_ws.send_json({
                    'jsonrpc': '2.0',
                    'id': 1,
                    'method': 'core.tracklist.add',
                    'params': {
                        'uris': [uri],
                        'at_position': position
                    }})
            elif status == 'remove-track':
                data = resp['data']
                uri = data['uri']
                position = data['position']

                self.logger.info('Received request to remove track with '
                                 'uri {0} and position {1}.'
                                 .format(uri, position))
                yield from self._mopidy_ws.send_json({
                    'jsonrpc': '2.0',
                    'id': 1,
                    'method': 'core.tracklist.remove',
                    'params': {
                        'criteria': {
                            'uri': [uri]
                        }
                    }})

                if position == 0:
                    yield from self._send_stop_playback()
                    yield from self._send_next_track()
                    yield from self._send_play_playback()

            yield from self._mopidy_ws.send_json({
                'jsonrpc': '2.0',
                'id': 1,
                'method': 'core.tracklist.get_tracks'})

    @asyncio.coroutine
    def _send_next_track(self):
        """Coroutine to tell mopidy to go to the next track."""
            yield from self._mopidy_ws.send_json({
                'jsonrpc': '2.0',
                'id': 1,
                'method': 'core.playback.next'})

    @asyncio.coroutine
    def _send_stop_playback(self):
        """Coroutine to tell mopidy to stop playback."""
            yield from self._mopidy_ws.send_json({
                'jsonrpc': '2.0',
                'id': 1,
                'method': 'core.playback.stop'})

    @asyncio.coroutine
    def _send_play_playback(self):
        """Coroutine to tell mopidy to play playback."""
            yield from self._mopidy_ws.send_json({
                'jsonrpc': '2.0',
                'id': 1,
                'method': 'core.playback.play',
                'params': {
                    'tl_track': None,
                    'tlid': None
                }})

    def _discover_master_server(self):
        """Run service discovery to get the master server address.

        Returns:
            str: The master server address.

        """
        # TODO
        return None
