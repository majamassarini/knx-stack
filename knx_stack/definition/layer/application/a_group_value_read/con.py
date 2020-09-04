from typing import NamedTuple


class Msg(NamedTuple):
    asap: 'knx_stack.ASAP'
    dpt: 'knx_stack.datapointtypes.DPT'
    status: 'knx_stack.layer.link.ConfirmFlag'

    def __repr__(self):
        return "GroupValueReadCon status {} ({} for asap {})".format(self.status.value, self.dpt, self.asap)
