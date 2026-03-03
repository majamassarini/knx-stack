from __future__ import annotations
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import knx_stack


class Msg(NamedTuple):
    asap: knx_stack.ASAP
    dpt: knx_stack.datapointtypes.DPT
    status: knx_stack.layer.link.ConfirmFlag

    def __repr__(self):
        return "GroupValueWriteCon status {} ({} for asap {})".format(
            self.status.value, self.dpt, self.asap
        )
