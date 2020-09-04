from typing import Iterable
from knx_stack.definition.knxnet_ip import ErrorCodes
from knx_stack.definition.knxnet_ip.core.disconnect.res import Msg


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[Msg]:
    """
    >>> import knx_stack
    >>> example = knx_stack.knxnet_ip.Msg.make_from_str("00080500")
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip)
    >>> res = decode(state, example)
    >>> res
    [DisconnectRes(communication_channel_id=5, status=0)]
    """
    result = []
    (size, body) = msg.short()
    (communication_channel_id, body) = body.octect()
    (status, body) = body.octect()
    if status.value == ErrorCodes.E_NO_ERROR:
        state.communication_channel_id = 0
        result.append(Msg(communication_channel_id=communication_channel_id.value,
                          status=ErrorCodes(status.value)))
    return result
