from __future__ import annotations
from knx_stack import Msg, Octect
from knx_stack.definition import layer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def tl_encode(state: knx_stack.State, msg: knx_stack.Msg) -> knx_stack.Msg:
    """Encode a T_Data_Group PDU at the transport layer into raw message bytes.

    Prepends the transport TPCI byte for a group data PDU when the state has
    registered TSAPs; otherwise returns the message unchanged.
    """
    new_msg = msg
    if state.get_tsaps():
        ldata = layer.L_Data()
        ldata.nsdu = layer.NSDU.T_Data_Group_PDU
        ldata.apci = state.apci  # type: ignore[misc]
        new_msg = Msg([Octect(value=ldata.tpci)] + msg)
    return new_msg
