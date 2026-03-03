from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import knx_stack


class Msg(NamedTuple):
    asap: knx_stack.ASAP

    def __repr__(self):
        return "GroupValueReadReq (for asap {})".format(self.asap)
