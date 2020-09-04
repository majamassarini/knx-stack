import socket

from knx_stack import Octect, Short
from knx_stack.definition.knxnet_ip import Msg as NetMsg, Services, HEADER_SIZE_10
from knx_stack.encode.knxnet_ip import header
from knx_stack.encode.knxnet_ip.core import hpai


def encode(state: 'knx_stack.State', msg: 'knx_stack.knxnet_ip.core.connectionstate.req.Msg') -> 'knx_stack.Msg':
    """
    >>> import knx_stack
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, None, None)
    >>> search_request = knx_stack.knxnet_ip.core.connectionstate.req.Msg(addr_control_endpoint='127.0.0.1',
    ...                                                                   port_control_endpoint=1234)
    >>> bus_msg = knx_stack.encode_msg(state, search_request)
    >>> bus_msg
    061002070010000008017F00000104D2
    """
    ip_control_endpoint = socket.inet_aton(msg.addr_control_endpoint)
    hpai_control_endpoint = hpai.create(ip_control_endpoint, msg.port_control_endpoint)
    new_msg = NetMsg(Short(value=Services.CONNECTIONSTATE_REQUEST.value).octects)
    new_msg += NetMsg(Short(value=(2 + hpai.LENGTH + HEADER_SIZE_10)).octects)
    new_msg += NetMsg([Octect(value=state.communication_channel_id), Octect(value=0)])
    new_msg += hpai_control_endpoint
    final_msg = header.encode(state, new_msg)
    return final_msg
