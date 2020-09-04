from enum import IntEnum


class ServiceId(IntEnum):
    reserved = 0x00,
    DeviceFeatureGet = 0x01,
    DeviceFeatureResponse = 0x02,
    DeviceFeatureSet = 0x03,
    DeviceFeatureInfo = 0x04

