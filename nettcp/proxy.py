#!/usr/bin/env python2
# encoding: utf-8
# Copyright 2016 Timo Schmid
from __future__ import print_function, unicode_literals, absolute_import
import socket
import logging
import sys
import binascii
import threading
import warnings
import datetime
import http.server
import socketserver
import requests
import jsonpickle
import queue
import time
import json
import base64
import traceback
import subprocess
from io import BytesIO

from nettcp.protocol2xml import parse
from wcf.xml2records import XMLParser
from wcf.records import dump_records, print_records

from nbfx import Nbfx, nbfx_export_values, nbfx_import_values, nbfx_serialize

from kaitaistruct import KaitaiStream

try:
    import SocketServer
except ImportError:
    import socketserver as SocketServer

from .stream.socket import SocketStream
from .nmf import (
    Record,
    EndRecord,
    KnownEncodingRecord,
    UpgradeRequestRecord,
    UpgradeResponseRecord,
    register_types,
)

from wcf.records import Record as WcfRecord

try:
    from .stream.gssapi import GSSAPIStream
except ImportError:
    warnings.warn("gssapi not installed, no negotiate protocol available")
    GSSAPIStream = None
except OSError:
    warnings.warn(
        "KFW is not installed for the Python GSSAPI module, install it from here: https://web.mit.edu/kerberos/kfw-4.1/kfw-4.1.html"
    )
    GSSAPIStream = None

try:
    from helperlib import print_hexdump
except ImportError:
    warnings.warn(
        "python-helperlib not installed, no hexdump available (https://github.com/bluec0re/python-helperlib)"
    )
    print_hexdump = False


logging.basicConfig(level="DEBUG")
log = logging.getLogger(__name__ + ".NETTCPProxy")

trace_file = None

args = None

http_recv_q = queue.Queue()


def print_data(msg, data):
    if log.isEnabledFor(logging.DEBUG):
        print(msg, file=sys.stderr)
        if print_hexdump:
            print_hexdump(data, colored=True, file=sys.stderr)
        else:
            print(data, file=sys.stderr)


class RecvThread(threading.Thread):
    def __init__(self, handler):
        self.stop = threading.Event()
        super(RecvThread, self).__init__()
        self.handler = handler
        self.close_after_next_packet = False

    def run(self):
        log.debug("Handling data coming from the server")
        while not self.stop.is_set():
            obj = Record.parse_stream(self.handler.stream)
            log.debug("Got from server: %r", obj)
            data = obj.to_bytes()

            self.handler.log_data("s>c", data)

            print_data("Got Data from server:", data)
            self.handler.request.sendall(data)

            if obj.code == EndRecord.code:
                self.handler.stop.set()
                if self.stop.is_set():
                    log.info("Server confirmed end")
                    self.handler.stream.close()
                    self.handler.request.close()
                else:
                    log.info("Server requested end")
                    self.stop.wait()

    def terminate(self):
        self.stop.set()


# We have async responses, so we need a separate thread to handle responses
class HttpRecvThread(threading.Thread):
    def __init__(self, s):
        super(HttpRecvThread, self).__init__()
        self.stream = s
        self.stop = threading.Event()

    def run(self):
        log.debug("HTTP Handling data coming from the server")
        global http_recv_q
        while not self.stop.is_set():
            obj = Record.parse_stream(self.stream)
            log.debug("Got from server: %r", obj)
            http_recv_q.put(obj)
            data = obj.to_bytes()
            # self.handler.log_data('s>c', data)

    def terminate(self):
        self.stop.set()


class NETTCPProxy(SocketServer.BaseRequestHandler):
    negotiate = True
    server_name = None

    def log_data(self, direction, data):
        if trace_file is None:
            return

        args = self.client_address + (direction, binascii.b2a_hex(data).decode())
        trace_file.write("{}\t{}:{}\t{}\t{}\n".format(datetime.datetime.today(), *args))
        trace_file.flush()

    def handle(self):
        global args
        log.info("New connection from %s:%d", *self.client_address)
        s = None
        t = None
        self.stop = threading.Event()
        self.negotiated = False
        if args.upstream_url is None:
            s = socket.create_connection((TARGET_HOST, TARGET_PORT))
            self.stream = SocketStream(s)
            t = RecvThread(self)
            # t.daemon = True
        try:
            self.mainloop(s, t)
        finally:
            if args.upstream_url is None:
                t.terminate()

    def mainloop(self, s, t):
        global args

        request_stream = SocketStream(self.request)
        while not self.stop.is_set():
            obj = Record.parse_stream(request_stream)

            log.debug("Client record: %s", obj)
            data = obj.to_bytes()

            self.log_data("c>s", data)

            print_data("Got Data from client:", data)
            if args.upstream_url is None:
                self.stream.write(data)
            else:
                proxies = {"http": args.upstream_proxy}
                full_data = json.loads(jsonpickle.dumps(obj))
                if "Payload" in full_data:
                    try:
                        print("===NEW BLOCK OF EXECUTION===")
                        b64_payload = full_data["Payload"]["py/b64"]
                        binary_decoded_payload = base64.b64decode(b64_payload)
                        print("Original binary data: {}".format(binary_decoded_payload))
                        nbfx = None
                        with KaitaiStream(BytesIO(binary_decoded_payload)) as _io:
                            nbfx = Nbfx(_io)
                            nbfx._read()
                        print("RECORDS LENGTH", len(nbfx.records))
                        # second parameter is a key to the string cache dictionary
                        # it's supposed to be a connection identifier as caches are apparently
                        # maintained in a per-connection basis

                        # Decode using python WCF
                        decoded_payload = parse(
                            binary_decoded_payload, ("127.0.0.1:9000", "c>s")
                        )
                        # print(decoded_payload)

                        # Directly storing the Nbfx object, jsonpickle will serialize it
                        # obj.nbfx=nbfx

                        # Attach editable data to the object
                        obj.wcf_export = nbfx_export_values(nbfx)

                        print("===END EXECUTION===")
                    except ConnectionResetError:
                        print("Connection reset")
                        self.stop.set()
                        return

                resp = requests.post(
                    args.upstream_url, data=jsonpickle.dumps(obj), proxies=proxies
                )

                resp_list = jsonpickle.loads(resp.text)

                if len(resp_list) == 0:
                    print("No response, try further client messages")
                for resp_obj in resp_list:
                    print("Sending object")
                    # resp_obj=jsonpickle.loads(resp.text)
                    self.request.sendall(resp_obj.to_bytes())
                    if resp_obj.code == EndRecord.code:
                        self.stop.set()
                continue
                # self.stream.write(data)
            if obj.code == KnownEncodingRecord.code:
                if self.negotiate:
                    upgr = UpgradeRequestRecord(
                        UpgradeProtocolLength=21,
                        UpgradeProtocol="application/negotiate",
                    ).to_bytes()
                    s.sendall(upgr)
                    resp = Record.parse_stream(SocketStream(s))
                    assert resp.code == UpgradeResponseRecord.code, resp
                    self.stream = GSSAPIStream(self.stream, self.server_name)
                    self.stream.negotiate()
                    self.negotiated = True
                # start receive thread
                t.start()
            elif obj.code == EndRecord.code:
                t.terminate()
                if self.stop.is_set():
                    log.info("Client confirmed end")
                    s.close()
                    self.request.close()
                else:
                    log.info("Client requested end")
                    self.stop.wait()


