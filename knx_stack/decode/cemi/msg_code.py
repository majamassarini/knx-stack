from typing import Iterable, NamedTuple
from knx_stack import Msg
from knx_stack.definition.cemi import MessageCode
from knx_stack.decode.cemi.ldata import con, ind


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    result = []
    (message_code, body) = msg.octect()
    (additional_info_length, body) = body.octect()
    body = Msg(body[additional_info_length.value:])
    
    if message_code.value == MessageCode.L_Data_ind:
        result = ind.decode(state, body)
    elif message_code.value == MessageCode.L_Data_con:
        result = con.decode(state, body)

    return result
