"""CLI for running the Spotnet master server."""

import asyncio
import sys

from argparse import ArgumentParser, RawTextHelpFormatter

from .server import SpotnetMasterServer


def get_parsed_args(args=None):
    """Get the parsed args.

    Args:
        args (List[str]): The list of command line args to parse; if left as
            None, sys.argv will be used.

    Returns:
        Namespace: The Namespace object returned by ArgumentParser.parse_args

    """
    parser = ArgumentParser(
        prog='cli.py',
        description='CLI for the Spotnet master server.',
        formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        '--port',
        dest='port',
        action='store',
        type=int,
        required=True,
        help='The port on which to run the server.')

    parser.add_argument(
        '--keyphrase',
        dest='keyphrase',
        action='store',
        type=str,
        required=True,
        help='The keyphrase required to achieve permissions from the web\n'
             'client.')

    parser.add_argument(
        '--advertise',
        dest='do_advertise',
        action='store_true',
        required=False,
        default=False,
        help='Flag to indicate that the server should advertise itself\n'
             'on the local network.')

    parser.add_argument(
        '--voting-enabled',
        dest='voting_enabled',
        action='store_true',
        required=False,
        default=False,
        help='Flag to indicate that voting for track skipping is\n'
             'enabled on server initialization.')

    parser.add_argument(
        '--votes-for-skip',
        dest='votes_for_skip',
        action='store',
        type=str,
        required=False,
        default=5,
        help='The number of votes required to skip a track.')

    if args is None:
        args = sys.argv[1:]

    return parser.parse_args(args)


def main():
    """The main routine to run the client.
    Returns:
        int: The status code of the routine.
    """
    try:
        opts = get_parsed_args()

        port = opts.port
        keyphrase = opts.keyphrase
        do_advertise = opts.do_advertise
        voting_enabled = opts.voting_enabled
        votes_for_skip = opts.votes_for_skip

        server = SpotnetMasterServer(port, keyphrase, do_advertise,
                                     voting_enabled, votes_for_skip)

        run_forever = server.get_run_forever_coro()
        asyncio.get_event_loop().run_until_complete(run_forever)
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        print('We got an exception :(. Re-raising it.')
        raise e
