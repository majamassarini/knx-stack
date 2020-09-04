from knx_stack import Octect, Msg, Short
from knx_stack.definition.layer import L_Data


def ll_encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    ldata = L_Data()
    ldata.address_type = state.address_type
    cntrl1 = Octect(value=ldata._cntrl1.value)
    cntrl2 = Octect(value=ldata._cntrl2.value)
    source = Short(value=0x0000)
    new_msg = Msg([cntrl1, cntrl2, source.MSB, source.LSB] + msg)
    return new_msg
