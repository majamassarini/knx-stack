from knx_stack import Msg
from knx_stack import Octect
from knx_stack.cemi import EMIId
from knx_stack.send.usb_hid.report_body.usb_protocol_header import protocol_id


def send(state, msg):
    emi_id = Octect(value=EMIId.commonEmi)
    emi_id_a = Octect(value=0)
    emi_id_b = Octect(value=0)
    new_msg = Msg([emi_id, emi_id_a, emi_id_b] + msg)
    (final_state, final_msg) = protocol_id.send(state, new_msg)
    return final_state, final_msg
