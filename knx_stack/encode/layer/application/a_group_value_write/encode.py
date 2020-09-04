from typing import Union
from knx_stack import Msg, Octect, Short, Long
from knx_stack.definition import layer
from knx_stack.datapointtypes import DPT


def al_encode(state: 'knx_stack.State',
              msg: Union['knx_stack.layer.application.a_group_value_write.req.Msg',
                         'knx_stack.layer.application.a_group_value_write.ind.Msg']) -> 'knx_stack.Msg':
    apci = 0x80
    state.asap = msg.asap
    state.apci = apci
    state.address_type = layer.AddressType.group
    dpt = state.get_dpt()
    ldata = layer.L_Data()
    new_msg = Msg([])
    if dpt.length == DPT.Length.LESS_THAN_A_BYTE:
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
    return new_msg
