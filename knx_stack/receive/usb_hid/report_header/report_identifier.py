from knx_stack.usb_hid import KNX_DATA_EXCHANGE
from knx_stack.receive.usb_hid.report_header import packet_info


def receive(state, msg):
    (head, body) = msg.octect()
    (data, new_state) = (None, state)
    if head.value == KNX_DATA_EXCHANGE:
        (data, new_state) = packet_info.receive(state, body)
    return data, new_state
