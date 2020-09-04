from knx_stack import Msg, Octect
from knx_stack.definition import layer
from knx_stack.encode.layer.network.n_data_individual import req


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    final_msg = msg
    ldata = layer.L_Data()
    if state.address_type == layer.AddressType.individual:
        ldata.nsdu = layer.NSDU.T_Data_Individual_PDU
        ldata.apci = state.apci
        new_msg = Msg([Octect(value=ldata.tpci)] + msg)
        final_msg = req.encode(state, new_msg)
    return final_msg
