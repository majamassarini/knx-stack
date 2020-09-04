from knx_stack.layer import NSDU
from knx_stack.receive.layer.transport.t_data_group import con


def receive(state, msg):
    if state.ldata.nsdu == NSDU.T_Data_Group_PDU:
        return con.receive(state, msg)

