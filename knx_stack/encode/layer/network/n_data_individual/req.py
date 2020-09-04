from knx_stack import Short, Octect, Msg
from knx_stack.encode.layer.link import l_data


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    npdu_length = Octect(value=(len(msg) - 1))
    destination = Short(value=state.individual_address.free_style)
    new_msg = Msg([destination.MSB, destination.LSB, npdu_length] + msg)
    final_msg = l_data.req.encode(state, new_msg)
    return final_msg
