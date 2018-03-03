from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from data import PicSQL
from pico import find_imgs, create_pic, create_response, patterns

import json
import os
import base64
from urllib import parse
from urllib.request import unquote

import pprint


class PicoHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)

        if not self.path.startswith("/api"):
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()
        elif self.path == "/api/path/home/hakyell/Pictures":
            buf = b"work, work, kill bug"
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(buf)

        elif self.path.startswith("/api/search"):
            self.send_header("Content-type", "application/json")
            self.end_headers()
            dirpath = parse.urlsplit(self.path).query.split("=", 1)[-1]
            tmp = dirpath.split("&")
            dirpath = tmp[1][5:]
            f = tmp[0]
            print(f)
            dirpath = unquote(dirpath)
            if os.path.isdir(dirpath):
                res = f + create_response(create_pic(find_imgs(dirpath, patterns)))
                # print(res)
                res = res.encode("utf-8")
                self.wfile.write(res)
            print(dirpath)

        elif self.path.startswith("/api/test"):
            self.send_header("Content-type", "application/json")
            self.end_headers()
            res = {
                "md5": "85e22171db75eacc989c8bc109a3d552",
                "size": 513530,
                "pubtime": None,
                "startime": 1516260429,
                "r18": 1,
                "score": None,
                "name": "58204218_p0.jpg",
                "illustor": None,
                "dir": "/home/hakyell/Pictures",
            }
            res["file"] = "data:image/{0};base64,{1}".format(
                res["name"].rsplit(".", 1)[1],
                base64.b64encode(open("/home/hakyell/Pictures/58204218_p0.jpg" ,"rb").read()).decode('utf-8')
            )
            jres = json.dumps(res)
            self.wfile.write(jres.encode("utf-8"))




def run(server_class=HTTPServer, handler_class=PicoHandler):
    server_address = ("", 65210)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
