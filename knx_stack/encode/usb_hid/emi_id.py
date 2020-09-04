from knx_stack import Msg
from knx_stack import Octect
from knx_stack.definition.cemi import EMIId
from knx_stack.encode.usb_hid.report_body.usb_protocol_header import protocol_id


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    emi_id = Octect(value=EMIId.commonEmi)
    emi_id_a = Octect(value=0)
    emi_id_b = Octect(value=0)
    new_msg = Msg([emi_id, emi_id_a, emi_id_b] + msg)
    final_msg = protocol_id.encode(state, new_msg)
    return final_msg
