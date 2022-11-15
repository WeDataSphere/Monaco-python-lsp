import json
import logging
import subprocess
import threading
import os

from tornado import ioloop, process, web, websocket

from pyls_jsonrpc import streams

from lxpy import copy_headers_dict

log = logging.getLogger(__name__)


class LanguageServerWebSocketHandler(websocket.WebSocketHandler):
    """Setup tornado websocket handler to host an external language server."""
    log.info("=========LanguageServerWebSocketHandler=======")
    writer = None
    map_catch = {}

    def open(self, *args, **kwargs):
        log.info("Spawning pyls subprocess")

        # Create an instance of the language server
        proc = process.Subprocess(
            ['pyls', '-v'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        cookie = self.absolve_cookie()
        log.info("====================headers=================")
        log.info(cookie)
        log.info("====================headers=================")
        global map_catch
        self.map_catch[cookie] = proc.pid

        log.info("================pid================")
        log.info(self.map_catch)
        log.info("================pid================")

        # Create a writer that formats json messages with the correct LSP headers
        self.writer = streams.JsonRpcStreamWriter(proc.stdin)

        # Create a reader for consuming stdout of the language server. We need to
        # consume this in another thread
        def consume():
            # Start a tornado IOLoop for reading/writing to the process in this thread
            ioloop.IOLoop()
            reader = streams.JsonRpcStreamReader(proc.stdout)
            reader.listen(lambda msg: self.write_message(json.dumps(msg)))

        thread = threading.Thread(target=consume)
        thread.daemon = True
        thread.start()

    def on_message(self, message):
        """Forward client->server messages to the endpoint."""
        self.writer.write(json.loads(message))

    def check_origin(self, origin):
        return True

    def on_close(self) -> None:
        try:
            close_cookie = self.absolve_cookie()
            log.info(close_cookie)
            log.info(self.map_catch)
            os.kill(int(self.map_catch[close_cookie]), 9)
            log.info(True)
            del self.map_catch[close_cookie]
        except:
            log.info(False)
        log.info("=============on_close==============")

    def absolve_cookie(self):
        header_dict = copy_headers_dict(str(self.request.headers))
        return header_dict['Cookie']


if __name__ == "__main__":
    print("=========main=========")
    app = web.Application([
        (r"/python", LanguageServerWebSocketHandler),
    ])
    app.listen(3001)
    ioloop.IOLoop.current().start()
    print("=========main=========")
