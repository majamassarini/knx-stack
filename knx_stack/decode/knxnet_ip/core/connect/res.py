from __future__ import annotations
from collections.abc import Iterable
from knx_stack.definition.knxnet_ip.core.connect.res import Msg, Status
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def decode(
    state: knx_stack.State, msg: knx_stack.Msg
) -> Iterable[knx_stack.knxnet_ip.core.connect.res.Msg]:
    """
    >>> import knx_stack
    >>> example = knx_stack.knxnet_ip.Msg.make_from_str("00144a000801ac1f0afa0e570404ffff")
    >>> state = knx_stack.State(knx_stack.Medium.knxnet_ip,
    ...                         knx_stack.AssociationTable(knx_stack.AddressTable(knx_stack.Address(0xAA), [], 255)),
    ...                         knx_stack.GroupObjectTable())
    >>> res = knx_stack.decode.knxnet_ip.core.connect.res.decode(state, example)
    >>> res
    [ConnectRes(ip=172.31.10.250, port=3671, individual address=0xFFFF, status=0)]
    """
    result: list[knx_stack.knxnet_ip.core.connect.res.Msg] = []
    size, body = msg.short()
    communication_channel_id, body = body.octect()
    status, body = body.octect()
    ip, port, body = body.HPAI()  # type: ignore[attr-defined]
    if status.value == Status.E_NO_ERROR:
        tunnel_connection, individual_address, body = body.CRD()  # type: ignore[attr-defined]
        state.communication_channel_id = communication_channel_id.value  # type: ignore[attr-defined]
    else:
        individual_address = None
    result.append(
        Msg(
            ip=ip,
            port=port,
            individual_address=individual_address,
            status=Status(status.value),
        )
    )
    return result
