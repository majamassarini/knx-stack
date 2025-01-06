from knx_stack import Octect, Short
from knx_stack.definition.knxnet_ip import Msg as NetMsg, Services, HEADER_SIZE_10
from knx_stack.encode.knxnet_ip import header


def encode(
    state: "knx_stack.State", msg: "knx_stack.knxnet_ip.core.disconnect.res.Msg"
) -> "knx_stack.Msg":
    """
    >>> import knx_stack
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, None, None)
    >>> state.communication_channel_id = 5
    >>> disconnect_response = knx_stack.knxnet_ip.core.disconnect.res.Msg(
    ...     communication_channel_id=5,
    ...     status=knx_stack.knxnet_ip.ErrorCodes.E_NO_ERROR
    ... )
    >>> bus_msg = knx_stack.encode_msg(state, disconnect_response)
    >>> bus_msg
    0610020A00080500
    """
    new_msg = NetMsg(Short(value=Services.DISCONNECT_RESPONSE.value).octects)
    new_msg += NetMsg(Short(value=(2 + HEADER_SIZE_10)).octects)
    new_msg += NetMsg([Octect(value=msg.communication_channel_id), Octect(value=msg.status)])
    final_msg = header.encode(state, new_msg)
    return final_msg
