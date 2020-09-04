from enum import IntEnum


class EMIId(IntEnum):
    reserved = 0x00,
    emi1 = 0x01,
    emi2 = 0x02,
    commonEmi = 0x03


