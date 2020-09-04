import struct
import socket
import asyncio
import logging

from knx_stack import Medium, layer, datapointtypes
from knx_stack.knxnet_ip import State, Msg, DISCOVERY_MULTICAST_PORT, DISCOVERY_MULTICAST_ADDR, ErrorCodes
from knx_stack import send, receive


class Discovery(asyncio.DatagramProtocol):

    def __init__(self, local_addr, local_port):
        self._loop = asyncio.get_event_loop()
        self._transport = None
        self._local_addr = local_addr
        self._local_port = local_port
        self._state = State(Medium.knxnet_ip, None, None)

        self.logger = logging.getLogger('knxnet_ip.client.Discovery')

    def connection_made(self, transport):
        self._transport = transport
        self.logger.info("Connection made: {}".format(str(self._transport)))
        self._state, msg = send.knxnet_ip.core.search.req.send(self._state,
                                                    send.knxnet_ip.core.search.req.Msg(addr=self._local_addr,
                                                                                       port=self._local_port))
        self.logger.info("send: {}".format(str(msg)))
        self._transport.sendto(bytearray.fromhex(str(msg)),
                               (DISCOVERY_MULTICAST_ADDR, DISCOVERY_MULTICAST_PORT))

    def connection_lost(self, exc):
        self.logger.error("Connection lost: {}".format(str(exc)))
        self._transport = None

    def error_received(self, exc):
        self.logger.error("Error received: {}".format(str(exc)))

    def datagram_received(self, data, addr):
        self.logger.info("read data:    {}".format(data.hex()))
        self.logger.info("read from:    {}".format(str(addr)))


class DiscoveryListener(asyncio.DatagramProtocol):

    def __init__(self, tasks, triggers, commands):
        self._loop = asyncio.get_event_loop()
        self._transport = None
        self._tasks = set(tasks)
        self._listening_addresses = triggers
        self._writing_addresses = commands
        self._state = State(Medium.knxnet_ip, None, None)

        self.logger = logging.getLogger('knxnet_ip.client.Tunneling')

    @property
    def addresses(self):
        return self._listening_addresses.union(self._writing_addresses)

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
        search_response, self._state = receive.knxnet_ip.receive(self._state, Msg(Msg.stringtooctects(data.hex())))
        self.logger.info("read decoded: {}".format(str(search_response)))


