from knx_stack.send.layer.link import l_data
from knx_stack.send.layer.network.n_data_group.send import nl_send


def send(state, msg):
    (new_state, new_msg) = nl_send(state, msg)
    (final_state, final_msg) = l_data.req.send(new_state, new_msg)
    return final_state, final_msg
