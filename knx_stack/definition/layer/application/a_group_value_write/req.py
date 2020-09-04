from typing import NamedTuple


class Msg(NamedTuple):
    asap: 'knx_stack.ASAP'
    dpt: 'knx_stack.datapointtypes.DPT'

    def __repr__(self):
        return "GroupValueWriteReq ({} for asap {})".format(self.dpt, self.asap)
