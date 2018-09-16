from threading import Thread
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


class WebSocketHandler(WebSocket):
    def handleConnected(self):
        while True:
            self.sendMessage("hi")


server = SimpleWebSocketServer("0.0.0.0", 8000, WebSocketHandler)
Thread(target=server.serveforever, daemon=True).start()
