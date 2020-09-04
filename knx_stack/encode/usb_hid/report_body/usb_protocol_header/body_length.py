from knx_stack import Msg, Short
from knx_stack.encode.usb_hid.report_body.usb_protocol_header import header_length


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    length = len(msg) - 4
    body_length = Short(value=length)
    new_msg = Msg([body_length.MSB, body_length.LSB] + msg)
    final_msg = header_length.encode(state, new_msg)
    return final_msg
