from knx_stack import Msg, Octect
from knx_stack.definition.usb_hid import KNX_DATA_EXCHANGE


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    packet_info = Octect(value=KNX_DATA_EXCHANGE)
    final_msg = Msg([packet_info] + msg)
    return final_msg
