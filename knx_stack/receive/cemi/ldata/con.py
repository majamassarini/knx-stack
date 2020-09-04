import knx_stack.state
from knx_stack import layer
from knx_stack.receive.layer.link import l_data


def receive(state, msg):
    (data, body) = layer.link.L_Data.make_from(msg)
    state.ldata = data
    return l_data.con.receive(state, body)
