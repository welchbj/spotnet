"""The Spotnet slave server implementation."""

from websockets.exceptions import ConnectionClosed

from ..utils import get_configured_logger, WebSocketWrapper
from .config import SPOTNET_SLAVE_LOGGER_NAME


class SpotnetSlaveServer(WebSocketWrapper):

    """A server for Spotify audio playback.

    Attributes:
        master_address (str): The address pointing to the master server.
        logger (logging.Logger): A logger instance for this server.
        username (str): Username to use when authenticating with Spotify.
        password (str): Password to use when authenticating with Spotify.

    Raises:
        ValueError: If discovery mode is disabled and no master address is
            specified.

    """

    def __init__(self, do_discover, master_address=None):
        super(SpotnetSlaveServer, self).__init__()

        self.logger = get_configured_logger(SPOTNET_SLAVE_LOGGER_NAME)

        if do_discover:
            self.master_address = self._discover_master_server()
        elif master_address is None:
            raise ValueError('Must specify master server address if '
                             'discovery mode is disabled.')
        else:
            self.master_address = master_address

    async def run_forever(self):
        """Run the slave server."""
        self.logger.info('Beginning execution of Spotnet slave server.')

        try:
            await self.open_ws(self.master_address)
            await self._await_connected()

            while True:
                await self._handle_master_message()
        except ConnectionClosed as e:
            self.logger.error('Unexpected closed WebSocket connection.')
        except ValueError as e:
            self.logger.error('Invalid message received: ' + repr(e))
        except Exception as e:
            self.logger.error('Received unexpected error: ' + repr(e))
        finally:
            self.logger.info('Closing WebSocket connection.')
            await self.close_ws()

    async def _await_connected(self):
        """Coroutine to perform the slave connection flow."""
        await self.send_json({
            'status': 'request-connect',
            'sender': 'slave'})

        # wait for credentials to be sent from the master server
        resp = await self.recv_json()

        status = resp.get('status')
        if status != 'send-credentials':
            raise ValueError(
                'Invalid "status" received in slave connection flow.')

        self.logger.info('Received "send-credentials" directive from master.')

        data = resp['data']
        self.username = data['username']
        self.password = data['password']

        self.logger.info('Received Spotify username "{}" from master; not '
                         'displaying password here.'.format(self.username))

    async def _handle_master_message(self):
        pass

    def _discover_master_server(self):
        """Run service discovery to get the master server address.

        Returns:
            str: The master server address.

        """
        # TODO
        return None
