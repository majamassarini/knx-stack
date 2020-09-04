from knx_stack.layer import NSDU
from knx_stack.receive.layer.transport.t_data_group import ind


def receive(state, msg):
    if state.ldata.nsdu == NSDU.T_Data_Group_PDU:
        return ind.receive(state, msg)

