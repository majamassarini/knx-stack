from __future__ import annotations
from knx_stack import Short, Octect, Msg
from knx_stack.encode.layer.link import l_data
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def encode(state: knx_stack.State, msg: knx_stack.Msg) -> knx_stack.Msg:
    """Encode an N_Data_Individual request at the network layer into raw message bytes.

    Prepends the individual destination address and NPDU length to the message,
    then delegates to the link layer L_Data request encoder.
    """
    npdu_length = Octect(value=(len(msg) - 1))
    destination = Short(value=state.individual_address.free_style)
    new_msg = Msg([destination.MSB, destination.LSB, npdu_length] + msg)
    final_msg = l_data.req.encode(state, new_msg)
    return final_msg
