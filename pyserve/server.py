import socket


class Server:

    # http://man7.org/linux/man-pages/man2/socket.2.html

    def setup(self, config):
        self.config = config
        self.socket = None

    def run(self):
        listen_port = self.config['port']
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', listen_port))
        # What is backlog
        self.socket.listen(self.config.get('backlog', 100))
        return self.socket

    def shutdown(self):
        if self.socket:
            self.socket.close()
