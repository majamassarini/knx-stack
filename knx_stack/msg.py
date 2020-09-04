from ctypes import c_uint8, LittleEndianStructure, Union, c_uint16, c_uint32


class Msg(list):
    """
    >>> s = "0102030A"
    >>> octects = Msg.stringtooctects(s)
    >>> msg = Msg(octects)
    >>> (head, body) = msg.octect()
    >>> head.value
    1
    >>> (head, body) = body.short()
    >>> head.value
    515
    >>> (head, body) = body.octect()
    >>> head.value
    10
    """
    
    @staticmethod
    def stringtooctects(list_):
        high_nibbles = [int(nibble, 16) for index, nibble in enumerate(list_) if not index % 2]
        low_nibbles = [int(nibble, 16) for index, nibble in enumerate(list_) if index % 2]
        return list(map(lambda high_nibble, low_nibble: Octect(Nibbles(high=high_nibble, low=low_nibble)), high_nibbles, low_nibbles))
            
    def octect(self):
        return self[0], self.__class__(self[1:])
    
    def short(self):
        short = Short()
        short.byte.MSB = self[0].value
        short.byte.LSB = self[1].value
        return short, self.__class__(self[2:])

    def long(self):
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
    >>> o = Octect(Nibbles(high=1, low=0))
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
    >>> MSB = Octect(Nibbles(high=1, low=0)).value
    >>> MSB
    16
    >>> LSB = Octect(Nibbles(high=0, low=0)).value
    >>> LSB
    0
    >>> bytes = Bytes(MSB=MSB, LSB=LSB)
    >>> short = Short(bytes)
    >>> short.value
    4096
    """

    _fields_ = [('byte', Bytes),
                ('value', c_uint16)]

    @property
    def MSB(self):
        return Octect(value=self.byte.MSB)

    @property
    def LSB(self):
        return Octect(value=self.byte.LSB)

    @property
    def octects(self):
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
    >>> long = Long(value=0x91000008)
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
    def B1(self):
        return Octect(value=self.byte.B1)

    @property
    def B2(self):
        return Octect(value=self.byte.B2)

    @property
    def B3(self):
        return Octect(value=self.byte.B3)

    @property
    def B4(self):
        return Octect(value=self.byte.B4)

    @property
    def octects(self):
        return [self.B4, self.B3, self.B2, self.B1]

    def __repr__(self, *args, **kwargs):
        return "0x%08X" % self.value

    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
