from knx_stack.usb_hid import KNX_USB_TRANSFER_PROTOCOL_HEADER_LENGTH
from knx_stack.receive.usb_hid.report_body.usb_protocol_header import body_length


def receive(state, msg):
    (head, body) = msg.octect()
    (data, new_state) = (None, state)
    if head.value == KNX_USB_TRANSFER_PROTOCOL_HEADER_LENGTH:
        (data, new_state) = body_length.receive(state, body)
    return data, new_state
