from typing import Iterable, NamedTuple
from knx_stack.decode.layer.transport.t_data_broadcast import con


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    return con.decode(state, msg)
