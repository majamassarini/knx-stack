from knx_stack import Short, Octect, Msg
from knx_stack.send.layer.link import l_data


def send(state, msg):
    npdu_length = Octect(value=(len(msg) - 1))
    destination = Short(value=state.individual_address)
    new_msg = Msg([destination.MSB, destination.LSB, npdu_length] + msg)
    (final_state, final_msg) = l_data.req.send(state, new_msg)
    return final_state, final_msg