from knx_stack import Octect, Msg
from knx_stack.definition.cemi import MessageCode
from knx_stack.encode.usb_hid import emi_id


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    message_code = Octect(value=MessageCode.L_Data_ind)
    additional_info_length = Octect(value=0)
    new_msg = Msg([message_code, additional_info_length] + msg)
    final_msg = emi_id.encode(state, new_msg)
    return final_msg
