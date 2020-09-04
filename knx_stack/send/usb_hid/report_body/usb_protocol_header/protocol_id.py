from knx_stack import Octect, Msg
from knx_stack.usb_hid import ProtocolId
from knx_stack.send.usb_hid.report_body.usb_protocol_header import body_length


def send(state, msg):
    protocol_id = Octect(value=ProtocolId.KNXTunnel)
    new_msg = Msg([protocol_id] + msg)
    (final_state, final_msg) = body_length.send(state, new_msg)
    return final_state, final_msg
