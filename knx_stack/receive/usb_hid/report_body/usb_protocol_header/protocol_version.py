from knx_stack.usb_hid import KNX_USB_TRANSFER_PROTOCOL
from knx_stack.receive.usb_hid.report_body.usb_protocol_header import header_length


def receive(state, msg):
    (head, body) = msg.octect()
    (data, new_state) = (None, state)
    if head.value == KNX_USB_TRANSFER_PROTOCOL:
        (data, new_state) = header_length.receive(state, body)

    return data, new_state
