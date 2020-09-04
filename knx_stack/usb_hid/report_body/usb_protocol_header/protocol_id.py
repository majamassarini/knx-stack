from enum import IntEnum


class ProtocolId(IntEnum):
    reserved = 0x00,
    KNXTunnel = 0x01,
    MBusTunnel = 0x02,
    BatiBusTunnel = 0x03,
    BusAccessServerFeatureService = 0x0F


