from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import knx_stack


class Msg(NamedTuple):
    """KNXnet/IP tunneling request message."""

    sequence_counter: int
    status: knx_stack.knxnet_ip.ErrorCodes

    def __repr__(self):
        return "TunnelingReq(sequence counter={}, status={})".format(
            self.sequence_counter, repr(self.status)
        )
