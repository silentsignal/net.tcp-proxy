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

# This dict will hold connection data associated to client addresses (e.g. ("127.0.0.1",51234))
http2bin_conn_pool = {}


def print_data(msg, data):
    if log.isEnabledFor(logging.DEBUG):
        print(msg, file=sys.stderr)
        if print_hexdump:
            print_hexdump(data, colored=True, file=sys.stderr)
        else:
            print(data, file=sys.stderr)


# Receiver thread for old TCP mode
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


# Receiver thread for new HTTP connections
# We have async responses, so we need a separate thread to handle responses
class HttpRecvThread(threading.Thread):
    def __init__(self, s, q):
        super(HttpRecvThread, self).__init__()
        self.stream = s
        self.stop = threading.Event()
        self.q = q
        log.info("HTTP receiver start")

    def run(self):
        log.debug("HTTP Handling data coming from the server")
        while not self.stop.is_set():
            try:
                obj = Record.parse_stream(self.stream)
            except ConnectionAbortedError:
                print("HTTP receiver connection aborted, thread exit")
                break
            log.debug("Got from server: %r", obj)
            # Put data to connection-specific queue, the HTTP service will consume it
            self.q.put(obj)
            # data = obj.to_bytes()
            # self.handler.log_data('s>c', data)

    def terminate(self):
        self.stop.set()


# TCP connection handler for raw NMF streams
# In HTTP mode this is the NMF Client<->HTTP part
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
        self.negotiated = False  # Is initial NMF protocol negotiation done?

        # Are we in HTTP proxy mode?
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
            data = obj.to_bytes()

            self.log_data("c>s", data)

            print_data("Got Data from client:", data)

            # Are we in HTTP proxy mode?
            if args.upstream_url is None:
                # If we only proxy raw NMF we just pass the data upstream
                self.stream.write(data)
            else:
                proxies = {"http": args.upstream_proxy}

                # This is wrong and should be fixed
                # full_data = json.loads(jsonpickle.dumps(obj))
                if hasattr(obj, "Payload"):
                    try:
                        print("===NEW BLOCK OF EXECUTION===")
                        # b64_payload = full_data["Payload"]["py/b64"]
                        binary_decoded_payload = (
                            obj.Payload
                        )  # base64.b64decode(b64_payload)
                        print("Original binary data: {}".format(binary_decoded_payload))
                        nbfx = None

                        # Beacuse of read-write mode, we have to explicitly call _read()
                        with KaitaiStream(BytesIO(binary_decoded_payload)) as _io:
                            nbfx = Nbfx(_io)
                            nbfx._read()
                        # TODO error handling

                        # print("RECORDS LENGTH", len(nbfx.records))

                        # Decode using python WCF
                        # second parameter is a key to the string cache dictionary
                        # it's supposed to be a connection identifier as caches are apparently
                        # maintained in a per-connection basis
                        # TODO I have no idea why this needs a static value
                        # If we use self.client_address the second connection results in KeyError in the dictionary
                        decoded_payload = parse(
                            binary_decoded_payload,
                            ("127.0.0.1:9000", "c>s"),  # (self.client_address, "c>s")
                        )

                        # Attach editable data to the object
                        obj.wcf_export = nbfx_export_values(nbfx)

                    except ConnectionResetError:
                        print("Connection reset")
                        self.stop.set()
                        return

                # We mark the object with the client identifier for multiplexing
                obj.client_address = self.client_address

                # Send data to the intercepting HTTP proxy
                resp = requests.post(
                    args.upstream_url, data=jsonpickle.dumps(obj), proxies=proxies
                )

                # Deserialize JSON HTTP response
                # We may receive multiple NMF frames
                try:
                    resp_list = jsonpickle.loads(resp.text)
                except:
                    print(resp.text)
                    raise

                if len(resp_list) == 0:
                    print("No response, try further client messages")

                # Send response NMF objects back in the raw NMF stream
                for resp_obj in resp_list:
                    print("Sending object")
                    # resp_obj=jsonpickle.loads(resp.text)
                    self.request.sendall(resp_obj.to_bytes())
                    if resp_obj.code == EndRecord.code:
                        self.stop.set()
                continue
                # self.stream.write(data)

            # KnownEncodingRecord marks the end of negotiation phase
            # We can start our receiver threads here
            if obj.code == KnownEncodingRecord.code:
                # Kerberos authentication happens here
                if self.negotiate:
                    # Send protocol upgrade request
                    upgr = UpgradeRequestRecord(
                        UpgradeProtocolLength=21,
                        UpgradeProtocol="application/negotiate",
                    ).to_bytes()
                    s.sendall(upgr)
                    # Read response
                    #   SockerStream is net.tcp-proxy's TCP wrapper class
                    #   that is required for NMF deserialization, encryption, etc.
                    resp = Record.parse_stream(SocketStream(s))
                    assert resp.code == UpgradeResponseRecord.code, resp
                    # Wrap the original TCP stream in GSSAPIStream that will handle Karberos
                    self.stream = GSSAPIStream(self.stream, self.server_name)
                    # Negotiate
                    self.stream.negotiate()
                    self.negotiated = True
                # Start receive thread
                t.start()
            # Server closed the connection, exit here
            elif obj.code == EndRecord.code:
                t.terminate()
                if self.stop.is_set():
                    log.info("Client confirmed end")
                    s.close()
                    self.request.close()
                else:
                    log.info("Client requested end")
                    self.stop.wait()


