import logging
from knx_stack.receive.layer import application


def receive(state, msg):
    tsap = state.get_tsap()
    (data, new_state) = (None, state)
    if tsap == 0:
        if state.ldata.apci == 0x3D5:
            (data, new_state) = application.a_property_value_read.con.receive(state, msg)
        elif state.ldata.apci == 0x3D6:
            (data, new_state) = application.a_property_value_response.con.receive(state, msg)
        elif state.ldata.apci == 0x3D7:
            (data, new_state) = application.a_property_value_write.con.receive(state, msg)
    else:
        logger = logging.getLogger( '%s' % __name__)
        logger.info("discarded msg %s with data %s" % (state.ldata, msg))
        new_state = state
    return data, new_state
