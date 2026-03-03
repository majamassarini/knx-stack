from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.definition.layer import NSDU
from knx_stack.decode.layer.transport.t_data_group import con

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    if state.ldata.nsdu == NSDU.T_Data_Group_PDU:
        return con.decode(state, msg)
    return []
