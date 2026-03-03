from ctypes import c_uint8, c_uint16, LittleEndianStructure, Union


class ThreeLevelStyle(LittleEndianStructure):
    """KNX group address in three-level style (main/middle/sub)."""

    _fields_ = [
        ("sub", c_uint8, 8),
        ("middle", c_uint8, 3),
        ("main", c_uint8, 5),
    ]


class TwoLevelStyle(LittleEndianStructure):
    """KNX group address in two-level style (main/sub)."""

    _fields_ = [
        ("sub", c_uint16, 11),
        ("main", c_uint16, 5),
    ]


class Address(Union):
    """
    A 16-bit address wrapper.

    A common representation for both *individual addresses* and *group addresses*.

    >>> import knx_stack
    >>> g = knx_stack.Address(0x0A)
    >>> g.free_style
    10
    """

    _fields_ = [
        ("free_style", c_uint16),
    ]

    def __repr__(self, *args, **kwargs):
        """Return the address as a zero-padded 4-digit hex string."""
        return "0x%04X" % (self.free_style)

    def __eq__(self, other):
        """Compare two addresses by their free-style value."""
        try:
            return self.free_style == other.free_style
        except AttributeError as e:
            raise e

    def __hash__(self):
        """Hash the address using its free-style value."""
        return self.free_style


class GroupAddress(Union):
    """
    A wrapper to c_uint16.

    It has properties to access *three level style* and *two level style* group addresses representations.

    >>> import knx_stack
    >>> g = knx_stack.GroupAddress(three_level_style=knx_stack.address.ThreeLevelStyle(main=1, middle=1, sub=1))
    >>> hex(g.free_style)
    '0x901'
    >>> g.two_level_style.main
    1
    >>> g.three_level_style.middle
    1
    >>> g
    (0x0901 1/257 1/1/1)

    >>> g = knx_stack.GroupAddress(free_style=0x1202)
    >>> hex(g.free_style)
    '0x1202'
    >>> g.two_level_style.main
    2
    >>> g.three_level_style.middle
    2
    >>> g
    (0x1202 2/514 2/2/2)
    """

    _fields_ = [
        ("free_style", c_uint16),
        ("two_level_style", TwoLevelStyle),
        ("three_level_style", ThreeLevelStyle),
    ]

    def __repr__(self, *args, **kwargs):
        """Return the address in free-style, two-level, and three-level formats."""
        return "(0x%04X %d/%d %d/%d/%d)" % (
            self.free_style,
            self.two_level_style.main,
            self.two_level_style.sub,
            self.three_level_style.main,
            self.three_level_style.middle,
            self.three_level_style.sub,
        )

    def __eq__(self, other):
        """Compare two group addresses by their free-style value."""
        try:
            return self.free_style == other.free_style
        except AttributeError as e:
            raise e

    def __hash__(self):
        """Hash the group address using its free-style value."""
        return self.free_style
