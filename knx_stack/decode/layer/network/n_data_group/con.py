from typing import Iterable, NamedTuple
from knx_stack.definition.layer import NSDU
from knx_stack.decode.layer.transport.t_data_group import con


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    if state.ldata.nsdu == NSDU.T_Data_Group_PDU:
        return con.decode(state, msg)

