import logging

from .server import _start
from . import datastore


def main():
    """Called from the executable and __main__.py"""
    import argparse

    parser = argparse.ArgumentParser(description='Starts an ActivityWatch server')
    parser.add_argument('--testing', dest='testing', action='store_const',
                        const=True, default=False,
                        help='Run aw-server in testing mode using different ports and database')
    # TODO: Implement datastore.FILES storage method and use it so that there is a storage method
    #       with persistence that does not have any dependencies on external software (such as MongoDB)
    parser.add_argument('--storage', dest='storage',
                        choices=[datastore.MONGODB, datastore.MEMORY, datastore.FILES],
                        default=datastore.MEMORY,
                        help='Uses files as storage method (not supported yet)')

    args = parser.parse_args()

    logger = logging.getLogger("main")
    logging.basicConfig(level=logging.DEBUG if args.testing else logging.INFO)

    if args.testing:
        # TODO: Set logging level for root logger properly
        logger.info("Will run in testing mode")
        logger.debug("Using args: {}".format(args))
        testing = True
        port = 5666
    else:
        testing = False
        port = 5600

    logger.info("Staring up...")
    _start(port=port, testing=testing, storage_method=args.storage)
