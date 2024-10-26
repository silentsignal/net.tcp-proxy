.Net netTcp WCF Binding Framwork
================================

This is a fork of [ERNW](https://github.com/ernw/net.tcp-proxy)'s [unmaintaned](https://github.com/ernw/net.tcp-proxy/pull/3#issuecomment-1546656400) repo with several bugfixes **and HTTP support!**

This library implements the MC-NMF, MC-NMFTB and MS-NNS protocols for net.tcp
webservices. It is able to parse and encode the different protocols and interact
as an Man-in-the-Middle proxy for the negotiate authentication.

This library is meant to be run/installed with **python3**. It should also work with python2.7
(possibly required with GSSAPI). Ensure not to run the proxy.py file directly, as it requires
to be part of a python package. Use **nettcp-proxy** instead.

Usage
-----

In the HTTP setup you'll need 2 instances of this tool.

### Client to HTTP

The following command will create a WCF service on 127.0.0.1:9000, you should redirect the client's traffic there (e.g. modify the config or use the hosts file).

```
python3 nettcp-proxy.py
                        -b 127.0.0.1 # Bind host the client will connect to
                        -p 9000      # Bind port for the client connection
                        -U http://127.0.0.1:10000 # URL of the HTTP to Server proxy (see below)
                        -P http://127.0.0.1:8080  # URL of an intercepting proxy to use
                        127.0.0.1 # Ignored
                        1234      # Ignoded
```

### HTTP to Server

This will create a HTTP server on 127.0.0.1:10000 that will accept the traffic from the intercepting proxy and translate it back for the WCF service. 

```
python3 nettcp-proxy.py
                        -b 127.0.0.1 # Bind host the HTTP proxy will connect to
                        -p 10000     # Bind port the HTTP proxy will connect to
                        -H           # HTTP server mode
                        10.0.0.0.1   # WCF service host
                        9000         # WCF service port
```

If you need Kerberos, configure it here!

---


Old README
==========

<a href="https://asciinema.org/a/71sbvkyjpr0jpmznk36u3ec9q" target="_blank">
<img src="https://asciinema.org/a/71sbvkyjpr0jpmznk36u3ec9q.png" />
</a>

Parse data
----------

Code:

```python
from io import BytesIO
stream = BytesIO(data)

while stream.tell() < len(data):
    record = Record.parse_stream(stream)
```

From trace file (captured by proxy)
```bash
decode-nmf foo.trace
```

Connect to service
------------------

Unencrypted:
```python
import socket
from nettcp.stream.socket import SocketStream
from nettcp.stream.nmf import NMFStream

s = socket.create_connection(('127.0.0.1', 1234))
socket_stream = SocketStream(s)
stream = NMFStream(socket_stream, 'net.tcp://127.0.0.1/Service1')

stream.preamble()
stream.write('...')
```

With GSSAPI:

requesting ticket with krb5
```bash
kvno host/foo.example.com
```

authenticate with python
```python
import socket
from nettcp.stream.socket import SocketStream
from nettcp.stream.nmf import NMFStream

s = socket.create_connection(('127.0.0.1', 1234))
socket_stream = SocketStream(s)
stream = NMFStream(socket_stream, 'net.tcp://127.0.0.1/Service1', 'host@foo.example.com')

stream.preamble()
stream.write('...')
```


Capture connection
------------------

```bash
nettcp-proxy.py -b <localaddr> -p <localport> -t logfile.trace <targetserver> <targetport>
```

Man-in-the-Middle of netTcp with negotiate stream
-------------------------------------------------

```bash
kinit user/foo.example.com
kvno host/foo.example.com
nettcp-proxy.py -b <localaddr> -p <localport> -t logfile.trace -n host@foo.example.com <targetserver> <targetport>
```
