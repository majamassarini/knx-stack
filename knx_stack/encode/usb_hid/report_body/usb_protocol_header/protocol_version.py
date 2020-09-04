from knx_stack import Msg, Octect
from knx_stack.encode.usb_hid.report_header import packet_info


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    header_length = Octect(value=0)
    new_msg = Msg([header_length] + msg)
    final_msg = packet_info.encode(state, new_msg)
    return final_msg
