import struct
import socket
import asyncio
import logging

import knx_stack


class Request(asyncio.DatagramProtocol):
    """
    A KNXnet/IP Discovery request service.

    Sends a KNXnet/IP search request to the multicast group and logs any
    search responses that arrive on the same socket.

    :param local_addr: host IP address used as the discovery request source
    :param local_port: UDP port bound to the discovery request socket

    Example::

        async def send_discovery_request(local_addr: str, local_port: int):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('', knx_stack.knxnet_ip.DISCOVERY_MULTICAST_PORT))
            group = socket.inet_aton(knx_stack.knxnet_ip.DISCOVERY_MULTICAST_ADDR)
            mreq = struct.pack('!4sL', group, socket.INADDR_ANY)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            sock.setblocking(False)

            transport, protocol = await loop.create_datagram_endpoint(
                lambda: Request(local_addr, local_port), sock=sock,
            )
            return transport, protocol

    """

    def __init__(self, local_addr: str, local_port: int):
        self._transport = None
        self._local_addr = local_addr
        self._local_port = local_port
        self._state = knx_stack.knxnet_ip.State(
            knx_stack.Medium.knxnet_ip, None, None
        )

        self.logger = logging.getLogger(__name__)

    def connection_made(self, transport):
        """Store the transport and immediately transmit a KNXnet/IP search request."""
        self._transport = transport
        self.logger.info("Connection made: {}".format(str(self._transport)))
        msg = knx_stack.encode_msg(
            self._state,
            knx_stack.knxnet_ip.core.search.req.Msg(
                addr=self._local_addr, port=self._local_port
            ),
        )
        self.logger.info("encode: {}".format(msg))
        self._transport.sendto(
            bytearray.fromhex(str(msg)),
            (
                knx_stack.knxnet_ip.DISCOVERY_MULTICAST_ADDR,
                knx_stack.knxnet_ip.DISCOVERY_MULTICAST_PORT,
            ),
        )

    def connection_lost(self, exc):
        """Log the error and clear the stored transport when the connection is lost."""
        self.logger.error("Connection lost: {}".format(str(exc)))
        self._transport = None

    def error_received(self, exc):
        """Log any transport-level error received from the remote end."""
        self.logger.error("Error received: {}".format(str(exc)))

    def datagram_received(self, data, addr):
        """Log the raw datagram payload and its source address."""
        self.logger.info("read data:    {}".format(data.hex()))
        self.logger.info("read from:    {}".format(str(addr)))


class Listen(asyncio.DatagramProtocol):
    """
    A KNXnet/IP Discovery listener service.

    Listens on a dedicated UDP endpoint for KNXnet/IP search responses and
    decodes each incoming datagram using the KNX stack.

    :param local_addr: host IP address bound to the discovery listener socket
    :param local_port: UDP port bound to the discovery listener socket

    Example::

        async def listen_discovery_responses(local_addr: str, local_port: int):
            transport, protocol = await loop.create_datagram_endpoint(
                lambda: Listen(), local_addr=(local_addr, local_port),
            )
            return transport, protocol

        if __name__ == '__main__':
            import sys

            root = logging.getLogger()
            root.setLevel(logging.DEBUG)
            handler = logging.StreamHandler(sys.stdout)
            root.addHandler(handler)

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            transport1, _ = loop.run_until_complete(loop.create_task(listen_discovery_responses('172.31.10.111', 5544)))
            transport2, _ = loop.run_until_complete(loop.create_task(send_discovery_request('172.31.10.111', 5544)))

            try:
                loop.run_forever()
            except KeyboardInterrupt:
                pass
            print("Closing transport...")
            transport1.close()
            transport2.close()
            loop.close()
    """

    def __init__(self):
        self._transport = None
        self._state = knx_stack.knxnet_ip.State(
            knx_stack.Medium.knxnet_ip, None, None
        )

        self.logger = logging.getLogger(__name__)

    def connection_made(self, transport):
        """Store the transport once the UDP endpoint is ready."""
        self._transport = transport
        self.logger.info("Connection made: {}".format(str(self._transport)))

    def connection_lost(self, exc):
        """Log the error and clear the stored transport when the connection is lost."""
        self.logger.error("Connection lost: {}".format(str(exc)))
        self._transport = None

    def error_received(self, exc):
        """Log any transport-level error received from the remote end."""
        self.logger.error("Error received: {}".format(str(exc)))

    def datagram_received(self, data, addr):
        """Decode and log an incoming KNXnet/IP search response datagram."""
        self.logger.info("read    {}".format(str(data.hex())))
        self.logger.info("read    {}".format(str(addr)))
        search_response = knx_stack.decode_msg(
            self._state, knx_stack.knxnet_ip.Msg.make_from_str(data.hex())
        )
        self.logger.info("read decoded: {}".format(str(search_response)))


async def send_discovery_request(local_addr: str, local_port: int):
    """Create a multicast UDP socket and return a Request transport/protocol pair."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", knx_stack.knxnet_ip.DISCOVERY_MULTICAST_PORT))
    group = socket.inet_aton(knx_stack.knxnet_ip.DISCOVERY_MULTICAST_ADDR)
    mreq = struct.pack("!4sL", group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setblocking(False)

    transport, protocol = await loop.create_datagram_endpoint(
        lambda: Request(local_addr, local_port),
        sock=sock,
    )
    return transport, protocol


async def listen_discovery_responses(local_addr: str, local_port: int):
    """Create a UDP endpoint and return a Listen transport/protocol pair."""
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: Listen(),
        local_addr=(local_addr, local_port),
    )
    return transport, protocol


if __name__ == "__main__":
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    root.addHandler(handler)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if len(sys.argv):
        transport1, _ = loop.run_until_complete(
            loop.create_task(listen_discovery_responses(sys.argv[1], 5544))
        )
        transport2, _ = loop.run_until_complete(
            loop.create_task(send_discovery_request(sys.argv[1], 5544))
        )

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("Closing transport...")
    transport1.close()
    transport2.close()
    loop.close()
