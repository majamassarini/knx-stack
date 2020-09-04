from knx_stack import Msg, Octect, layer
from knx_stack.send.layer.network.n_data_individual import req


def send(state, msg):
    (final_state, final_msg) = (state, msg)
    ldata = layer.L_Data()
    if state.address_type == layer.AddressType.individual:
        ldata.nsdu = layer.NSDU.T_Data_Individual_PDU
        ldata.apci = state.apci
        new_msg = Msg([Octect(value=ldata.tpci)] + msg)
        (final_state, final_msg) = req.send(state, new_msg)
    return final_state, final_msg
