from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.decode.layer.transport.t_data_broadcast import ind

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    """Decode an N_Data_Broadcast indication at the network layer from raw message bytes.

    Delegates directly to the transport layer T_Data_Broadcast indication decoder.
    """
    return ind.decode(state, msg)
