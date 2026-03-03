from knx_stack import Octect, Short
from knx_stack.definition.knxnet_ip import Msg as NetMsg, IPV4_UDP

LENGTH = 8


def create(ip, port):
    """Encode a KNXnet/IP HPAI (Host Protocol Address Information) structure.

    Builds the HPAI block containing the structure length, IPv4/UDP protocol
    indicator, IP address bytes, and port number.
    """
    hpai = NetMsg([Octect(value=LENGTH), Octect(value=IPV4_UDP)])
    hpai += NetMsg([Octect(value=b) for b in ip])
    hpai += NetMsg(Short(value=port).octects)
    return hpai
