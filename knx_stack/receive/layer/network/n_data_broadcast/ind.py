from knx_stack.receive.layer.transport.t_data_broadcast import ind


def receive(state, msg):
    return ind.receive(state, msg)
