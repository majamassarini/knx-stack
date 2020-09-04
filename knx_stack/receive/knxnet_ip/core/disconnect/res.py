from collections import namedtuple
from knx_stack.knxnet_ip import ErrorCodes


Msg = namedtuple('DisconnectRes', ['communication_channel_id', 'status'])


def receive(state, msg):
    """
    >>> import knx_stack
    >>> example = knx_stack.knxnet_ip.Msg.stringtooctects("00080500")
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip)
    >>> res, state = receive(state, knx_stack.knxnet_ip.Msg(example))
    >>> res
    [DisconnectRes(communication_channel_id=5, status=0)]
    """
    (size, body) = msg.short()
    (communication_channel_id, body) = body.octect()
    (status, body) = body.octect()
    if status.value == ErrorCodes.E_NO_ERROR:
        state.communication_channel_id = 0
        data = Msg(communication_channel_id=communication_channel_id.value,
                   status=status.value)
    return [data], state
