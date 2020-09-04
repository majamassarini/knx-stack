from typing import Iterable, NamedTuple
from knx_stack.definition.usb_hid import KNX_USB_TRANSFER_PROTOCOL_HEADER_LENGTH
from knx_stack.decode.usb_hid.report_body.usb_protocol_header import body_length


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    (head, body) = msg.octect()
    result = []
    if head.value == KNX_USB_TRANSFER_PROTOCOL_HEADER_LENGTH:
        result = body_length.decode(state, body)
    return result
