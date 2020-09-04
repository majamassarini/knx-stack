from knx_stack.layer import NSDU
from knx_stack.receive.layer import transport


def receive(state, msg):
    (data, new_state) = (None, state)
    if state.ldata.nsdu == NSDU.T_Data_Individual_PDU:
         (data, new_state) = transport.t_data_individual.con.receive(state, msg)
    elif state.ldata.nsdu == NSDU.T_Data_Tag_Group_PDU:
        print("NSDU.T_Data_Tag_Group_PDU")
    elif state.ldata.nsdu == NSDU.T_Connect_PDU:
         (data, new_state) = transport.t_connect.con.receive(state, msg)
    elif state.ldata.nsdu == NSDU.T_Disconnect_PDU:
         (data, new_state) = transport.t_disconnect.con.receive(state, msg)
    elif state.ldata.nsdu == NSDU.T_Data_Connected_PDU:
         (data, new_state) = transport.t_data_connected.con.receive(state, msg)
    return data, new_state