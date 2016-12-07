"""The Spotnet slave server implementation."""

import asyncio

from subprocess import PIPE, Popen
from websockets.exceptions import ConnectionClosed

from ..utils import get_configured_logger, WebSocketWrapper
from .config import SPOTNET_SLAVE_LOGGER_NAME


class SpotnetSlaveServer(object):

    """A server for Spotify audio playback.

    Attributes:
        master_address (str): The address pointing to the master server.
        mopidy_port (int): The port to run the mopidy server on.
        is_connected (bool): Boolean indicating whether this slave has
            successfully set up its Spotify credentials and is ready for
            playback.
        logger (logging.Logger): A logger instance for this server.

    Raises:
        ValueError: If discovery mode is disabled and no master address is
            specified.

    """

    def __init__(self, do_discover, master_address=None, mopidy_port=8888):
        self._master_server_ws = WebSocketWrapper()
        self._mopidy_server_ws = WebSocketWrapper()

        self.mopidy_port = mopidy_port

        self.is_connected = False
        self.logger = get_configured_logger(SPOTNET_SLAVE_LOGGER_NAME)

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

        if self._run_mopidy_proc(username, password):
            # TODO: spawn mopidy process, make sure it starts ok, init ws
            addr = 'localhost:{}/mopidy/ws'.format(self.mopidy_port)
            yield from self._mopidy_server_ws.open_ws(addr)
        else:
            # TODO: send ws login failure back to master
            pass

    def _run_mopidy_proc(self, username, password):
        """Spawn a mopidy server process.

        Notes:
            This method will set the private ``_mopidy_proc`` and
            ``_mopidy_ws`` attributes of this class.

        Returns:
            bool: True if Spotify authentication passed, otherwise false.

        """
        self.logger.info('Attempting to initialize mopidy server with '
                         'provided Spotify credentials.')

        args = 'mopidy -o spotify/username={0} -o spotify/password={1}'.format(
                    username, password)
        self._mopidy_proc = Popen(args, universal_newlines=True, stdout=PIPE,
                                  stderr=PIPE)

        # TODO: check out stdout to make sure nothing bad happened
        print(self._run_mopidy_proc.stdout)

        # TODO: more logging
        # TODO: update _has_connected

        # we should be good to go now, then. maybe confirm connection?
        # TODO: send completion message to master

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
