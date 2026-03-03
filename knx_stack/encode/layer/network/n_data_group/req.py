from __future__ import annotations
from knx_stack.encode.layer.link import l_data
from knx_stack.encode.layer.network.n_data_group.encode import nl_encode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def encode(state: knx_stack.State, msg: knx_stack.Msg) -> knx_stack.Msg:
    """Encode an N_Data_Group request at the network layer into raw message bytes.

    Applies network-layer group data encoding, then delegates to the link
    layer L_Data request encoder.
    """
    new_msg = nl_encode(state, msg)
    final_msg = l_data.req.encode(state, new_msg)
    return final_msg
