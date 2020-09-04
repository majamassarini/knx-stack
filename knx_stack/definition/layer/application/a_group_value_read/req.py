from typing import NamedTuple


class Msg(NamedTuple):
    asap: 'knx_stack.ASAP'

    def __repr__(self):
        return "GroupValueReadReq (for asap {})".format(self.asap)
