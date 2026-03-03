from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import knx_stack


class Msg(NamedTuple):
    """KNXnet/IP disconnect response message."""

    communication_channel_id: int
    status: knx_stack.knxnet_ip.ErrorCodes

    def __repr__(self):
        return "DisconnectRes(communication_channel_id={}, status={})".format(
            self.communication_channel_id, self.status
        )
