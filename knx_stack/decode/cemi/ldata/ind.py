from typing import Iterable, NamedTuple
from knx_stack.definition import layer
from knx_stack.decode.layer.link import l_data


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    (data, body) = layer.L_Data.make_from(msg)
    state.ldata = data
    return l_data.ind.decode(state, body)

