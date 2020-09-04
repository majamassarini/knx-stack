import logging

from knx_stack.receive.layer import application


def receive(state, msg):
    tsap = state.get_tsap()
    data = None
    if tsap:
        if state.ldata.apci == 0:
            (data, state) = application.a_group_value_read.con.receive(state, msg)
        elif (state.ldata.apci - state.ldata.data) == 0x40:
            (data, state) = application.a_group_value_response.con.receive(state, msg)
        elif (state.ldata.apci - state.ldata.data) == 0x80:
            (data, state) = application.a_group_value_write.con.receive(state, msg)
    else:
        logger = logging.getLogger( '%s' % __name__)
        logger.info("discarded msg %s with data %s" % (state.ldata, msg))
    return data, state
