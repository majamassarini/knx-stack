from typing import NamedTuple
from enum import IntEnum


class Status(IntEnum):
    E_NO_ERROR = 0x00
    E_CONNECTION_ID = 0x21  # no active connection id
    E_DATA_CONNECTION = 0x26  # data error in connection id
    E_KNX_CONNECTION = 0x27  # knx subnetwork error in connectiond id


class Msg(NamedTuple):
    status: 'knx_stack.knxnet_ip.core.connectionstate.Status'

    def __repr__(self):
        return "ConnectionstateRes(status={})".format(self.status)
