from knx_stack import Msg, Octect
from knx_stack.usb_hid import KNX_DATA_EXCHANGE


def send(state, msg):
    packet_info = Octect(value=KNX_DATA_EXCHANGE)
    final_msg = Msg([packet_info] + msg)
    return state, final_msg
