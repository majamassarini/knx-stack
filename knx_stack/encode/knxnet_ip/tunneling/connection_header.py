from knx_stack.msg import Octect
from knx_stack.definition.knxnet_ip import Msg as NetMsg

CONNECTION_HEADER_LEN = 4


def create(state, status, sequence_counter):
    """Encode the KNXnet/IP tunneling connection header into raw message bytes.

    Builds the four-byte connection header containing the header length,
    communication channel ID, sequence counter, and status fields.
    """
    connection_header = NetMsg(
        [
            Octect(value=CONNECTION_HEADER_LEN),
            Octect(value=state.communication_channel_id),
            Octect(value=sequence_counter),
            Octect(value=status),
        ]
    )
    return connection_header
