import logging
from knx_stack.receive.layer import application


def receive(state, msg):
    (data, new_state) = (None, state)
    if state.ldata.source == state.association_table.individual_address:
        if state.ldata.apci == 0x3D5:
            (data, new_state) = application.a_property_value_read.ind.receive(state, msg)
        elif state.ldata.apci == 0x3D6:
            (data, new_state) = application.a_property_value_response.ind.receive(state, msg)
        elif state.ldata.apci == 0x3D7:
            (data, new_state) = application.a_property_value_write.ind.receive(state, msg)
    else:
        logger = logging.getLogger( '%s' % __name__)
        logger.info("discarded msg %s with data %s" % (state.ldata, msg))
        new_state = state
    return data, new_state
