"""CLI for running the Spotnet slave server."""

import asyncio
import sys

from argparse import ArgumentParser, RawTextHelpFormatter

from .server import SpotnetSlaveServer


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
        description='CLI for the Spotnet slave server.',
        formatter_class=RawTextHelpFormatter)

    parser.add_argument(
        '--discover',
        dest='do_discover',
        action='store_true',
        required=False,
        default=False,
        help='Flag to indicate that the master server address should be\n'
             'discovered on the local network.')

    parser.add_argument(
        '--master-address',
        dest='master_address',
        action='store',
        required=False,
        help='Optional parameter to indicate the address of the master\n'
             'server, used when discovery mode is not enabled.')

    if args is None:
        args = sys.argv[1:]

    opts = parser.parse_args(args)
    if not opts.do_discover and opts.master_address is None:
        parser.error('Must specify --master-address if --discover option is '
                     'not enabled.')

    return opts


def main():
    """The main routine to run the client.
    Returns:
        int: The status code of the routine.
    """
    try:
        opts = get_parsed_args()

        do_discover = opts.do_discover
        master_address = opts.master_address

        server = SpotnetSlaveServer(do_discover, master_address)

        asyncio.get_event_loop().run_until_complete(server.run_forever())
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        print('We got an exception :(. Re-raising it.')
        raise e
