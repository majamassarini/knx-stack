from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple
from enum import IntEnum

if TYPE_CHECKING:
    import knx_stack


class Status(IntEnum):
    """KNXnet/IP connect response status codes."""

    E_NO_ERROR = 0x00
    E_CONNECTION_TYPE = 0x22  # connection type not supported
    E_CONNECTION_OPTION = 0x23  # connection option not supported
    E_NO_MORE_CONNECTIONS = 0x24


class Msg(NamedTuple):
    """KNXnet/IP connect response message."""

    ip: str
    port: int
    individual_address: knx_stack.Address
    status: "Status"

    def __repr__(self):
        return "ConnectRes(ip={}, port={}, individual address={}, status={})".format(
            self.ip, self.port, self.individual_address, self.status
        )
