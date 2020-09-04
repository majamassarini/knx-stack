from enum import IntEnum


class FeatureId(IntEnum):
    supportedEMIType = 0x01,
    hostDeviceDescriptorType = 0x02,
    busConnectionStatus = 0x03,
    knxManufacturerCode = 0x04,
    activeEMIType = 0x05

