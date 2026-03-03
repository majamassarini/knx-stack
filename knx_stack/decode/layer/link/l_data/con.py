from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.definition.layer import AddressType
from knx_stack.decode.layer import network

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    """Decode an L_Data confirmation at the link layer from raw message bytes.

    Inspects the address type in the decoded L_Data state and dispatches to
    the appropriate network layer confirmation decoder (individual, group, or
    broadcast).
    """
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
