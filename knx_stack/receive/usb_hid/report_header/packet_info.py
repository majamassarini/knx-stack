from knx_stack import Msg
from knx_stack.usb_hid import PacketType
from knx_stack.receive.usb_hid.report_body.usb_protocol_header import protocol_version


def receive(state, msg):
    (data, new_state) = (None, state)
    (packet_info_byte, body) = msg.octect()
    packet_type = packet_info_byte.nibble.low

    if packet_type == PacketType.allInOnePacket:
        (data_length, body) = body.octect()
        (data, new_state) = protocol_version.receive(state, Msg(body[0:data_length.value]))
    else:
        _sequence_number = packet_info_byte.nibble.high

    return data, new_state
