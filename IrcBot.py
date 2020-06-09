import socket
import threading


# Simple Irc Bot with auto-reconnect
class SimpleIrcBot(threading.Thread):
    def __init__(self, host, channel, nickname, password=None, port=6667):
        threading.Thread.__init__(self)
        self.host = host
        self.channel = channel
        self.nickname = nickname
        self.password = password
        self.port = port

    def _start_requests(self):
        pass

    def _check_on_connected(self, response):
        if response:
            return True
        return False

    def __connect(self):
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))

        self._start_requests()

        response = self.socket.recv(1024).decode("utf-8")

        return self._check_on_connected(response)

    def __get_responses(self):
        is_disconnected = True
        while True:
            try:
                while is_disconnected:
                    is_disconnected = not self.__connect()
                response = self.socket.recv(1024).decode("utf-8")
                if len(response) == 0:
                    is_disconnected = True
                elif response == "PING :{}\r\n".format(self.host):
                    self.socket.send("PONG :{}\r\n".format(self.host).encode("utf-8"))
                else:
                    yield response
            except:
                is_disconnected = True

    def _process_response(self, response):
        pass

    def run(self):
        for response in self.__get_responses():
            self._process_response(response)
