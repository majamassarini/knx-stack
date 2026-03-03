from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    """Decode a T_Disconnect indication at the transport layer from raw message bytes.

    Not yet implemented; returns an empty result.
    """
    return []  # @todo not yet implemented
