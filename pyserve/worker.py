import logging
import queue
import threading
from typing import Type

from pyserve.gateway import DummyGateway, WSGI

logger = logging.getLogger(__name__)


class Worker:

    is_stopped = False

    def setup(self, config):
        self.config = config

        # What should be the size of this queue?
        self.queue = queue.Queue(maxsize=config.get('concurrency', 10))

        app_type = config.get('app-type', 'dummy')
        if app_type == 'dummy':
            self.gateway = DummyGateway()
        elif app_type == 'wsgi':
            self.gateway = WSGI(config['app-loc'], config['app-module'], config['app'])

        self.kill_pill = threading.Event()

        # Is using threads ok?
        threads = [RequestProcessorThread(name=f'RequestProcessor {i}', queue=self.queue, kill_pill=self.kill_pill, gateway=self.gateway) for i in range(config.get('concurrency', 10))]
        for t in threads:
            t.start()

    def run(self, listener):
        logger.info("Accepting connections now")
        while not self.is_stopped:
            sock, _ = listener.accept()
            self.submit(sock)

    def submit(self, sock):
        try:
            self.queue.put(sock, timeout=self.config.get('timeout', 5))
        except queue.Full:
            # What should we do here?
            pass

    def shutdown(self):
        self.is_stopped = True
        self.kill_pill.set()


class RequestProcessorThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None, queue:queue.Queue=None, kill_pill=None, gateway=None, args=(), kwargs=None):
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs)
        self.queue: Type[queue.Queue] = queue
        self.kill_pill = kill_pill
        self.gateway = gateway

    def run(self) -> None:
        logger.info(f"Running thread {self.name}")
        while not self.kill_pill.is_set():
            try:
                socket = self.queue.get(block=True, timeout=1)
                self.process(socket)
            except queue.Empty:
                continue

    def process(self, sock):
        # Should we read the body?
        # Do we decide to read the body if method is not GET?
        # What if we read the body even if method is GET?
        # Does the server need to read the body or should we let the application read it?
        chunk = sock.recv(1000)
        parts = chunk.decode("utf-8").split('\r\n')
        parts = parts[0].split(' ')
        path = parts[1]

        def write(data):
            sock.send(data)

        self.gateway.process(path, sock, write)

        # Should we close the connection?
        sock.close()

