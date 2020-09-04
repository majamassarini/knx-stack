from knx_stack import Msg
from knx_stack.receive.usb_hid.report_body.usb_protocol_header import protocol_id


def receive(state, msg):
    (head, body) = msg.short()
    body_length = head.value
    the_other_header_octects = 4
    return protocol_id.receive(state, Msg(body[0:body_length + the_other_header_octects]))
