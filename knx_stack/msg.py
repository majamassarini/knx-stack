from ctypes import c_uint8, LittleEndianStructure, Union, c_uint16, c_uint32
from typing import Iterable, Tuple


class Msg(list):
    """
    A bus message wrapper which is able to consume the message's bytes in different ways: through an octect,
    through a short or through a long.

    >>> import knx_stack
    >>> msg = knx_stack.Msg.make_from_str("112203AA0B0C0D")
    >>> (head, body) = msg.octect()
    >>> head
    0x11
    >>> body
    2203AA0B0C0D
    >>> (head, body) = body.short()
    >>> head
    0x2203
    >>> body
    AA0B0C0D
    >>> (head, body) = body.long()
    >>> head
    0xAA0B0C0D
    >>> body
    <BLANKLINE>
    """

    @classmethod
    def make_from_str(cls, msg: str) -> 'knx_stack.Msg':
        octects = cls.stringtooctects(msg)
        return cls(octects)
    
    @staticmethod
    def stringtooctects(msg: str) -> Iterable['knx_stack.msg.Octect']:
        high_nibbles = [int(nibble, 16) for index, nibble in enumerate(msg) if not index % 2]
        low_nibbles = [int(nibble, 16) for index, nibble in enumerate(msg) if index % 2]
        return list(map(lambda high_nibble, low_nibble: Octect(Nibbles(high=high_nibble, low=low_nibble)), high_nibbles, low_nibbles))
            
    def octect(self) -> Tuple['knx_stack.msg.Octect', 'knx_stack.Msg']:
        """
        Consumes an Octect from the message's byte list

        :return: Tuple(Octect, the other bytes as a new Msg)
        """
        return self[0], self.__class__(self[1:])
    
    def short(self) -> Tuple['knx_stack.msg.Short', 'knx_stack.Msg']:
        """
        Consumes a Short from the message's byte list

        :return: Tuple(Short, the other bytes as a new Msg)
        """
        short = Short()
        short.byte.MSB = self[0].value
        short.byte.LSB = self[1].value
        return short, self.__class__(self[2:])

    def long(self) -> Tuple['knx_stack.msg.Long', 'knx_stack.Msg']:
        """
        Consumes a Long from the message's byte list

        :return: Tuple(Long, the other bytes as a new Msg)
        """
        long = Long()
        long.byte.B4 = self[0].value
        long.byte.B3 = self[1].value
        long.byte.B2 = self[2].value
        long.byte.B1 = self[3].value
        return long, self.__class__(self[4:])

    def __repr__(self, *args, **kwargs):
        s = ""
        for o in self:
            s += "%02X" % o.value
        return s


class Nibbles(LittleEndianStructure):
    _fields_ = [('low', c_uint8, 4),
                ('high', c_uint8, 4)]


class Octect(Union):
    """
    A wrapper for a byte value with methods to access *low* and *high* nibbles.

    >>> import knx_stack
    >>> o = knx_stack.msg.Octect(knx_stack.msg.Nibbles(high=1, low=0))
    >>> o
    0x10
    >>> o.nibble.high
    1
    >>> o.nibble.low
    0
    >>> o.value
    16
    """

    _fields_ = [('nibble', Nibbles),
                ('value', c_uint8)]

    def __repr__(self, *args, **kwargs):
        return "0x%02X" % self.value


class Bytes(LittleEndianStructure):
    _fields_ = [('LSB', c_uint8, 8),
                ('MSB', c_uint8, 8)]


class Short(Union):
    """
    A wrapper for a short value with methods to access *MSB (most significant byte)*, *LSB (less significant byte)*
    and both its octects.

    >>> import knx_stack
    >>> MSB = knx_stack.msg.Octect(knx_stack.msg.Nibbles(high=1, low=0)).value
    >>> LSB = knx_stack.msg.Octect(knx_stack.msg.Nibbles(high=0, low=1)).value
    >>> bytes = knx_stack.msg.Bytes(MSB=MSB, LSB=LSB)
    >>> short = knx_stack.msg.Short(bytes)
    >>> short
    0x1001
    >>> short.byte.MSB
    16
    >>> short.byte.LSB
    1
    >>> short.value
    4097
    """

    _fields_ = [('byte', Bytes),
                ('value', c_uint16)]

    @property
    def MSB(self) -> 'knx_stack.msg.Octect':
        return Octect(value=self.byte.MSB)

    @property
    def LSB(self) -> 'knx_stack.msg.Octect':
        return Octect(value=self.byte.LSB)

    @property
    def octects(self) -> Iterable['knx_stack.msg.Octect']:
        return[self.MSB, self.LSB]

    def __repr__(self, *args, **kwargs):
        return "0x%04X" % self.value


class LBytes(LittleEndianStructure):
    _fields_ = [('B1', c_uint32, 8),
                ('B2', c_uint32, 8),
                ('B3', c_uint32, 8),
                ('B4', c_uint32, 8),
                ]


class Long(Union):
    """
    A wrapper for a long value with methods to access its single bytes or octects.

    >>> import knx_stack
    >>> long = knx_stack.msg.Long(value=0x91000008)
    >>> long.B1
    0x08
    >>> long.B2
    0x00
    >>> long.B3
    0x00
    >>> long.B4
    0x91
    """

    _fields_ = [('byte', LBytes),
                ('value', c_uint32)]

    @property
    def B1(self) -> 'knx_stack.msg.Octect':
        return Octect(value=self.byte.B1)

    @property
    def B2(self) -> 'knx_stack.msg.Octect':
        return Octect(value=self.byte.B2)

    @property
    def B3(self) -> 'knx_stack.msg.Octect':
        return Octect(value=self.byte.B3)

    @property
    def B4(self) -> 'knx_stack.msg.Octect':
        return Octect(value=self.byte.B4)

    @property
    def octects(self) -> Iterable['knx_stack.msg.Octect']:
        return [self.B4, self.B3, self.B2, self.B1]

    def __repr__(self, *args, **kwargs):
        return "0x%08X" % self.value

