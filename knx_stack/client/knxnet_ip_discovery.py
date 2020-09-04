import struct
import socket
import asyncio
import logging

import knx_stack


class Request(asyncio.DatagramProtocol):

    def __init__(self, local_addr: str, local_port: int):
        """
        A KNXnet IP Discovery request service

        :param local_addr: discovery request instance host ip address
        :param local_port: discovery request instance binding port

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
        self._loop = asyncio.get_event_loop()
        self._transport = None
        self._local_addr = local_addr
        self._local_port = local_port
        self._state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, None, None)

        self.logger = logging.getLogger(__name__)

    def connection_made(self, transport):
        self._transport = transport
        self.logger.info("Connection made: {}".format(str(self._transport)))
        msg = knx_stack.encode_msg(self._state,
                                   knx_stack.knxnet_ip.core.search.req.Msg(addr=self._local_addr,
                                                                           port=self._local_port))
        self.logger.info("encode: {}".format(msg))
        self._transport.sendto(bytearray.fromhex(str(msg)),
                                 (knx_stack.knxnet_ip.DISCOVERY_MULTICAST_ADDR,
                                  knx_stack.knxnet_ip.DISCOVERY_MULTICAST_PORT))

    def connection_lost(self, exc):
        self.logger.error("Connection lost: {}".format(str(exc)))
        self._transport = None

    def error_received(self, exc):
        self.logger.error("Error received: {}".format(str(exc)))

    def datagram_received(self, data, addr):
        self.logger.info("read data:    {}".format(data.hex()))
        self.logger.info("read from:    {}".format(str(addr)))


class Listen(asyncio.DatagramProtocol):
    """
        A KNXnet IP Discovery listener service

        :param local_addr: discovery listener instance host ip address
        :param local_port: discovery listener instance binding port

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

                loop = asyncio.get_event_loop()
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
        self._state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, None, None)

        self.logger = logging.getLogger(__name__)

    def connection_made(self, transport):
        self._transport = transport
        self.logger.info("Connection made: {}".format(str(self._transport)))

    def connection_lost(self, exc):
        self.logger.error("Connection lost: {}".format(str(exc)))
        self._transport = None

    def error_received(self, exc):
        self.logger.error("Error received: {}".format(str(exc)))

    def datagram_received(self, data, addr):
        self.logger.info("read    {}".format(str(data.hex())))
        self.logger.info("read    {}".format(str(addr)))
        search_response = knx_stack.decode_msg(self._state,
                                               knx_stack.knxnet_ip.Msg.make_from_str(data.hex()))
        self.logger.info("read decoded: {}".format(str(search_response)))


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

    loop = asyncio.get_event_loop()
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

