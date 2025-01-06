from typing import Iterable
from knx_stack.definition.knxnet_ip.core.disconnect.req import Msg


def decode(state: "knx_stack.State", msg: "knx_stack.Msg") -> Iterable[Msg]:
    """
    >>> import knx_stack
    >>> from knx_stack.decode.knxnet_ip.core.disconnect.req import decode
    >>> example = knx_stack.knxnet_ip.Msg.make_from_str("0010050008017F00000104D2")
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip)
    >>> state.communication_channel_id = 5
    >>> res = decode(state, example)
    >>> res
    [DisconnectReq (control endpoint = 127.0.0.1:1234)]
    """
    result = []
    (size, body) = msg.short()
    (communication_channel_id, body) = body.octect()
    (reserved, body) = body.octect()

    # Decode HPAI (Host Protocol Address Information)
    (ip, port, body) = body.HPAI()

    result.append(
        Msg(
            addr_control_endpoint=ip,
            port_control_endpoint=port,
        )
    )
    return result
