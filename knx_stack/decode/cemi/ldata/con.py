from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.definition import layer
from knx_stack.decode.layer.link import l_data

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    (data, body) = layer.link.L_Data.make_from(msg)
    state.ldata = data
    return l_data.con.decode(state, body)
