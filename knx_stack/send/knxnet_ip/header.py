from knx_stack.knxnet_ip import HEADER_SIZE_10, KNXNETIP_VERSION_10
from knx_stack.msg import Msg, Octect


def send(state, msg):
    final_msg = Msg([Octect(value=HEADER_SIZE_10), Octect(value=KNXNETIP_VERSION_10)] + msg)
    return state, final_msg
