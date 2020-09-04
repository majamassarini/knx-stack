from knx_stack import Msg, Octect
from knx_stack.send.usb_hid.report_header import packet_info


def send(state, msg):
    header_length = Octect(value=0)
    new_msg = Msg([header_length] + msg)
    (final_state, final_msg) = packet_info.send(state, new_msg)
    return final_state, final_msg
