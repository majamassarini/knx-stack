from typing import Iterable
from knx_stack.definition.knxnet_ip.core.connectionstate.res import Msg, Status


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[Msg]:
    """
    >>> import knx_stack
    >>> example = knx_stack.knxnet_ip.Msg.make_from_str("00087000")
    >>> state = knx_stack.State(knx_stack.Medium.knxnet_ip,
    ...                         knx_stack.AssociationTable(knx_stack.AddressTable(knx_stack.Address(0xAA), [], 255)),
    ...                         knx_stack.GroupObjectTable())
    >>> res = knx_stack.decode.knxnet_ip.core.connectionstate.res.decode(state, example)
    >>> res
    [ConnectionstateRes(status=0)]
    """
    result = []
    (size, body) = msg.short()
    (communication_channel_id, body) = body.octect()
    (status, body) = body.octect()
    result.append(Msg(status=Status(status.value)))
    return result
