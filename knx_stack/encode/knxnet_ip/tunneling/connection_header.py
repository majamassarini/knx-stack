from knx_stack.msg import Octect
from knx_stack.definition.knxnet_ip import Msg as NetMsg

CONNECTION_HEADER_LEN = 4


def create(state, status, sequence_counter):
    connection_header = NetMsg([Octect(value=CONNECTION_HEADER_LEN),
                                Octect(value=state.communication_channel_id),
                                Octect(value=sequence_counter),
                                Octect(value=status)])
    return connection_header
