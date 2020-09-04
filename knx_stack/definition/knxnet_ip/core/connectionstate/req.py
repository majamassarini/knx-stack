from typing import NamedTuple


class Msg(NamedTuple):
    addr_control_endpoint: str
    port_control_endpoint: int

    def __repr__(self):
        return "ConnectionstateReq (control endpoint = {}:{})".format(self.addr_control_endpoint,
                                                                      self.port_control_endpoint)
