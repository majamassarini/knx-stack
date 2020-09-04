from typing import NamedTuple


class Msg(NamedTuple):
    addr: str
    port: int

    def __repr__(self):
        return "SearchReq ({}:{})".format(self.addr, self.port)
