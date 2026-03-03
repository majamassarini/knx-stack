from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.definition import layer
from knx_stack.decode.layer.link import l_data

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    """Decode a cEMI L_Data confirmation from raw message bytes and update the state.

    Parses the L_Data fields from the message, stores the result in the state,
    and delegates to the link layer L_Data confirmation decoder.
    """
    data, body = layer.link.L_Data.make_from(msg)
    state.ldata = data
    return l_data.con.decode(state, body)
