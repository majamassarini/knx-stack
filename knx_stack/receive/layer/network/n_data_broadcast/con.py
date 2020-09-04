from knx_stack.receive.layer.transport.t_data_broadcast import con


def receive(state, msg):
    return con.receive(state, msg)
