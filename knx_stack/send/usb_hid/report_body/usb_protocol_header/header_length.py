from knx_stack.msg import Msg, Octect
from knx_stack.usb_hid import KNX_USB_TRANSFER_PROTOCOL_HEADER_LENGTH
from knx_stack.send.usb_hid.report_body.usb_protocol_header import protocol_version


def send(state, msg):
    header_length = Octect(value=KNX_USB_TRANSFER_PROTOCOL_HEADER_LENGTH)
    new_msg = Msg([header_length] + msg)
    (final_state, final_msg) = protocol_version.send(state, new_msg)
    return final_state, final_msg
