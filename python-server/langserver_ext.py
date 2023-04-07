import json
import subprocess
import threading
import os
import requests
from properties_read import Properties
from filter_util import filter_list_item1, filter_list_item2, read_file
from langserver_timer import timer_task
from logging_config import GetLog

from tornado import ioloop, process, web, websocket

from pylsp_jsonrpc import streams

from lxpy import copy_headers_dict

log = GetLog(os.path.basename(__file__)).get_log()


class LanguageServerWebSocketHandler(websocket.WebSocketHandler):
    """Setup tornado websocket handler to host an external language server."""
    log.info("=========LanguageServerWebSocketHandler=======")
    writer = None
    map_catch = {}
    py_content = read_file('./python-server/pre-import/pre_compile_py.py')
    python_content = read_file('./python-server/pre-import/pre_compile_python.py')

    def __init__(self, *args, **kwargs):
        log.info("python-server开始初始化：")
        super().__init__(*args, **kwargs)
        self.cookie = self.absolve_cookie()
        self.pid = None
        # 读取配置文件
        properties = Properties("params.properties").getProperties()
        self.server_address = properties["linkis_server_address"]
        self.python_python_version = self.get_python_version(
            self.server_address + "/api/rest_j/v1/configuration/getFullTreesByAppName",
            {"creator": "IDE", "engineType": "python", "version": "python2"})
        self.spark_python_version = self.get_python_version(
            self.server_address + "/api/rest_j/v1/configuration/getFullTreesByAppName",
            {"creator": "IDE", "engineType": "spark", "version": "2.4.3"})
        # 读取python spark预编译文件
        self.py_pre_line = LanguageServerWebSocketHandler.py_content['num_lines']
        self.py_pre_content = LanguageServerWebSocketHandler.py_content['content']
        log.info("read py pre-compile file result: %s", LanguageServerWebSocketHandler.py_content)
        self.python_pre_line = LanguageServerWebSocketHandler.python_content['num_lines']
        self.python_pre_content = LanguageServerWebSocketHandler.python_content['content']
        log.info("read python pre-compile file result: %s", LanguageServerWebSocketHandler.python_content)

    # 解析python_version
    def get_python_version(self, url, params):
        log.debug("get_python_version cookie:%s", self.cookie)
        result = requests.get(url, params, headers={"Cookie": self.cookie})
        if result.ok and result.json():
            log.info("get_python_version request url: %s", result.url)
            data = result.json()["data"]["fullTree"]
            fullTree = list(filter(filter_list_item1, data))[0]
            config_python_version = list(filter(filter_list_item2, fullTree["settings"]))[0]["configValue"]
            default_python_version = list(filter(filter_list_item2, fullTree["settings"]))[0]["defaultValue"]
            python_version = config_python_version if config_python_version != '' else default_python_version
            log.info("default_python_version: %s, config_python_version: %s", default_python_version,
                     config_python_version)
        else:
            log.error("call linkis error: %s ", result.raise_for_status())
        log.info("call url get python_version is %s", python_version)
        return python_version

    def open(self, *args, **kwargs):
        log.info("Spawning pylsp subprocess")

        # Create an instance of the language server
        proc = process.Subprocess(
            ['./bin/python3', './bin/pylsp', '-vv'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        log.info("====================cookie=================")
        log.info(self.cookie)
        log.info(proc.pid)
        log.info("==================cookie-end=================")
        global map_catch
        self.pid = proc.pid
        cookie_map = self.map_converse()
        if self.map_catch != {}:
            for keys in list(self.map_catch.keys()):
                if keys == self.cookie and self.map_catch[keys] != proc.pid:
                    self.map_catch[self.cookie].append(proc.pid)
                elif keys != self.cookie:
                    self.map_catch.update(cookie_map)
        else:
            self.map_catch.update(cookie_map)
        log.info("================map_catch================")
        log.info(self.map_catch)
        log.info("=============catch-end==============")

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
        context = json.loads(message)
        if context["method"] == "textDocument/changePage":
            log.info("cookie %s call method changePage, pylsp process will be kill", self.cookie)
            self.on_close()
        else:
            if context["method"] == "textDocument/didOpen":
                context["params"]["textDocument"].update({"pythonVersion": self.python_python_version})
                if os.path.splitext(context["params"]["textDocument"]["uri"])[-1] == ".py":
                    context["params"]["textDocument"]["text"] = self.py_pre_content + context["params"]["textDocument"][
                        "text"]
                    context["params"]["textDocument"]["preLine"] = self.py_pre_line
                else:
                    context["params"]["textDocument"]["text"] = self.python_pre_content + context["params"]["textDocument"][
                        "text"]
                    context["params"]["textDocument"]["preLine"] = self.python_pre_line
                log.info("request method didOpen:%s", context)
            elif context["method"] == "textDocument/didChange":
                context["params"]["textDocument"].update({"pythonVersion": self.python_python_version})
                if os.path.splitext(context["params"]["textDocument"]["uri"])[-1] == ".py":
                    for range in context["params"]["contentChanges"]:
                        range['range']['start']['line'] = range['range']['start']['line'] + self.py_pre_line
                        range['range']['end']['line'] = range['range']['end']['line'] + self.py_pre_line
                    context["params"]["textDocument"]["preLine"] = self.py_pre_line
                else:
                    for range in context["params"]["contentChanges"]:
                        range['range']['start']['line'] = range['range']['start']['line'] + self.python_pre_line
                        range['range']['end']['line'] = range['range']['end']['line'] + self.python_pre_line
                    context["params"]["textDocument"]["preLine"] = self.python_pre_line
                log.info("request method didChange:%s", context)
            elif context["method"] == "textDocument/completion":
                context["params"]["textDocument"].update({"pythonVersion": self.python_python_version})
                if os.path.splitext(context["params"]["textDocument"]["uri"])[-1] == ".py":
                    context['params']['position']['line'] = context['params']['position']['line'] + self.py_pre_line
                else:
                    context['params']['position']['line'] = context['params']['position']['line'] + self.python_pre_line
            log.info("request method completion:%s", context)
            self.writer.write(context)

    def check_origin(self, origin):
        return True

    def on_close(self) -> None:
        log.info("=============on_close==============")
        log.info("=========before catch========")
        log.info("before on_close map_catch:%s ", self.map_catch)
        if self.map_catch != {}:
            for pid in self.map_catch[self.cookie]:
                try:
                    log.info("<<<<<<kill pid>>>>>")
                    log.info(pid)
                    os.kill(int(pid), 9)
                    log.info(True)
                except Exception as err:
                    log.error(err)
            del self.map_catch[self.cookie]
            log.info("=======after delete map_catch:=======")
            log.info("after kill pylsp process map_catch: %s", self.map_catch)
        log.info("==========close-end==============")

    def absolve_cookie(self):
        header_dict = copy_headers_dict(str(self.request.headers))
        log.info(header_dict)
        if 'Cookie' in header_dict:
            return header_dict['Cookie']
        else:
            return None

    def map_converse(self):
        return {self.cookie: [self.pid]}


if __name__ == "__main__":
    timer_task()
    app = web.Application([
        (r"/python", LanguageServerWebSocketHandler),
    ])
    app.listen(3001)
    ioloop.IOLoop.current().start()
