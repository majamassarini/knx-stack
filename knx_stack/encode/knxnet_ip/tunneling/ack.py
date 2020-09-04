import logging
from knx_stack.msg import Short
from knx_stack.definition.knxnet_ip import Msg as NetMsg, Services, HEADER_SIZE_10
from knx_stack.encode.knxnet_ip import header
from knx_stack.encode.knxnet_ip.tunneling import connection_header


def encode(state: 'knx_stack.State', msg: 'knx_stack.knxnet_ip.tunneling.ack.Msg') -> 'knx_stack.Msg':
    """
    >>> import knx_stack
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, None, None)
    >>> ack = knx_stack.knxnet_ip.tunneling.ack.Msg(sequence_counter=1,
    ...                                             status=knx_stack.knxnet_ip.ErrorCodes.E_NO_ERROR)
    >>> bus_msg = knx_stack.encode_msg(state, ack)
    >>> bus_msg
    06100421000A04000000
    """
    new_msg = NetMsg(Short(value=Services.TUNNELING_ACK.value).octects)
    new_msg += NetMsg(Short(value=connection_header.CONNECTION_HEADER_LEN + HEADER_SIZE_10).octects)
    new_msg += connection_header.create(state, status=msg.status, sequence_counter=state.sequence_counter_remote)
    logging.getLogger(__name__).info("knxnet_ip.tunneling.encode.ack with sequence counter={}".format(state.sequence_counter_remote))
    if msg.sequence_counter == state.sequence_counter_remote:
        state.sequence_counter_remote += 1
    final_msg = header.encode(state, new_msg)
    return final_msg
