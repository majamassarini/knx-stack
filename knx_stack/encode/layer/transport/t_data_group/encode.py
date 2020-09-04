from knx_stack import Msg, Octect
from knx_stack.definition import layer


def tl_encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    new_msg = msg
    if state.get_tsaps():
        ldata = layer.L_Data()
        ldata.nsdu = layer.NSDU.T_Data_Group_PDU
        ldata.apci = state.apci
        new_msg = Msg([Octect(value=ldata.tpci)] + msg)
    return new_msg