# This is the HTTP Proxy <-> WCF Service part
# A minimalist HTTP server to translate for the target WCF service
class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    # BaseHTTPRequestHandler is really minimalist,
    # we have to handcraft HTTP responses
    def _response(self, content):
        self.wfile.write(
            b"HTTP/1.1 200 OK\r\nContent-Length: %d\r\n\r\n%s"
            % (len(content.encode("utf-8")), content.encode("utf-8"))
        )
        print("got response: {}".format(content))

    # Every incoming HTTP POST triggers this method
    def do_POST(self):
        global args, http_recv_threads

        # BaseHTTPRequestHandler is really minimalist
        # We have to extract the request body ourselves
        content_len = int(self.headers.get("Content-Length"))
        post_body = self.rfile.read(content_len)

        obj = jsonpickle.loads(post_body)
        raw_socket = None  # Python TCP socket
        wcf_stream = None  # net.tcp-proxy SocketStream

        # Look up / initialize global connection pool for multiplexing
        if obj.client_address not in http2bin_conn_pool:
            print(
                "New connection from",
                obj.client_address,
                "to",
                (TARGET_HOST, TARGET_PORT),
            )
            raw_socket = socket.create_connection((TARGET_HOST, TARGET_PORT))
            wcf_stream = SocketStream(
                raw_socket
            )  # SocketStream will reference the underlying TCP socket
            wcf_stream.negotiated = False
            http2bin_conn_pool[obj.client_address] = {"wcf_stream": wcf_stream}
        else:
            wcf_stream = http2bin_conn_pool[obj.client_address]["wcf_stream"]
            raw_socket = wcf_stream._socket

        pool = http2bin_conn_pool[obj.client_address]
        if hasattr(obj, "wcf_export"):
            print("Size:", obj.Size, " len(Payload):", len(obj.Payload))
            with KaitaiStream(BytesIO(obj.Payload)) as _io:
                nbfx = Nbfx(_io)
                nbfx._read()
                nbfx_edited = nbfx_import_values(nbfx, obj.wcf_export)
                nbfx_edited_bytes = nbfx_serialize(nbfx_edited)
                obj.Size = len(nbfx_edited_bytes)
                obj.Payload = nbfx_edited_bytes

        wcf_stream.write(obj.to_bytes())

        if obj.code == KnownEncodingRecord.code:
            # TODO Duplicate code from mainloop()!
            if not wcf_stream.negotiated and args.negotiate:
                print("Negotiating Kerberos")
                upgr = UpgradeRequestRecord(
                    UpgradeProtocolLength=21, UpgradeProtocol="application/negotiate"
                ).to_bytes()
                raw_socket.sendall(upgr)
                resp = Record.parse_stream(wcf_stream)
                assert resp.code == UpgradeResponseRecord.code, resp
                wcf_stream = GSSAPIStream(wcf_stream, args.negotiate)
                wcf_stream.negotiate()
            print("Negotiated!")
            wcf_stream.negotiated = True

            pool["q"] = queue.Queue()  # Message queue dedicated for this connection
            # Start receiver thread, pass msg queue
            t = HttpRecvThread(wcf_stream, pool["q"])
            t.start()
            pool["recv_thread"] = t

        # print("Negotiated?", wcf_stream.negotiated)
        exit_now = False  # Variable to track if any of the received responses was an EndOfStream

        # After negotiation is down we can expect some data in the receive queue
        if wcf_stream.negotiated:
            print("sleeping before we ask for data...")
            timer = 0.1
            # It may take some time to get a response
            # Since the client side is usually synchronized, we better wait a bit
            while pool["recv_thread"].q.empty():
                time.sleep(timer)  # uglyyyy
                timer *= 2
                if timer > 1.0:
                    break

            # Collect responses recevied by the HTTPRecvThread
            ret = []
            while not pool["recv_thread"].q.empty():
                recv_obj = pool["recv_thread"].q.get()
                ret.append(recv_obj)
                # If there is NBFX payload, we include exported data in the HTTP response
                # The response data is read-only for now!
                # Note: if you want to include the full Nbfx object you shouldn't close _io
                #       before passing it to jsonpickle!
                if hasattr(recv_obj, "Payload"):
                    with KaitaiStream(BytesIO(recv_obj.Payload)) as _io:
                        nbfx = Nbfx(_io)
                        nbfx._read()
                        recv_obj.nbfx = nbfx_export_values(nbfx)
                # Should we close this connection?
                if recv_obj.code == EndRecord.code:
                    exit_now = True
            self._response(jsonpickle.dumps(ret))
        else:
            # If the stream is not negotiated yet, we just send an empty response
            self._response(jsonpickle.dumps([]))

        # Server closed the connection, exit here
        if exit_now:
            pool["recv_thread"].terminate()
            pool["wcf_stream"]._socket.close()
            del http2bin_conn_pool[obj.client_address]


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
        with socketserver.ThreadingTCPServer(
            ("", args.port), MyHttpRequestHandler
        ) as httpd:
            print("Http Server Serving at port", args.port)
            httpd.serve_forever()


if __name__ == "__main__":
    main()