class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    def _response(self, content):
        self.wfile.write(
            b"HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s"
            % (len(content.encode("utf-8")), content.encode("utf-8"))
        )
        print("got response: {}".format(content))

    def do_POST(self):
        global args
        content_len = int(self.headers.get("Content-Length"))
        post_body = self.rfile.read(content_len)

        obj = jsonpickle.loads(post_body)

        if hasattr(obj, "wcf_export"):
            print("Size:", obj.Size, " len(Payload):", len(obj.Payload))
            with KaitaiStream(BytesIO(obj.Payload)) as _io:
                nbfx = Nbfx(_io)
                nbfx._read()
                nbfx_edited = nbfx_import_values(nbfx, obj.wcf_export)
                nbfx_edited_bytes = nbfx_serialize(nbfx_edited)
                obj.Size = len(nbfx_edited_bytes)
                obj.Payload = nbfx_edited_bytes

        self.server.wcf_stream.write(obj.to_bytes())

        if obj.code == KnownEncodingRecord.code:
            print("Negotiating Kerberos")
            if args.negotiate:
                upgr = UpgradeRequestRecord(
                    UpgradeProtocolLength=21, UpgradeProtocol="application/negotiate"
                ).to_bytes()
                self.server.wcf_stream.write(upgr)
                resp = Record.parse_stream(SocketStream(s))
                assert resp.code == UpgradeResponseRecord.code, resp
                self.server.wcf_stream = GSSAPIStream(self.stream, self.server_name)
                self.server.wcf_stream.negotiate()
                # self.negotiated = True
            # self.http_recv_thread = HttpRecvThread(self.server.wcf_stream)
            # self.http_recv_thread.start()
        # recv=self.server.wcf_stream.read(1024)
        # rec=Record.parse(recv)

        time.sleep(0.5)  # uglyyyy
        ret = []
        while not http_recv_q.empty():
            obj = http_recv_q.get()
            ret.append(obj)
        print("sending response")
        self._response(jsonpickle.dumps(ret))


def main():
    import argparse

    global trace_file, TARGET_HOST, TARGET_PORT, args

    HOST, PORT = "localhost", 8090

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--trace_file", type=argparse.FileType("w"))
    parser.add_argument("-b", "--bind", default=HOST)
    parser.add_argument("-p", "--port", type=int, default=PORT)
    parser.add_argument("-U", "--upstream-url", type=str)
    parser.add_argument("-P", "--upstream-proxy", type=str)
    parser.add_argument("-H", "--http-listener", action="store_true")
    parser.add_argument(
        "-n", "--negotiate", help="Negotiate with the given server name"
    )
    parser.add_argument("TARGET_HOST")
    parser.add_argument("TARGET_PORT", type=int)

    args = parser.parse_args()

    TARGET_HOST = args.TARGET_HOST
    TARGET_PORT = args.TARGET_PORT

    trace_file = args.trace_file

    register_types()

    NETTCPProxy.negotiate = bool(args.negotiate)
    NETTCPProxy.server_name = args.negotiate

    if GSSAPIStream is None and NETTCPProxy.negotiate:
        log.error(
            "GSSAPI not available, negotiation not possible. Try python2 with gssapi"
        )
        sys.exit(1)

    if not args.http_listener:
        server = SocketServer.ThreadingTCPServer((args.bind, args.port), NETTCPProxy)
        server.serve_forever()
    else:
        # Handler = MyHttpRequestHandler
        with socketserver.ThreadingTCPServer(
            ("", args.port), MyHttpRequestHandler
        ) as httpd:
            print("Http Server Serving at port", args.port)
            s = socket.create_connection((TARGET_HOST, TARGET_PORT))
            wcf_stream = SocketStream(s)
            httpd.wcf_stream = wcf_stream
            http_recv_thread = HttpRecvThread(wcf_stream)
            http_recv_thread.start()
            httpd.serve_forever()


if __name__ == "__main__":
    main()
