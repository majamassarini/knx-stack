from typing import NamedTuple
from enum import IntEnum


class Status(IntEnum):
    E_NO_ERROR = 0x00
    E_CONNECTION_TYPE = 0x22  # connection type not supported
    E_CONNECTION_OPTION = 0x23  # connection option not supported
    E_NO_MORE_CONNECTIONS = 0x24


class Msg(NamedTuple):
    ip: str
    port: int
    individual_address: 'knx_stack.Address'
    status: 'knx_stack.knxnet_ip.core.connect.Status'

    def __repr__(self):
        return "ConnectRes(ip={}, port={}, individual address={}, status={})".format(self.ip,
                                                                                     self.port,
                                                                                     self.individual_address,
                                                                                     self.status)
