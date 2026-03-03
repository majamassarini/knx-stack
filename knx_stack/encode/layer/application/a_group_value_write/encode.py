from __future__ import annotations
from typing import TYPE_CHECKING, Union
from knx_stack import Msg, Octect, Short, Long
from knx_stack.definition import layer
from knx_stack.datapointtypes import DPT

if TYPE_CHECKING:
    import knx_stack


def al_encode(
    state: knx_stack.State,
    msg: Union[
        knx_stack.layer.application.a_group_value_write.req.Msg,
        knx_stack.layer.application.a_group_value_write.ind.Msg,
    ],
) -> knx_stack.Msg:
    """Encode an A_GroupValue_Write PDU at the application layer into raw message bytes.

    Serialises the DPT value and APCI byte for a group value write service,
    handling sub-byte, one-byte, two-byte, and four-byte DPT sizes.
    """
    apci = 0x80
    state.asap = msg.asap
    state.apci = apci
    state.address_type = layer.AddressType.group
    dpt = state.get_dpt()
    ldata = layer.L_Data()
    new_msg = Msg([])
    if dpt.length == DPT.Length.LESS_THAN_A_BYTE:
        ldata.apci = apci  # type: ignore[misc]
        ldata.data = msg.dpt.value  # type: ignore[attr-defined]
        new_msg = Msg([Octect(value=ldata.apci)])
    else:
        ldata.apci = apci  # type: ignore[misc]
        ldata.data = 0
        if dpt.value.size == 1:  # type: ignore[attr-defined]
            new_msg = Msg(
                [Octect(value=ldata.apci), Octect(value=msg.dpt.value)]  # type: ignore[attr-defined]
            )
        elif dpt.value.size == 2:  # type: ignore[attr-defined]
            short = Short(value=msg.dpt.value)  # type: ignore[attr-defined]
            new_msg = Msg([Octect(value=ldata.apci), short.MSB, short.LSB])
        elif dpt.value.size == 4:  # type: ignore[attr-defined]
            long = Long(value=msg.dpt.value)  # type: ignore[attr-defined]
            new_msg = Msg(
                [Octect(value=ldata.apci), long.B4, long.B3, long.B2, long.B1]
            )
    return new_msg
