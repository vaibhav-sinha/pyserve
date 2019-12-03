import argparse
import yaml
import logging
import signal

from pyserve.server import Server
from pyserve.worker import Worker

logger = logging.getLogger(__name__)
server = Server()
worker = Worker()


def get_args():
    parser = argparse.ArgumentParser(description='Serve your WSGI App')
    parser.add_argument('-c', '--config', dest='config', help='location of the config file', required=True)
    return parser.parse_args()


def setup():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGHUP, shutdown)

    args = get_args()
    with open(args.config, 'r') as stream:
        config = yaml.safe_load(stream)

    logger.info("Running server with following config: %s", str(config))
    server.setup(config)
    worker.setup(config)


def run():
    listener = server.run()
    worker.run(listener)


def shutdown(signum, _):
    logger.warning("Received signal %d. Shutting down.", signum)
    worker.shutdown()
    server.shutdown()
    exit(0)


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(name)s %(asctime)s %(message)s', level=logging.DEBUG)
    setup()
    run()
