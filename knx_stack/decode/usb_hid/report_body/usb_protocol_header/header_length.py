from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.definition.usb_hid import (
    KNX_USB_TRANSFER_PROTOCOL_HEADER_LENGTH,
)
from knx_stack.decode.usb_hid.report_body.usb_protocol_header import (
    body_length,
)

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    """Decode the USB HID USB protocol header length field from raw message bytes.

    Validates the header length byte and, if it matches the expected KNX USB
    transfer protocol header length, delegates to the body_length decoder.
    """
    (head, body) = msg.octect()
    result: Iterable[NamedTuple] = []
    if head.value == KNX_USB_TRANSFER_PROTOCOL_HEADER_LENGTH:
        result = body_length.decode(state, body)
    return result
