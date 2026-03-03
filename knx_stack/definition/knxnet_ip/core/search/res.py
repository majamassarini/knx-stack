from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import knx_stack


class Msg(NamedTuple):
    """KNXnet/IP search response message."""

    ip: str
    port: int
    individual_address: knx_stack.Address

    def __repr__(self):
        return "SearchRes(ip={}, port={}, individual address={})".format(
            self.ip, self.port, self.individual_address
        )
