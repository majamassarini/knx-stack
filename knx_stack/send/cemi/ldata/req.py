from knx_stack import Medium, Octect, Msg
from knx_stack.cemi import MessageCode
from knx_stack.send.knxnet_ip import tunneling
from knx_stack.send.usb_hid import emi_id


def send(state, msg):
    message_code = Octect(value=MessageCode.L_Data_req)
    additional_info_length = Octect(value=0)
    new_msg = Msg([message_code, additional_info_length] + msg)
    if state.medium == Medium.usb_hid:
        (final_state, final_msg) = emi_id.send(state, new_msg)
    elif state.medium == Medium.knxnet_ip:
        (final_state, final_msg) = tunneling.req.send(state, new_msg)
    else:
        (final_state, final_msg) = (state, new_msg)
    return final_state, final_msg
