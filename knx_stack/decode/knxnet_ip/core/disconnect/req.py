from __future__ import annotations
from collections.abc import Iterable
from knx_stack.definition.knxnet_ip.core.disconnect.req import Msg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def decode(
    state: knx_stack.State, msg: knx_stack.Msg
) -> Iterable[knx_stack.knxnet_ip.core.disconnect.req.Msg]:
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
    result: list[knx_stack.knxnet_ip.core.disconnect.req.Msg] = []
    size, body = msg.short()
    communication_channel_id, body = body.octect()
    reserved, body = body.octect()

    # Decode HPAI (Host Protocol Address Information)
    ip, port, body = body.HPAI()  # type: ignore[attr-defined]

    result.append(
        Msg(
            addr_control_endpoint=ip,
            port_control_endpoint=port,
        )
    )
    return result
