

class Client:

    def __init__(self, port, host, thread):
        self.port = port
        self.host = host
        self.thread = thread
        self.thread.start()
