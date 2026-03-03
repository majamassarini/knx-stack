from __future__ import annotations
from knx_stack import Octect, Msg
from knx_stack.definition.cemi import MessageCode
from knx_stack.encode.usb_hid import emi_id
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def encode(state: knx_stack.State, msg: knx_stack.Msg) -> knx_stack.Msg:
    """Encode a cEMI L_Data indication into raw message bytes.

    Prepends the L_Data.ind message code and an additional-info length of zero,
    then delegates to the USB HID EMI identifier encoder.
    """
    message_code = Octect(value=MessageCode.L_Data_ind)
    additional_info_length = Octect(value=0)
    new_msg = Msg([message_code, additional_info_length] + msg)
    final_msg = emi_id.encode(state, new_msg)
    return final_msg
