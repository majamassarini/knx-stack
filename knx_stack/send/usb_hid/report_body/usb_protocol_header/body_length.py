from knx_stack import Msg, Short
from knx_stack.send.usb_hid.report_body.usb_protocol_header import header_length


def send(state, msg):
    length = len(msg) - 4
    body_length = Short(value=length)
    new_msg = Msg([body_length.MSB, body_length.LSB] + msg)
    (final_state, final_msg) = header_length.send(state, new_msg)
    return final_state, final_msg
