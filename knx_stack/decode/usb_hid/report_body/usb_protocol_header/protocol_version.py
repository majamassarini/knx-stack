from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.definition.usb_hid import KNX_USB_TRANSFER_PROTOCOL
from knx_stack.decode.usb_hid.report_body.usb_protocol_header import (
    header_length,
)

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    (head, body) = msg.octect()
    result: Iterable[NamedTuple] = []
    if head.value == KNX_USB_TRANSFER_PROTOCOL:
        result = header_length.decode(state, body)
    return result
