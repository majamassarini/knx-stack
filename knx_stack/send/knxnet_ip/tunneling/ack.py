import logging
from collections import namedtuple
from knx_stack import LOGGER_NAME
from knx_stack.msg import Short
from knx_stack.knxnet_ip import Msg as NetMsg, Services, HEADER_SIZE_10
from knx_stack.send.knxnet_ip import header
from knx_stack.send.knxnet_ip.tunneling import connection_header

Msg = namedtuple('TunnelingAck', ['sequence_counter', 'status'])


def send(state, msg):
    """
    >>> import knx_stack
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, None, None)
    >>> (final_state, final_msg) = send(state, Msg(sequence_counter=1, status=knx_stack.knxnet_ip.ErrorCodes.E_NO_ERROR))
    >>> final_msg
    06100421000A04000000
    """
    new_msg = NetMsg(Short(value=Services.TUNNELING_ACK.value).octects)
    new_msg += NetMsg(Short(value=connection_header.CONNECTION_HEADER_LEN + HEADER_SIZE_10).octects)
    new_msg += connection_header.create(state, status=msg.status, sequence_counter=state.sequence_counter_remote)
    logging.getLogger(LOGGER_NAME).info("knxnet_ip.tunneling.send.ack with sequence counter={}".format(state.sequence_counter_remote))
    if msg.sequence_counter == state.sequence_counter_remote:
        state.sequence_counter_remote += 1
    (final_state, final_msg) = header.send(state, new_msg)
    return final_state, final_msg
