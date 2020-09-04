from knx_stack import Short, Octect, Msg


def nl_send(state, msg):
    new_msg = msg
    for address in state.get_addresses():
        npdu_length = Octect(value=(len(msg) - 1))
        destination = Short(value=address)
        new_msg = Msg([destination.MSB, destination.LSB, npdu_length] + msg)
        break  # just the first address is the sending address...
    return state, new_msg
