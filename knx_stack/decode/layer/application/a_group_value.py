from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import knx_stack


class GroupData(NamedTuple):
    asap: knx_stack.ASAP
    dpt: knx_stack.datapointtypes.DPT


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[GroupData]:
    """Decode an A_GroupValue application PDU from raw message bytes.

    Reads and assembles the DPT value from the message bytes and returns a
    list of GroupData named tuples, one for each associated ASAP and DPT.
    """
    associations = []
    for asap, dpt in state.get_asaps_and_dpts():
        data = dpt()
        value = 0
        head, body = msg.octect()
        while body:
            value <<= 8
            value += head.value
            head, body = body.octect()
        value <<= 8
        value += head.value
        data.value = value
        associations.append(GroupData(asap=asap, dpt=data))
    return associations
