from typing import NamedTuple


class Msg(NamedTuple):
    communication_channel_id: int
    status: 'knx_stack.knxnet_ip.ErrorCodes'

    def __repr__(self):
        return "DisconnectRes(communication_channel_id={}, status={})".format(self.communication_channel_id,
                                                                              self.status)
