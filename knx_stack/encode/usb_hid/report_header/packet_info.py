from knx_stack import Msg, Octect, Nibbles
from knx_stack.definition.usb_hid import PacketType
from knx_stack.encode.usb_hid.report_header import report_identifier


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    sequence_number = 1
    packet_type = PacketType.allInOnePacket
    packet_info = Octect(Nibbles(high=sequence_number, low=packet_type))
    data_length = Octect(value=len(msg))
    new_msg = Msg([packet_info, data_length] + msg)
    final_msg = report_identifier.encode(state, new_msg)
    return final_msg
