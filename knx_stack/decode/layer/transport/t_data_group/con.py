from __future__ import annotations
import logging
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.decode.layer import application

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    logger = logging.getLogger(__name__)
    tsap = state.get_tsap()
    result: Iterable[NamedTuple] = []
    if tsap:
        if state.ldata.apci == 0:
            result = application.a_group_value_read.con.decode(state, msg)
        elif (state.ldata.apci - state.ldata.data) == 0x40:
            result = application.a_group_value_response.con.decode(state, msg)
        elif (state.ldata.apci - state.ldata.data) == 0x80:
            result = application.a_group_value_write.con.decode(state, msg)
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
