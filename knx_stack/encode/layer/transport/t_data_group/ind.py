from knx_stack.encode.layer.network.n_data_group import ind
from knx_stack.encode.layer.transport.t_data_group.encode import tl_encode


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    new_msg = tl_encode(state, msg)
    final_msg = ind.encode(state, new_msg)
    return final_msg
