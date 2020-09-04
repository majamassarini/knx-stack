import asyncio
import logging
from typing import Iterable, NamedTuple

import knx_stack


class Tunneling(asyncio.DatagramProtocol):
    """
    *A minimal asynchronous KNXnet IP Tunneling Client*.

    :param local_addr: tunneling running host ip address
    :param local_port: tunneling running port bind
    :param remote_addr: knxnet ip gateway ip address
    :param remote_port: knxnet ip gateway listening port

    Example:
        Turn on and off a light::

            async def start_tunneling(local_addr: str, local_port: int, remote_addr: str, remote_port: int,
                                      state: knx_stack.knxnet_ip.State, msgs: Iterable[NamedTuple]):
                transport, protocol = await loop.create_datagram_endpoint(
                        lambda: Tunneling(local_addr, local_port, remote_addr, remote_port, state, msgs),
                        local_addr=(local_addr, local_port),
                        remote_addr=(remote_addr, remote_port))
                return transport, protocol


            if __name__ == '__main__':
                import sys

                root = logging.getLogger()
                root.setLevel(logging.INFO)
                handler = logging.StreamHandler(sys.stdout)
                root.addHandler(handler)

                address_table = knx_stack.AddressTable(knx_stack.Address(0x1004), [], 255)
                association_table = knx_stack.AssociationTable(address_table, {})
                asap_command = knx_stack.ASAP(1, "turn on/off floor light")
                association_table.associate(asap_command, [knx_stack.GroupAddress(free_style=0x0F81)])
                state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, association_table,
                                                  knx_stack.GroupObjectTable({asap_command: knx_stack.datapointtypes.DPT_Switch}))

                msgs = list()

                switch_on = knx_stack.datapointtypes.DPT_Switch()
                switch_on.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.on
                msgs.append(knx_stack.layer.application.a_group_value_write.req.Msg(asap=asap_command, dpt=switch_on))

                switch_off = knx_stack.datapointtypes.DPT_Switch()
                switch_off.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.off
                msgs.append(knx_stack.layer.application.a_group_value_write.req.Msg(asap=asap_command, dpt=switch_off))

                loop = asyncio.get_event_loop()
                transport, protocol = loop.run_until_complete(loop.create_task(start_tunneling('172.31.10.111', 5544, '172.31.10.250', 3671,
                                                                                               state, msgs)))
                loop.run_until_complete(loop.create_task(protocol.writer()))

                transport.close()

    """

    def __init__(self, local_addr: str, local_port: int, remote_addr: str, remote_port: int,
                 state: knx_stack.State, msgs: Iterable[NamedTuple]):
        self._transport = None
        self._local_addr = local_addr
        self._local_port = local_port
        self._remote_addr = remote_addr
        self._remote_port = remote_port
        self._state = state
        self._msgs = msgs
        self.connected = False

        self.logger = logging.getLogger(__name__)

    def connection_made(self, transport):
        self._transport = transport
        self.logger.info("Connection made: {}".format(str(self._transport)))

        connect_msg = knx_stack.knxnet_ip.core.connect.req.Msg(addr_control_endpoint=self._local_addr,
                                                               port_control_endpoint=self._local_port,
                                                               addr_data_endpoint=self._local_addr,
                                                               port_data_endpoint=self._local_port)
        msg = knx_stack.encode_msg(self._state, connect_msg)
        self.send(msg)

    def connection_lost(self, exc):
        self.logger.error("Connection lost: {}".format(str(exc)))
        self._transport = None

    def error_received(self, exc):
        self.logger.error("Error received: {}".format(str(exc)))

    def send(self, msg):
        self._transport.sendto(bytearray.fromhex(str(msg)), (self._remote_addr, self._remote_port))

    def datagram_received(self, data, addr):
        responses = knx_stack.decode_msg(self._state,
                                         knx_stack.knxnet_ip.Msg.make_from_str(data.hex()))
        for res in responses:
            if isinstance(res, knx_stack.knxnet_ip.core.connect.res.Msg):
                self._state.sequence_counter_remote = 0
                connectionstate_msg = knx_stack.knxnet_ip.core.connectionstate.req.Msg(
                    addr_control_endpoint=self._local_addr,
                    port_control_endpoint=self._local_port)
                msg = knx_stack.encode_msg(self._state, connectionstate_msg)
                self.send(msg)
                self.connected = True

            if isinstance(res, knx_stack.knxnet_ip.tunneling.req.Msg):
                self.logger.info("read {}".format(res))
                if res.status == knx_stack.knxnet_ip.ErrorCodes.E_NO_ERROR:
                    tunneling_msg = knx_stack.knxnet_ip.tunneling.ack.Msg(sequence_counter=res.sequence_counter,
                                                                          status=res.status)
                    msg = knx_stack.encode_msg(self._state, tunneling_msg)
                    self.send(msg)

    async def writer(self):
        while not self.connected:
            await asyncio.sleep(1)
        for msg in self._msgs:
            self.logger.info("write {}".format(msg))
            req = knx_stack.encode_msg(self._state, msg)
            self.send(req)
            await asyncio.sleep(3)
        asyncio.get_event_loop().stop()


async def start_tunneling(local_addr: str, local_port: int, remote_addr: str, remote_port: int,
                          state: knx_stack.knxnet_ip.State, msgs: Iterable[NamedTuple]):
    transport, protocol = await loop.create_datagram_endpoint(
            lambda: Tunneling(local_addr, local_port, remote_addr, remote_port, state, msgs),
            local_addr=(local_addr, local_port),
            remote_addr=(remote_addr, remote_port))
    return transport, protocol


if __name__ == '__main__':
    import sys

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    root.addHandler(handler)

    address_table = knx_stack.AddressTable(knx_stack.Address(0x1004), [], 255)
    association_table = knx_stack.AssociationTable(address_table, {})
    asap_command = knx_stack.ASAP(1, "turn on/off floor light")
    association_table.associate(asap_command, [knx_stack.GroupAddress(free_style=0x0F81)])
    state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, association_table,
                                      knx_stack.GroupObjectTable({asap_command: knx_stack.datapointtypes.DPT_Switch}))

    msgs = list()

    switch_on = knx_stack.datapointtypes.DPT_Switch()
    switch_on.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.on
    msgs.append(knx_stack.layer.application.a_group_value_write.req.Msg(asap=asap_command, dpt=switch_on))

    switch_off = knx_stack.datapointtypes.DPT_Switch()
    switch_off.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.off
    msgs.append(knx_stack.layer.application.a_group_value_write.req.Msg(asap=asap_command, dpt=switch_off))

    loop = asyncio.get_event_loop()
    transport, protocol = loop.run_until_complete(loop.create_task(start_tunneling('172.31.10.111', 5544, '172.31.10.250', 3671,
                                                                                   state, msgs)))
    loop.run_until_complete(loop.create_task(protocol.writer()))

    transport.close()

