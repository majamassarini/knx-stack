from knx_stack import Msg, Octect, Short, Long, layer
from knx_stack.datapointtypes import Description


def al_send(state, msg):
    apci = 0x80
    state.asap = msg.asap
    state.apci = apci
    state.address_type = layer.AddressType.group
    new_msg = Msg([])
    dpt = state.get_dpt()
    ldata = layer.L_Data()
    if dpt.length == Description.Length.LESS_THAN_A_BYTE:
        ldata.apci = apci
        ldata.data = msg.dpt.value
        new_msg = Msg([Octect(value=ldata.apci)])
    else:
        ldata.apci = apci
        ldata.data = 0
        if dpt.value.size == 1:
            new_msg = Msg([Octect(value=ldata.apci), Octect(value=msg.dpt.value)])
        elif dpt.value.size == 2:
            short = Short(value=msg.dpt.value)
            new_msg = Msg([Octect(value=ldata.apci), short.MSB, short.LSB])
        elif dpt.value.size == 4:
            long = Long(value=msg.dpt.value)
            new_msg = Msg([Octect(value=ldata.apci), long.B4, long.B3, long.B2, long.B1])
    return state, new_msg
