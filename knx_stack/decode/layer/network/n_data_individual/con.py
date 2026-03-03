from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.definition.layer import NSDU
from knx_stack.decode.layer import transport

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    """Decode an N_Data_Individual confirmation at the network layer from raw message bytes.

    Inspects the NSDU field in the state and dispatches to the appropriate
    transport layer confirmation decoder (individual data, connect, disconnect,
    or data connected).
    """
    result: Iterable[NamedTuple] = []
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
