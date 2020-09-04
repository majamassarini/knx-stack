import socket

from knx_stack import Short
from knx_stack.definition.knxnet_ip import Msg as NetMsg, Services, HEADER_SIZE_10
from knx_stack.encode.knxnet_ip import header
from knx_stack.encode.knxnet_ip.core import hpai


def encode(state: 'knx_stack.State', msg: 'knx_stack.knxnet_ip.core.search.req.Msg') -> 'knx_stack.Msg':
    """
    >>> import knx_stack
    >>> state = knx_stack.State(knx_stack.Medium.knxnet_ip, None, None)
    >>> search_request = knx_stack.knxnet_ip.core.search.req.Msg(addr='127.0.0.1', port=1234)
    >>> bus_msg = knx_stack.encode_msg(state, search_request)
    >>> bus_msg
    06100201000E08017F00000104D2
    """
    ip = socket.inet_aton(msg.addr)
    hpai_ = hpai.create(ip, msg.port)
    new_msg = NetMsg(Short(value=Services.SEARCH_REQUEST.value).octects)
    new_msg += NetMsg(Short(value=(hpai.LENGTH + HEADER_SIZE_10)).octects)
    new_msg += hpai_
    final_msg = header.encode(state, new_msg)
    return final_msg
