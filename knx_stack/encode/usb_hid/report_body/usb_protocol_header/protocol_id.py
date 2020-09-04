from knx_stack import Octect, Msg
from knx_stack.definition.usb_hid import ProtocolId
from knx_stack.encode.usb_hid.report_body.usb_protocol_header import body_length


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    protocol_id = Octect(value=ProtocolId.KNXTunnel)
    new_msg = Msg([protocol_id] + msg)
    final_msg = body_length.encode(state, new_msg)
    return final_msg
