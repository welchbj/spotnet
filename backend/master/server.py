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
        web_client_host_ws (WebSocketServerProtocol): The WebSocket
            representing the current connection from the host of the
            application; i.e., the user that has unlimited privileges for
            modifying data. There may only be one of these connections per
            time with the master server, so this object also acts as a kind of
            lock.
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
        self.web_client_host_ws = None
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

    @asyncio.coroutine
    def _ws_handler(self, ws, path):
        """Base WebSocket coroutine, to interface with websockets library."""
        try:
            data = yield from ws.recv()
            json_dict = json.loads(data)
            sender = json_dict.get('sender')
            if sender == 'slave':
                yield from self._handle_slave_connection(ws, json_dict)
            elif sender == 'web-client':
                yield from self._handle_web_client_connection(ws, json_dict)
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

                if self.web_client_host_ws is not None:
                    # we need to notify the web client of the disonnected slave
                    yield from self.web_client_host_ws.remove_slave(ws_uuid)
                    self.logger.info('Sent web client notice to remove slave '
                                     'with uuid {}.'.format(ws_uuid))
            else:
                self.logger.info('Web client WebSocket disconnected.')
                self.web_client_host_ws = None

    @asyncio.coroutine
    def _handle_web_client_connection(self, ws, json_dict):
        """Coroutine to handle a WebSocket connection from the web client.

        Args:
            websocket (websockets.server.WebSocketServerProtocol): The open
                slave WebSocket connection.
            json_dict (dict): The JSON-like dict that was sent when this
                connection was initially open (on the first recv).

        """
        self.logger.info('Received connection from web client.')

        self.web_client_host_ws = SpotnetWebClient(ws)

        state_json = self._get_state()
        yield from self.web_client_host_ws.send_state(state_json)

        self.logger.info('Sent system state to web client.')

        while True:
            resp = yield from self.web_client_host_ws.recv_json()
            status = resp.get('status')
            data = resp.get('data')

            if status is None:
                raise ValueError('No "status" key on web client request.')
            elif data is None:
                raise ValueError('No "data" key on web client request.')
            elif status == 'send-credentials':
                uuid = data['uuid']
                slave = self.slave_dict_by_uuid[uuid]

                yield from slave.send_credentials(
                    data['name'], data['username'], data['password'])

                self.logger.info(
                    'Sent credentials to slave with UUID {0}, assigning '
                    'name {1}.'.format(slave.uuid, slave.name))
            elif status == 'add-track':
                uuid = data['uuid']
                slave = self.slave_dict_by_uuid[uuid]

                self.logger.info(
                    'Received "add-track" request from web client for slave '
                    'with UUID {}.'.format(uuid))

                position = data['position']
                track = data['track']

                if position == 'current':
                    if slave.is_paused:
                        slave.prepend_track(track)
                    else:
                        slave.replace_first_track(track)
                        yield from slave.send_track()
                elif position == 'next':
                    slave.set_next_track(track)
                else:
                    raise ValueError(
                        'Invalid position key "{}" sent in "add-track" '
                        'directive.'.format(position))

                self.logger.info(
                    'Added track with uri "{0}" on slave with UUID {1}.'
                    .format(track['uri'], uuid))

                yield from self.web_client_host_ws.send_slave_state(
                    slave.get_state())

                self.logger.info(
                    'Sent updated state back to web client for slave with '
                    'UUID {}.'.format(uuid))
            elif status == 'remove-track':
                uuid = data['uuid']
                slave = self.slave_dict_by_uuid[uuid]

                self.logger.info(
                    'Received "remove-track" request from web client for slave '
                    'with UUID {}.'.format(uuid))

                position = data['position']
                if position > (len(slave.track_queue) - 1):
                    self.logger.warn(
                        'Received invalid "position" value {0} from web '
                        'client when attempting to remove track on slave '
                        'with UUID {1}.'.format(position, uuid))
                else:
                    slave.remove_track(position)
                    if position == 0 and not slave.is_paused:
                        yield from slave.send_track()

                yield from self.web_client_host_ws.send_slave_state(
                    slave.get_state())

                self.logger.info(
                    'Sent updated state back to web client for slave with '
                    'UUID {}.'.format(uuid))
            else:
                raise ValueError(
                    'Invalid "status" key "{}" received from web client.'
                    .format(status))

    @asyncio.coroutine
    def _handle_slave_connection(self, ws, json_dict):
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

        if self.web_client_host_ws is not None:
            # need to notify web client of newly connected slave
            yield from self.web_client_host_ws.add_slave(slave.get_state())
            self.logger.info('Sent request to web client to add slave.')

        while True:
            # keep WebSocket alive, but don't expect slave to send anything
            resp = yield from ws.recv()
            self.logger.info('Received slave response {}.'.format(resp))

    @asyncio.coroutine
    def _advertise(self):
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
