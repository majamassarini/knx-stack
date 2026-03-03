from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import knx_stack


class Msg(NamedTuple):
    """GroupValueWrite indication message."""

    asap: knx_stack.ASAP
    dpt: knx_stack.datapointtypes.DPT

    def __repr__(self):
        return "GroupValueWriteInd ({} for asap {})".format(
            self.dpt, self.asap
        )
