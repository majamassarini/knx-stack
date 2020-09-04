from enum import IntEnum
from collections import namedtuple


Msg = namedtuple('ConnectionstateRes', ['status'])


class Status(IntEnum):
    E_NO_ERROR = 0x00
    E_CONNECTION_ID = 0x21  # no active connection id
    E_DATA_CONNECTION = 0x26  # data error in connection id
    E_KNX_CONNECTION = 0x27  # knx subnetwork error in connectiond id


def receive(state, msg):
    """
    >>> import knx_stack
    >>> example = knx_stack.knxnet_ip.Msg.stringtooctects("00087000")
    >>> state = knx_stack.State(knx_stack.Medium.knxnet_ip)
    >>> res, state = receive(state, knx_stack.knxnet_ip.Msg(example))
    >>> res
    [ConnectionstateRes(status=0)]
    """
    (size, body) = msg.short()
    (communication_channel_id, body) = body.octect()
    (status, body) = body.octect()
    data = Msg(status=status.value)
    return [data], state
