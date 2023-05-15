.Net netTcp WCF Binding Framwork
================================

(This is a fork of [ERNW](https://github.com/ernw/net.tcp-proxy)'s [unmaintaned](https://github.com/ernw/net.tcp-proxy/pull/3#issuecomment-1546656400) repo with several bugfixes)

This library implements the MC-NMF, MC-NMFTB and MS-NNS protocols for net.tcp
webservices. It is able to parse and encode the different protocols and interact
as an Man-in-the-Middle proxy for the negotiate authentication.

This library is meant to be run/installed with **python3**. It should also work with python2.7
(possibly required with GSSAPI). Ensure not to run the proxy.py file directly, as it requires
to be part of a python package. Use **nettcp-proxy** instead.

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
