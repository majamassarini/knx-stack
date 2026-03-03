from __future__ import annotations
from knx_stack.msg import Msg, Octect
from knx_stack.definition.usb_hid import (
    KNX_USB_TRANSFER_PROTOCOL_HEADER_LENGTH,
)
from knx_stack.encode.usb_hid.report_body.usb_protocol_header import (
    protocol_version,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def encode(state: knx_stack.State, msg: knx_stack.Msg) -> knx_stack.Msg:
    """Encode the USB HID USB protocol header length field into raw message bytes.

    Prepends the fixed KNX USB transfer protocol header length byte to the
    message, then delegates to the protocol_version encoder.
    """
    header_length = Octect(value=KNX_USB_TRANSFER_PROTOCOL_HEADER_LENGTH)
    new_msg = Msg([header_length] + msg)
    final_msg = protocol_version.encode(state, new_msg)
    return final_msg
