from typing import NamedTuple


class Msg(NamedTuple):
    ip: str
    port: int
    individual_address: 'knx_stack.Address'

    def __repr__(self):
        return "SearchRes(ip={}, port={}, individual address={})".format(self.ip,
                                                                         self.port,
                                                                         self.individual_address)
