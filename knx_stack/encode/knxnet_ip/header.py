from __future__ import annotations
from knx_stack.definition.knxnet_ip import HEADER_SIZE_10, KNXNETIP_VERSION_10
from knx_stack.msg import Msg, Octect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def encode(state: knx_stack.State, msg: knx_stack.Msg) -> knx_stack.Msg:
    final_msg = Msg(
        [Octect(value=HEADER_SIZE_10), Octect(value=KNXNETIP_VERSION_10)] + msg
    )
    return final_msg
