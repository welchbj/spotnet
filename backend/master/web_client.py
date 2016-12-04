"""An implementation for interacting with the Spotnet web client."""

from ..utils import WebSocketWrapper


class SpotnetWebClient(WebSocketWrapper):

    def __init__(self, ws):
        super(SpotnetWebClient, self).__init__(ws)

    async def send_state(self, state_json):
        """Send the system state over the WebSocket connection.

        Args:
            state_json (dict): A JSON-like dict representing the state of the
                system.

        """
        state_json['status'] = 'send-state'
        state_json['sender'] = 'master'
        await self.send_json(state_json)

    async def remove_slave(self, slave_uuid):
        """Coroutine to send a request to remove a slave.

        Args:
            slave_uuid (str): The UUID of the slave to remove.

        """
        await self.send_json({
            'status': 'remove-slave',
            'sender': 'master',
            'data': {
                'uuid': slave_uuid
            }})

    async def add_slave(self, slave_data):
        """Coroutine to send a request to add a slave.

        Args:
            slave_data (dict): A JSON-like dict representing the serialized
                state of a slave node.

        """
        await self.send_json({
            'status': 'add-slave',
            'sender': 'master',
            'data': {
                'slave': slave_data
            }})

    async def send_slave_state(self, slave_data):
        """Coroutine to send the updated state of a slave.

        Args:
            slave_data (dict): A JSON-like dict representing the serialized
                state of a slave node.

        """
        await self.send_json({
            'status': 'send-slave-state',
            'sender': 'master',
            'data': {
                'slave': slave_data
            }})
