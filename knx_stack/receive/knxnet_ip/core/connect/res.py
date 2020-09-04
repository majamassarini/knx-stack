from enum import IntEnum
from collections import namedtuple


Msg = namedtuple('ConnectRes', ['ip', 'port', 'individual_address', 'status'])


class Status(IntEnum):
    E_NO_ERROR = 0x00
    E_CONNECTION_TYPE = 0x22  # connection type not supported
    E_CONNECTION_OPTION = 0x23  # connection option not supported
    E_NO_MORE_CONNECTIONS = 0x24


def receive(state, msg):
    """
    >>> import knx_stack
    >>> example = knx_stack.knxnet_ip.Msg.stringtooctects("00144a000801ac1f0afa0e570404ffff")
    >>> state = knx_stack.State(knx_stack.Medium.knxnet_ip)
    >>> res, state = receive(state, knx_stack.knxnet_ip.Msg(example))
    >>> res
    [ConnectRes(ip='172.31.10.250', port=3671, individual_address=65535, status=0)]
    """
    (size, body) = msg.short()
    (communication_channel_id, body) = body.octect()
    (status, body) = body.octect()
    (ip, port, body) = body.HPAI()
    if status.value == Status.E_NO_ERROR:
        (tunnel_connection, individual_address, body) = body.CRD()
        state.communication_channel_id = communication_channel_id.value
    else:
        individual_address = None
    data = Msg(ip=ip,
               port=port,
               individual_address=individual_address,
               status=status.value)
    return [data], state
