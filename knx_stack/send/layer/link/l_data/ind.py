from knx_stack.send.cemi.ldata import ind
from knx_stack.send.layer.link.l_data.send import ll_send


def send(state, msg):
    (new_state, new_msg) = ll_send(state, msg)
    (final_state, final_msg) = ind.send(new_state, new_msg)
    return final_state, final_msg
