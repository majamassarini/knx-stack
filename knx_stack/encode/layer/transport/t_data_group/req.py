from __future__ import annotations
from knx_stack.encode.layer.network.n_data_group import req
from knx_stack.encode.layer.transport.t_data_group.encode import tl_encode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def encode(state: knx_stack.State, msg: knx_stack.Msg) -> knx_stack.Msg:
    new_msg = tl_encode(state, msg)
    final_msg = req.encode(state, new_msg)
    return final_msg
