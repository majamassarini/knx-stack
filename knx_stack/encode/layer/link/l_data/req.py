from knx_stack.encode.cemi.ldata import req
from knx_stack.encode.layer.link.l_data.encode import ll_encode


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    new_msg = ll_encode(state, msg)
    final_msg = req.encode(state, new_msg)
    return final_msg
