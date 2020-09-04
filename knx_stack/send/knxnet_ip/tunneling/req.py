import logging
from knx_stack import LOGGER_NAME
from knx_stack.msg import Short
from knx_stack.knxnet_ip import Msg as NetMsg, Services, HEADER_SIZE_10
from knx_stack.send.knxnet_ip import header
from knx_stack.send.knxnet_ip.tunneling import connection_header


def send(state, msg):
    """
    >>> import knx_stack
    >>> address_table = knx_stack.layer.AddressTable(0x1001, [], 255)
    >>> association_table = knx_stack.layer.AssociationTable(address_table, [])
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, association_table, None)
    >>> (_, t_connect) = knx_stack.send.layer.transport.t_connect.req.send(state, knx_stack.knxnet_ip.Msg([]))
    >>> (final_state, final_msg) = send(state, t_connect)
    >>> final_msg
    06100420001E040000000610042000140400000011009660000010010080
    """
    new_msg = NetMsg(Short(value=Services.TUNNELING_REQUEST.value).octects)
    new_msg += NetMsg(Short(value=connection_header.CONNECTION_HEADER_LEN + HEADER_SIZE_10 + len(msg)).octects)
    new_msg += connection_header.create(state, 0, sequence_counter=state.sequence_counter_local)
    new_msg += msg
    logging.getLogger(LOGGER_NAME).info("knxnet_ip.tunneling.send.req with sequence counter={}".format(state.sequence_counter_local))
    (final_state, final_msg) = header.send(state, new_msg)
    return final_state, final_msg
