"""The Spotnet master server implementation."""

import asyncio
import json
import websockets

from websockets.exceptions import ConnectionClosed

from ..utils import get_configured_logger
from .config import SPOTNET_MASTER_LOGGER_NAME
from .slave_client import SpotnetSlaveClient
from .web_client import SpotnetWebClient


class SpotnetMasterServer(object):

    """A server for managing the Spotnet network of slave nodes.

    Attributes:
        port (int): The port on which to run this server.
        connected_slaves (Dict{str:SpotnetSlaveClient}): TODO A dict that maps
            connected slaves' names to their client instance.
        keyphrase (str): The keyphrase required to connect to this server.
        do_advertise (bool): Boolean flag indicating whether or not to
            advertise this service via Zeroconf.
        voting_enabled (bool): Boolean flag indicating whether to allow for
            the voting of tracks.
        votes_for_skip (int): The number of votes required to
            skip a song.
        slave_dict_by_uuid (Dict{str:SpotnetSlaveClient}): A dict mapping
            slave UUIDs to the appropriate client.
        slave_dict_by_ws (Dict{WebSocketServerProtocol:SpotnetSlaveClient}):
            Similar to the ``slave_dict_by_uuid`` attribute, but keyed by
            open WebSocket connections.
        logger (logging.Logger): A logger instance for this server.

    """

    def __init__(self, port, keyphrase, do_advertise, voting_enabled,
                 votes_for_skip):
        self.port = port
        self.keyphrase = keyphrase
        self.do_advertise = do_advertise
        self.voting_enabled = voting_enabled
        self.votes_for_skip = votes_for_skip
        self.slave_dict_by_uuid = {}
        self.slave_dict_by_ws = {}
        self.logger = get_configured_logger(SPOTNET_MASTER_LOGGER_NAME)

    def get_run_forever_coro(self):
        """Get a Task to run this server."""
        ws_coro = websockets.serve(self._ws_handler, 'localhost', self.port)

        if self.do_advertise:
            # TODO: implement advertisement properly
            run_forever_coro = asyncio.gather(
                asyncio.ensure_future(self._advertse()),
                asyncio.ensure_future(ws_coro))
        else:
            self.logger.info('Skipping service advertisement.')
            run_forever_coro = asyncio.ensure_future(ws_coro)

        return run_forever_coro

    async def _ws_handler(self, ws, path):
        """Base WebSocket coroutine, to interface with websockets library."""
        try:
            data = await ws.recv()
            json_dict = json.loads(data)
            sender = json_dict.get('sender')
            if sender == 'slave':
                await self._handle_slave_connection(ws, json_dict)
            elif sender == 'web-client':
                await self._handle_web_client_connection(ws, json_dict)
            elif sender is None:
                raise ValueError('No "sender" entry in request.')
            else:
                raise ValueError('Invalid "sender" entry in request.')
        except ConnectionClosed as e:
            self.logger.warn('Unexpected closed WebSocket connection.')
        except ValueError as e:
            self.logger.error('Invalid message received: ' + repr(e))
        except Exception as e:
            self.logger.error('Received unexpected error: ' + repr(e))
        finally:
            # only clean up slave WebSockets;
            # web client connections are expected to end frequently
            if ws in self.slave_dict_by_ws:
                ws_uuid = self.slave_dict_by_ws[ws].uuid

                self.logger.info('Cleaning up slave WebSocket with uuid {}.'
                                 .format(ws_uuid))

                self.slave_dict_by_ws.pop(ws, None)
                self.slave_dict_by_uuid.pop(ws_uuid, None)
            else:
                self.logger.info('Web client WebSocket disconnected.')

    async def _handle_web_client_connection(self, ws, json_dict):
        """Coroutine to handle a WebSocket connection from the web client.

        Args:
            websocket (websockets.server.WebSocketServerProtocol): The open
                slave WebSocket connection.
            json_dict (dict): The JSON-like dict that was sent when this
                connection was initially open (on the first recv).

        """
        self.logger.info('Received connection from web client.')

        web_client = SpotnetWebClient(ws)

        state_json = self._get_state()
        await web_client.send_state(state_json)

        self.logger.info('Sent system state to web client.')

        while True:
            resp = await web_client.recv_json()
            status = resp.get('status')
            data = resp.get('data')

            if status is None:
                raise ValueError('No "status" key on web client request.')
            elif data is None:
                raise ValueError('No "data" key on web client request.')
            elif status == 'send-credentials':
                uuid = data['uuid']
                slave = self.slave_dict_by_uuid[uuid]

                await slave.send_credentials(
                    data['name'], data['username'], data['password'])

                self.logger.info(
                    'Sent credentials to slave with UUID {0}, assigning '
                    'name {1}.'.format(slave.uuid, slave.name))
            else:
                raise ValueError(
                    'Invalid "status" key "{}" received from web client.'
                    .format(status))

    async def _handle_slave_connection(self, ws, json_dict):
        """Coroutine to handle a WebSocket connection from a slave server.

        Args:
            websocket (websockets.server.WebSocketServerProtocol): The open
                slave WebSocket connection.
            json_dict (dict): The JSON-like dict that was sent when this
                connection was initially open (on the first recv).

        """
        self.logger.info('Received connection from slave server.')

        slave = SpotnetSlaveClient(ws)
        self.slave_dict_by_ws[ws] = slave
        self.slave_dict_by_uuid[slave.uuid] = slave

        self.logger.info('Generated slave with UUID {}.'.format(slave.uuid))

        while True:
            # keep WebSocket alive, but don't expect slave to send anything
            resp = await ws.recv()
            self.logger.info('Received slave response {}.'.format(resp))

    async def _advertise(self):
        """Advertise this service via Zeroconf."""
        # TODO
        pass

    def _get_state(self):
        """Return the entire state of the system as a JSON-like dict."""
        return {
            'data': {
                'voting-enabled': self.voting_enabled,
                'votes-for-skip': self.votes_for_skip,
                'slaves': [slave.get_state() for _, slave in
                           self.slave_dict_by_ws.items()]
            }
        }
