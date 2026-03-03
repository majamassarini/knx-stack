from __future__ import annotations
from knx_stack import Short, Octect, Msg
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def nl_encode(state: knx_stack.State, msg: knx_stack.Msg) -> knx_stack.Msg:
    """Encode an N_Data_Group PDU at the network layer into raw message bytes.

    Prepends the destination group address and NPDU length to the message using
    the first registered address from the state.
    """
    new_msg = msg
    for address in state.get_addresses():
        npdu_length = Octect(value=(len(msg) - 1))
        destination = Short(value=address.free_style)
        new_msg = Msg([destination.MSB, destination.LSB, npdu_length] + msg)
        break  # just the first address is the encodeing address...
    return new_msg
