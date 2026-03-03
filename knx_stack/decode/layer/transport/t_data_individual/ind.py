from __future__ import annotations
import logging
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.decode.layer import application

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    """Decode a T_Data_Individual indication at the transport layer from raw message bytes.

    Checks that the source address matches the association table's individual
    address, then dispatches to the appropriate application layer property value
    indication decoder based on the APCI value.
    """
    logger = logging.getLogger(__name__)
    result: Iterable[NamedTuple] = []
    if (
        state.ldata.source
        == state.association_table.individual_address.free_style
    ):
        if state.ldata.apci == 0x3D5:
            result = application.a_property_value_read.ind.decode(state, msg)
        elif state.ldata.apci == 0x3D6:
            result = application.a_property_value_response.ind.decode(
                state, msg
            )
        elif state.ldata.apci == 0x3D7:
            result = application.a_property_value_write.ind.decode(state, msg)
        s = "received msg {} {}".format(msg, state.ldata)
        try:
            logger.debug(
                "{} {} asaps {}".format(
                    s, result[0].dpt, [m.asap for m in result]  # type: ignore[index,attr-defined]
                )
            )
        except (AttributeError, IndexError):
            logger.debug("{} {}".format(s, result))
    else:
        logger.info("discarded msg {} {}".format(msg, state.ldata))
    return result
