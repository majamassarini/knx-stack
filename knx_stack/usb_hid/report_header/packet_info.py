from enum import IntEnum


class PacketType(IntEnum):
    reserved = 0x00,
    allInOnePacket = 0x03,
    partialPacket = 0x04,
    startPacket = 0x05,
    endPacket = 0x06

