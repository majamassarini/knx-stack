from typing import NamedTuple


class Msg(NamedTuple):
    sequence_counter: int
    status: 'knx_stack.knxnet_ip.ErrorCodes'

    def __repr__(self):
        return "TunnelingReq(sequence counter={}, status={})".format(self.sequence_counter,
                                                                     repr(self.status))
