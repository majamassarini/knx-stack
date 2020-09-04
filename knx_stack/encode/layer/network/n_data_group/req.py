from knx_stack.encode.layer.link import l_data
from knx_stack.encode.layer.network.n_data_group.encode import nl_encode


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    new_msg = nl_encode(state, msg)
    final_msg = l_data.req.encode(state, new_msg)
    return final_msg
