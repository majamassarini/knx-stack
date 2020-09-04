from knx_stack import Msg
from knx_stack.cemi import MessageCode
from knx_stack.receive.cemi.ldata import con, ind


def receive(state, msg):
    (data, new_state) = (None, state)
    (message_code, body) = msg.octect()
    (additional_info_length, body) = body.octect()
    body = Msg(body[additional_info_length.value:])
    
    if message_code.value == MessageCode.L_Data_ind:
        (data, new_state) = ind.receive(state, body)
    elif message_code.value == MessageCode.L_Data_con:
        (data, new_state) = con.receive(state, body)

    return data, new_state