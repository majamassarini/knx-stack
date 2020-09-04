from ctypes import c_uint8, c_uint16, c_uint32, LittleEndianStructure, Union


class _PropertyServiceHeader(LittleEndianStructure):

    _fields_ = [
        ('start_index', c_uint16, 12),
        ('number_of_elements', c_uint16, 4),
        ('property_id', c_uint8, 8),
        ('object_index', c_uint8, 8),
                ]


class PropertyServiceHeader(Union):
    """
    >>> h = PropertyServiceHeader()
    >>> h.value = 0x0079101F
    >>> h.bits.object_index
    0
    >>> h.bits.property_id
    121
    >>> h.bits.number_of_elements
    1
    >>> h.bits.start_index
    31
    """

    _fields_ = [('bits', _PropertyServiceHeader),
                ('value', c_uint32)]

