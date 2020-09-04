from knx_stack import Octect, Msg
from knx_stack.cemi import MessageCode
from knx_stack.send.usb_hid import emi_id


def send(state, msg):
    message_code = Octect(value=MessageCode.L_Data_ind)
    additional_info_length = Octect(value=0)
    new_msg = Msg([message_code, additional_info_length] + msg)
    (final_state, final_msg) = emi_id.send(state, new_msg)
    return final_state, final_msg
