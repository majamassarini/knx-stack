from knx_stack import Msg, Octect, layer


def tl_send(state, msg):
    new_msg = msg
    if state.get_tsaps():
        ldata = layer.L_Data()
        ldata.nsdu = layer.NSDU.T_Data_Group_PDU
        ldata.apci = state.apci
        new_msg = Msg([Octect(value=ldata.tpci)] + msg)
    return state, new_msg
