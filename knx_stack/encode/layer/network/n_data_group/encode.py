from knx_stack import Short, Octect, Msg


def nl_encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    new_msg = msg
    for address in state.get_addresses():
        npdu_length = Octect(value=(len(msg) - 1))
        destination = Short(value=address.free_style)
        new_msg = Msg([destination.MSB, destination.LSB, npdu_length] + msg)
        break  # just the first address is the encodeing address...
    return new_msg
