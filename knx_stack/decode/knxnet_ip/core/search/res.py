from typing import Iterable
import struct
import socket
from knx_stack.definition.knxnet_ip.core.search.res import Msg


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[Msg]:
    """
    >>> import knx_stack
    >>> example = knx_stack.Msg.make_from_str("004c0801ac1f0afa0e5736010200ffff00000001001e9a2e00000000000e8c000a8a495020496e74657266616365204e313438000000000000000000000000000802020103010401")
    >>> state = knx_stack.State(knx_stack.Medium.knxnet_ip,
    ...                         knx_stack.AssociationTable(knx_stack.AddressTable(knx_stack.Address(0xAA), [], 255)),
    ...                         knx_stack.GroupObjectTable())
    >>> res = knx_stack.decode.knxnet_ip.core.search.res.decode(state, example)
    >>> res
    [SearchRes(ip=172.31.10.250, port=3671, individual address=0x0200)]
    """
    result = []
    (size, body) = msg.short()
    (struct_len, body) = body.octect()
    (ipv4_udp, body) = body.octect()
    (ip, body) = body.long()
    (port, body) = body.short()
    (knx_medium, body) = body.octect()
    (device_status, body) = body.octect()
    (individual_address, body) = body.short()
    result.append(Msg(ip=socket.inet_ntoa(struct.pack('!I', ip.value)),
                      port=port.value,
                      individual_address=individual_address))
    return result
