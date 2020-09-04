import logging
from knx_stack.msg import Short
from knx_stack.definition.knxnet_ip import Msg as NetMsg, Services, HEADER_SIZE_10
from knx_stack.encode.knxnet_ip import header
from knx_stack.encode.knxnet_ip.tunneling import connection_header


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    """
    >>> import knx_stack
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(0x1001), [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, [])
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, association_table, None)
    >>> t_connect = knx_stack.encode.layer.transport.t_connect.req.encode(state, knx_stack.knxnet_ip.Msg([]))
    >>> bus_msg = knx_stack.encode.knxnet_ip.tunneling.req.encode(state, t_connect)
    >>> bus_msg
    06100420001E040000000610042000140400000011009660000010010080
    """
    new_msg = NetMsg(Short(value=Services.TUNNELING_REQUEST.value).octects)
    new_msg += NetMsg(Short(value=connection_header.CONNECTION_HEADER_LEN + HEADER_SIZE_10 + len(msg)).octects)
    new_msg += connection_header.create(state, 0, sequence_counter=state.sequence_counter_local)
    new_msg += msg
    logging.getLogger(__name__).debug("knxnet_ip.tunneling.encode.req with sequence counter={}".format(state.sequence_counter_local))
    final_msg = header.encode(state, new_msg)
    return final_msg
