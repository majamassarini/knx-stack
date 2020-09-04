from typing import Iterable, NamedTuple
from knx_stack import Msg
from knx_stack.decode.usb_hid.report_body.usb_protocol_header import protocol_id


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    (head, body) = msg.short()
    body_length = head.value
    the_other_header_octects = 4
    return protocol_id.decode(state, Msg(body[0:body_length + the_other_header_octects]))
