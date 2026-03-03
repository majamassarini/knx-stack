from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack import Msg
from knx_stack.decode.usb_hid.report_body.usb_protocol_header import (
    protocol_id,
)

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    """Decode the USB HID USB protocol header body length field from raw message bytes.

    Reads the two-byte body length, trims the message to the indicated length,
    and delegates to the protocol_id decoder.
    """
    (head, body) = msg.short()
    body_length = head.value
    the_other_header_octects = 4
    return protocol_id.decode(
        state, Msg(body[0 : body_length + the_other_header_octects])
    )
