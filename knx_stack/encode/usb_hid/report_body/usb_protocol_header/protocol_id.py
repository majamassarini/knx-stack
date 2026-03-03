from __future__ import annotations
from knx_stack import Octect, Msg
from knx_stack.definition.usb_hid import ProtocolId
from knx_stack.encode.usb_hid.report_body.usb_protocol_header import (
    body_length,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


def encode(state: knx_stack.State, msg: knx_stack.Msg) -> knx_stack.Msg:
    """Encode the USB HID USB protocol header protocol identifier field into raw message bytes.

    Prepends the KNX tunnel protocol ID byte to the message, then delegates
    to the body_length encoder.
    """
    protocol_id = Octect(value=ProtocolId.KNXTunnel)
    new_msg = Msg([protocol_id] + msg)
    final_msg = body_length.encode(state, new_msg)
    return final_msg
