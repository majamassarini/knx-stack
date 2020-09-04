import logging
from typing import Iterable, NamedTuple
from knx_stack.decode.layer import application


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    logger = logging.getLogger(__name__)
    tsap = state.get_tsap()
    result = []
    if tsap == 0:
        if state.ldata.apci == 0x3D5:
            result = application.a_property_value_read.con.decode(state, msg)
        elif state.ldata.apci == 0x3D6:
            result = application.a_property_value_response.con.decode(state, msg)
        elif state.ldata.apci == 0x3D7:
            result = application.a_property_value_write.con.decode(state, msg)
        s = "received msg {} {}".format(msg, state.ldata)
        try:
            logger.debug("{} {} asaps {}".format(s, result[0].dpt, [m.asap for m in result]))
        except (AttributeError, IndexError) as e:
            logger.debug("{} {}".format(s, result))
    else:
        logger.info("discarded msg {} {}".format(msg, state.ldata))
    return result
