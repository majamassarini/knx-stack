from __future__ import annotations
from knx_stack.encode.cemi.ldata import ind
from knx_stack.encode.layer.link.l_data.encode import ll_encode
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def encode(state: knx_stack.State, msg: knx_stack.Msg) -> knx_stack.Msg:
    new_msg = ll_encode(state, msg)
    final_msg = ind.encode(state, new_msg)
    return final_msg
