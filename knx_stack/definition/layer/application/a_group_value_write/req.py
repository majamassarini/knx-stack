from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import knx_stack


class Msg(NamedTuple):
    asap: knx_stack.ASAP
    dpt: knx_stack.datapointtypes.DPT

    def __repr__(self):
        return "GroupValueWriteReq ({} for asap {})".format(
            self.dpt, self.asap
        )