class Tunneling(asyncio.DatagramProtocol):

    def __init__(self, tasks, triggers, commands, local_addr, local_port, remote_addr, remote_port):
        address_table = layer.AddressTable(0x0001, [], 255)
        association_table = layer.AssociationTable(address_table, {})
        new_association_table = association_table.associate(0x0F41, 1)
        self._state = State(Medium.knxnet_ip, new_association_table, {1: datapointtypes.DPT_Switch})
        switch_on = datapointtypes.DPT_Switch()
        switch_on.bits.action = datapointtypes.DPT_Switch.Action.on
        self._req_msg_on = send.layer.application.a_group_value_write.req.Msg(asap=1, dpt=switch_on)
        switch_off = datapointtypes.DPT_Switch()
        switch_off.bits.action = datapointtypes.DPT_Switch.Action.off
        self._req_msg_off = send.layer.application.a_group_value_write.req.Msg(asap=1, dpt=switch_off)
        self._loop = asyncio.get_event_loop()
        self._transport = None
        self._tasks = set(tasks)
        self._listening_addresses = triggers
        self._writing_addresses = commands
        self._local_addr = local_addr
        self._local_port = local_port
        self._remote_addr = remote_addr
        self._remote_port = remote_port

        self.logger = logging.getLogger('knxnet_ip.client.Tunneling')

    @property
    def addresses(self):
        return self._listening_addresses.union(self._writing_addresses)

    def connection_made(self, transport):
        self._transport = transport
        self.logger.info("Connection made: {}".format(str(self._transport)))

        self._state, msg = send.knxnet_ip.core.connect.req.send(self._state,
                                                                send.knxnet_ip.core.connect.req.Msg(addr_control_endpoint=self._local_addr,
                                                                                                    port_control_endpoint=self._local_port,
                                                                                                    addr_data_endpoint=self._local_addr,
                                                                                                    port_data_endpoint=self._local_port))
        self.logger.info("send: {}".format(str(msg)))
        self._transport.sendto(bytearray.fromhex(str(msg)), (self._remote_addr, self._remote_port))

    def connection_lost(self, exc):
        self.logger.error("Connection lost: {}".format(str(exc)))
        self._transport = None

    def error_received(self, exc):
        self.logger.error("Error received: {}".format(str(exc)))

    def datagram_received(self, data, addr):
        self.logger.info("read    {}".format(str(data.hex())))
        self.logger.info("read    {}".format(str(addr)))
        responses, self._state = receive.knxnet_ip.receive(self._state, Msg(Msg.stringtooctects(data.hex())))
        for res in responses:
            self.logger.info("read decoded: {}".format(str(res)))
            if isinstance(res, receive.knxnet_ip.core.connect.res.Msg):
                self._state.sequence_counter_remote = 0
                self._state, msg = send.knxnet_ip.core.connectionstate.req.send(self._state,
                                                                                send.knxnet_ip.core.connectionstate.req.Msg(
                                                                                        addr_control_endpoint=self._local_addr,
                                                                                        port_control_endpoint=self._local_port))
                self.logger.info("send: {}".format(str(msg)))
                self._transport.sendto(bytearray.fromhex(str(msg)), (self._remote_addr, self._remote_port))
            if isinstance(res, receive.knxnet_ip.tunneling.req.Msg):
                if res.status == ErrorCodes.E_NO_ERROR:
                    self._state, ack = send.knxnet_ip.tunneling.ack.send(self._state,
                                                            send.knxnet_ip.tunneling.ack.Msg(sequence_counter=res.sequence_counter, status=res.status))
                    self._transport.sendto(bytearray.fromhex(str(ack)), (self._remote_addr, self._remote_port))

    @asyncio.coroutine
    def writer(self):
        while True:
            yield from asyncio.sleep(45)
            self._state, req = send.layer.application.a_group_value_write.req.send(self._state, self._req_msg_on)
            self._transport.sendto(bytearray.fromhex(str(req)), (self._remote_addr, self._remote_port))
            yield from asyncio.sleep(45)
            self._state, req = send.layer.application.a_group_value_write.req.send(self._state, self._req_msg_off)
            self._transport.sendto(bytearray.fromhex(str(req)), (self._remote_addr, self._remote_port))


@asyncio.coroutine
def start_discovery_server(local_addr, local_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', DISCOVERY_MULTICAST_PORT))
    group = socket.inet_aton(DISCOVERY_MULTICAST_ADDR)
    mreq = struct.pack('!4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.setblocking(False)

    transport, protocol = yield from loop.create_datagram_endpoint(
        lambda: Discovery(local_addr, local_port), sock=sock,
    )
    return transport, protocol


@asyncio.coroutine
def start_discovery_listener(local_addr, local_port):
    transport, protocol = yield from loop.create_datagram_endpoint(
        lambda: DiscoveryListener([], [], []), local_addr=(local_addr, local_port),
    )
    return transport, protocol

@asyncio.coroutine
def start_tunneling(local_addr, local_port, remote_addr, remote_port):
    transport, protocol = yield from loop.create_datagram_endpoint(
            lambda: Tunneling([], [], [], local_addr, local_port, remote_addr, remote_port),
            local_addr=(local_addr, local_port),
            remote_addr=(remote_addr, remote_port))
    return transport, protocol


if __name__ == '__main__':
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    root.addHandler(handler)

    loop = asyncio.get_event_loop()
    transport, protocol = loop.run_until_complete(loop.create_task(start_tunneling('172.31.10.149', 5544, '172.31.10.250', 3671)))
    loop.run_until_complete(loop.create_task(protocol.writer()))
    #transport1, protocol = loop.run_until_complete(loop.create_task(start_discovery_listener('172.31.10.149', 5544)))
    #transport2, protocol = loop.run_until_complete(loop.create_task(start_discovery_server('172.31.10.149', 5544)))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("Closing transport...")
    transport.close()
    #transport1.close()
    #transport2.close()
    loop.close()

