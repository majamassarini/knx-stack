from typing import Iterable, NamedTuple
from knx_stack.definition.layer import NSDU
from knx_stack.decode.layer import transport


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    result = []
    if state.ldata.nsdu == NSDU.T_Data_Individual_PDU:
        result = transport.t_data_individual.con.decode(state, msg)
    elif state.ldata.nsdu == NSDU.T_Data_Tag_Group_PDU:
        result = []  # @todo not yet implemented
    elif state.ldata.nsdu == NSDU.T_Connect_PDU:
        result = transport.t_connect.con.decode(state, msg)
    elif state.ldata.nsdu == NSDU.T_Disconnect_PDU:
        result = transport.t_disconnect.con.decode(state, msg)
    elif state.ldata.nsdu == NSDU.T_Data_Connected_PDU:
        result = transport.t_data_connected.con.decode(state, msg)
    return result
