from typing import NamedTuple


class Msg(NamedTuple):
    addr_control_endpoint: str
    port_control_endpoint: int
    addr_data_endpoint: str
    port_data_endpoint: int

    def __repr__(self):
        return "ConnectReq (control endpoint = {}:{} data endpoint {}:{})".format(self.addr_control_endpoint,
                                                                                  self.port_control_endpoint,
                                                                                  self.addr_data_endpoint,
                                                                                  self.port_data_endpoint)
