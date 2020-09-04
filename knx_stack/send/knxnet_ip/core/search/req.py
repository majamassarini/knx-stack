import socket

from collections import namedtuple

from knx_stack import Octect, Short
from knx_stack.knxnet_ip import Msg as NetMsg, Services, HEADER_SIZE_10, IPV4_UDP
from knx_stack.send.knxnet_ip import header
from knx_stack.send.knxnet_ip.core import hpai

Msg = namedtuple('SearchRequest', ['addr', 'port'])


def send(state, msg):
    """
    >>> import knx_stack
    >>> state = knx_stack.State(knx_stack.Medium.knxnet_ip, None, None)
    >>> search_request = Msg(addr='127.0.0.1', port=1234)
    >>> (final_state, final_msg) = send(state, search_request)
    >>> final_msg
    06100201000E08017F00000104D2
    """
    ip = socket.inet_aton(msg.addr)
    hpai_ = hpai.create(ip, msg.port)
    new_msg = NetMsg(Short(value=Services.SEARCH_REQUEST.value).octects)
    new_msg += NetMsg(Short(value=(hpai.LENGTH + HEADER_SIZE_10)).octects)
    new_msg += hpai_
    (final_state, final_msg) = header.send(state, new_msg)
    return final_state, final_msg
