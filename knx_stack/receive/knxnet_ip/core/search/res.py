import struct
import socket
from collections import namedtuple

Msg = namedtuple('SearchRes', ['ip', 'port', 'individual_address'])


def receive(state, msg):
    """
    >>> import knx_stack
    >>> example = knx_stack.Msg.stringtooctects("004c0801ac1f0afa0e5736010200ffff00000001001e9a2e00000000000e8c000a8a495020496e74657266616365204e313438000000000000000000000000000802020103010401")
    >>> state = knx_stack.State(knx_stack.Medium.knxnet_ip)
    >>> res, state = knx_stack.receive.knxnet_ip.core.search.res.receive(state, knx_stack.Msg(example))
    >>> res
    [SearchRes(ip='172.31.10.250', port=3671, individual_address=0x0200)]
    """
    (size, body) = msg.short()
    (struct_len, body) = body.octect()
    (ipv4_udp, body) = body.octect()
    (ip, body) = body.long()
    (port, body) = body.short()
    (knx_medium, body) = body.octect()
    (device_status, body) = body.octect()
    (individual_address, body) = body.short()
    data = Msg(ip=socket.inet_ntoa(struct.pack('!I', ip.value)),
               port=port.value,
               individual_address=individual_address)
    return [data], state
