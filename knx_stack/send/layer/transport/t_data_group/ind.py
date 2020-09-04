from knx_stack.send.layer.network.n_data_group import ind
from knx_stack.send.layer.transport.t_data_group.send import tl_send


def send(state, msg):
    (new_state, new_msg) = tl_send(state, msg)
    (final_state, final_msg) = ind.send(new_state, new_msg)
    return final_state, final_msg
