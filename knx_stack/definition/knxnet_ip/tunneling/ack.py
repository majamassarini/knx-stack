from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import knx_stack


class Msg(NamedTuple):
    sequence_counter: int
    status: knx_stack.knxnet_ip.ErrorCodes

    def __repr__(self):
        return "TunnelingAck(sequence counter={}, status={})".format(
            self.sequence_counter, self.status
        )
