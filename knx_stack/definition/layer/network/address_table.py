from typing import Iterable


class AddressTableException(Exception):
    """ Max entries already written inside address table """


class AddressTable(object):
    """
    **4.9 Group Address Table (GrAT)**


    *4.9.1 Abstract Resource definition*


    The GrAT shall be a shared Resource of both the Data Link Layer and the group oriented Transport Layer.

    The Data Link Layer shall use the Group Address Table as a look up reference to check whether it should pass a
    decoded frame to the upper layers or not.

    The group oriented Transported Layer shall consult the Group Address Table to map an incoming LSAP (Group Address)
    to a TSAP in receiving direction and vice-versa in sending direction.

    [...]

    >>> import knx_stack
    >>> table = knx_stack.AddressTable(knx_stack.Address(4097),
    ...                                      [knx_stack.GroupAddress(free_style=0xBB),
    ...                                       knx_stack.GroupAddress(free_style=0xAA),
    ...                                       knx_stack.GroupAddress(free_style=0xCC)],
    ...                                      255)

    >>> table.individual_address
    0x1001
    >>> table.individual_address = knx_stack.Address(4098)
    >>> table.individual_address
    0x1002
    >>> table.max_size
    255
    >>> table.addresses
    [(0x00AA 0/170 0/0/170), (0x00BB 0/187 0/0/187), (0x00CC 0/204 0/0/204)]
    >>> table.tsaps
    [0, 1, 2, 3]

    >>> table.get_address(0)
    0x1002
    >>> table.get_address(2)
    (0x00BB 0/187 0/0/187)
    >>> table.get_address(4)
    Traceback (most recent call last):
    ...
    IndexError: list index out of range

    >>> table.get_tsap(knx_stack.GroupAddress(free_style=0xCC))
    3
    >>> table.get_tsap(knx_stack.GroupAddress(free_style=0xDD))

    >>> table.add(knx_stack.GroupAddress(205))
    >>> table.addresses
    [(0x00AA 0/170 0/0/170), (0x00BB 0/187 0/0/187), (0x00CC 0/204 0/0/204), (0x00CD 0/205 0/0/205)]
    >>> table.remove(knx_stack.GroupAddress(205))
    >>> table.addresses
    [(0x00AA 0/170 0/0/170), (0x00BB 0/187 0/0/187), (0x00CC 0/204 0/0/204)]

    >>> table
    AddressTable: individual address: 0x1002, max_size=255
    <BLANKLINE>
        tsap -> individual address
        0 -> 0x1002
        tsap -> group address (hex_free_style two_level_style three_level_style)
        1 -> (0x00AA 0/170 0/0/170)
        2 -> (0x00BB 0/187 0/0/187)
        3 -> (0x00CC 0/204 0/0/204)
    <BLANKLINE>
    """

    def __init__(self, ia: 'knx_stack.Address', addresses: Iterable['knx_stack.GroupAddress'], max_size: int):
        """
        :param ia: an *individual address*
        :param addresses: a list of *group addresses*
        :param max_size: max number of *group addresses*
        """
        self._max_size = max_size
        self._individual_address = ia
        self._group_addresses = list(addresses)
        self._group_addresses.sort(key=lambda group_address: group_address.free_style)

    @property
    def individual_address(self) -> 'knx_stack.Address':
        return self._individual_address

    @individual_address.setter
    def individual_address(self, ia: 'knx_stack.Address'):
        self._individual_address = ia

    @property
    def max_size(self) -> int:
        return self._max_size   
    
    @property
    def tsaps(self) -> Iterable[int]:
        return [tsap for tsap in range(0, (len(self._group_addresses) + 1))]

    @property
    def addresses(self) -> Iterable['knx_stack.GroupAddress']:
        return self._group_addresses

    def get_address(self, tsap: int) -> int:
        if tsap >= 1:
            return self._group_addresses[tsap-1]
        else:
            return self._individual_address

    def get_tsap(self, address: 'knx_stack.GroupAddress') -> int:
        try:
            return self._group_addresses.index(address) + 1
        except ValueError:
            if address == self._individual_address:
                return 0
            else:
                return None

    def add(self, address: 'knx_stack.Address') -> 'knx_stack.AddressTable':
        """
        Returns a new *Address Table* containing the given *group address*

        :param address: a new *group address* to be inserted
        :return: a new AddressTable instance
        """
        if address not in self._group_addresses or address != self._individual_address:
            if len(self._group_addresses) >= self.max_size:
                raise AddressTableException("Max entries %d, already written inside address table" % self.max_size)
            self._group_addresses.append(address)
            try:
                self._group_addresses.sort(key=lambda group_address: group_address.free_style)
            except AttributeError as e:
                raise e

    def remove(self, address: 'knx_stack.GroupAddress') -> 'knx_stack.AddressTable':
        """
        Returns a new *Address Table* without the given *group address*

        :param address: a *group address* to be removed
        :return: a new AddressTable instance
        """
        self._group_addresses.remove(address)
        self._group_addresses.sort(key=lambda group_address: group_address.free_style)

    def __repr__(self, *args, **kwargs):
        s = ("""AddressTable: individual address: {}, max_size={}\n\n""".format(self.individual_address,
                                                                                   self.max_size))

        s += """    tsap -> individual address\n"""
        s += """    0 -> {}\n""".format(self.individual_address)
        s += """    tsap -> group address (hex_free_style two_level_style three_level_style)\n"""
        for tsap, address in enumerate(self._group_addresses):
            s += """    {} -> {}\n""".format((tsap+1), address)
            
        return s
