from knx_stack.layer import AddressType
from knx_stack.receive.layer import network


def receive(state, msg):
    (data, new_state) = (None, state)
    if state.ldata.address_type == AddressType.individual:
        (data, new_state) = network.n_data_individual.ind.receive(state, msg)
    elif state.ldata.address_type == AddressType.group and state.ldata.destination != 0:
        (data, new_state) = network.n_data_group.ind.receive(state, msg)
    elif state.ldata.address_type == AddressType.group and state.ldata.destination == 0:
        (data, new_state) = network.n_data_broadcast.ind.receive(state, msg)
    return data, new_state
