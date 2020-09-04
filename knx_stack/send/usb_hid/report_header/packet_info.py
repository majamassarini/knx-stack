from knx_stack import Msg, Octect, Nibbles
from knx_stack.usb_hid import PacketType
from knx_stack.send.usb_hid.report_header import report_identifier


def send(state, msg):
    sequence_number = 1
    packet_type = PacketType.allInOnePacket
    packet_info = Octect(Nibbles(high=sequence_number, low=packet_type))
    data_length = Octect(value=len(msg))
    new_msg = Msg([packet_info, data_length] + msg)
    (final_state, final_msg) = report_identifier.send(state, new_msg)
    return final_state, final_msg
