from knx_stack import Octect, Short
from knx_stack.definition.knxnet_ip import Msg as NetMsg, IPV4_UDP

LENGTH = 8


def create(ip, port):
    hpai = NetMsg([Octect(value=LENGTH), Octect(value=IPV4_UDP)])
    hpai += NetMsg([Octect(value=b) for b in ip])
    hpai += NetMsg(Short(value=port).octects)
    return hpai
