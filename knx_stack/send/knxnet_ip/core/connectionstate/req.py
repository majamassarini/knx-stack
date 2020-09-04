import socket

from collections import namedtuple

from knx_stack import Octect, Short
from knx_stack.knxnet_ip import Msg as NetMsg, Services, HEADER_SIZE_10
from knx_stack.send.knxnet_ip import header
from knx_stack.send.knxnet_ip.core import hpai

Msg = namedtuple('ConnectionstateRequest', ['addr_control_endpoint', 'port_control_endpoint'])


def send(state, msg):
    """
    >>> import knx_stack
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, None, None)
    >>> search_request = Msg(addr_control_endpoint='127.0.0.1', port_control_endpoint=1234)
    >>> (final_state, final_msg) = send(state, search_request)
    >>> final_msg
    061002070010000008017F00000104D2
    """
    ip_control_endpoint = socket.inet_aton(msg.addr_control_endpoint)
    hpai_control_endpoint = hpai.create(ip_control_endpoint, msg.port_control_endpoint)
    new_msg = NetMsg(Short(value=Services.CONNECTIONSTATE_REQUEST.value).octects)
    new_msg += NetMsg(Short(value=(2 + hpai.LENGTH + HEADER_SIZE_10)).octects)
    new_msg += NetMsg([Octect(value=state.communication_channel_id), Octect(value=0)])
    new_msg += hpai_control_endpoint
    (final_state, final_msg) = header.send(state, new_msg)
    return final_state, final_msg
