import socket

from collections import namedtuple

from knx_stack import Octect, Short
from knx_stack.knxnet_ip import Msg as NetMsg, Services, ConnectionTypes, HEADER_SIZE_10
from knx_stack.send.knxnet_ip import header
from knx_stack.send.knxnet_ip.core import hpai

Msg = namedtuple('ConnectRequest', ['addr_control_endpoint', 'port_control_endpoint',
                                    'addr_data_endpoint', 'port_data_endpoint'])


def send(state, msg):
    """
    Build the host protocol address information: HPAI and services related header bytes
    >>> import knx_stack
    >>> state = knx_stack.State(knx_stack.Medium.knxnet_ip, None, None)
    >>> search_request = Msg(addr_control_endpoint='127.0.0.1', port_control_endpoint=1234,
    ... addr_data_endpoint='192.168.0.1', port_data_endpoint=1234)
    >>> (final_state, final_msg) = send(state, search_request)
    >>> final_msg
    06100205001A08017F00000104D20801C0A8000104D204040200
    """
    ip_control_endpoint = socket.inet_aton(msg.addr_control_endpoint)
    ip_data_endpoint = socket.inet_aton(msg.addr_data_endpoint)
    cri_len = 4
    hpai_control_endpoint = hpai.create(ip_control_endpoint, msg.port_control_endpoint)
    hpai_data_endpoint = hpai.create(ip_data_endpoint, msg.port_data_endpoint)
    cri = NetMsg([Octect(value=cri_len)])
    cri += NetMsg([Octect(value=ConnectionTypes.TUNNEL_CONNECTION)])
    cri += NetMsg([Octect(value=2)])  # tunnel link layer
    cri += NetMsg([Octect(value=0)])  # reserved
    new_msg = NetMsg(Short(value=Services.CONNECT_REQUEST.value).octects)
    new_msg += NetMsg(Short(value=cri_len + (hpai.LENGTH * 2) + HEADER_SIZE_10).octects)
    new_msg += hpai_control_endpoint
    new_msg += hpai_data_endpoint
    new_msg += cri
    (final_state, final_msg) = header.send(state, new_msg)
    return final_state, final_msg
