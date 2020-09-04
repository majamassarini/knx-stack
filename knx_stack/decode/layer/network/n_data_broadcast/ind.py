from typing import Iterable, NamedTuple
from knx_stack.decode.layer.transport.t_data_broadcast import ind


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    return ind.decode(state, msg)
