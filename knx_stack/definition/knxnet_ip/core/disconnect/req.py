from typing import NamedTuple


class Msg(NamedTuple):
    """KNXnet/IP disconnect request message."""

    addr_control_endpoint: str
    port_control_endpoint: int

    def __repr__(self):
        return "DisconnectReq (control endpoint = {}:{})".format(
            self.addr_control_endpoint, self.port_control_endpoint
        )
