from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.definition.layer import AddressType
from knx_stack.decode.layer import network

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    result: Iterable[NamedTuple] = []
    if state.ldata.address_type == AddressType.individual:
        result = network.n_data_individual.con.decode(state, msg)
    elif (
        state.ldata.address_type == AddressType.group
        and state.ldata.destination != 0
    ):
        result = network.n_data_group.con.decode(state, msg)
    elif (
        state.ldata.address_type == AddressType.group
        and state.ldata.destination == 0
    ):
        result = network.n_data_broadcast.con.decode(state, msg)
    return result
