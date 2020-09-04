import logging
from knx_stack import LOGGER_NAME
from knx_stack.knxnet_ip import HEADER_SIZE_10, KNXNETIP_VERSION_10, Services
from knx_stack.receive.knxnet_ip import core, tunneling


def receive(state, msg):
    (header, body) = msg.octect()
    (version, body) = body.octect()
    (service, body) = body.short()
    data, new_state = (None, state)
    if header.value == HEADER_SIZE_10 and version.value == KNXNETIP_VERSION_10:
        if service.value == Services.SEARCH_RESPONSE:
            (data, new_state) = core.search.res.receive(state, body)
        elif service.value == Services.DISCONNECT_RESPONSE:
            (data, new_state) = core.disconnect.res.receive(state, body)
        elif service.value == Services.CONNECT_RESPONSE:
            (data, new_state) = core.connect.res.receive(state, body)
        elif service.value == Services.CONNECTIONSTATE_RESPONSE:
            (data, new_state) = core.connectionstate.res.receive(state, body)
        elif service.value == Services.TUNNELING_REQUEST:
            (data, new_state) = tunneling.req.receive(state, body)
        elif service.value == Services.TUNNELING_ACK:
            (data, new_state) = tunneling.ack.receive(state, body)
        else:
            logging.getLogger(LOGGER_NAME).error("Unknown knxnet_ip service value %d" % service.value)
    return data, new_state
