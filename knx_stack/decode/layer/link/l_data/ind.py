from typing import Iterable, NamedTuple
from knx_stack.definition.layer import AddressType
from knx_stack.decode.layer import network


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    result = []
    if state.ldata.address_type == AddressType.individual:
        result = network.n_data_individual.ind.decode(state, msg)
    elif state.ldata.address_type == AddressType.group and state.ldata.destination != 0:
        result = network.n_data_group.ind.decode(state, msg)
    elif state.ldata.address_type == AddressType.group and state.ldata.destination == 0:
        result = network.n_data_broadcast.ind.decode(state, msg)
    return result
