from typing import Iterable
from collections import namedtuple

Association = namedtuple('Association', ['asap', 'address'])


class ASAP:
    """
    **Application Service Access Point**

    Ideally connects a **piece of code** with messages from/to one or more **group addressess**.

    An ASAP in KNX specifications is an int.

    This implementation can add to the ASAP identifier (an int value) a **name**.

    >>> import knx_stack
    >>> asap_no_name = knx_stack.ASAP(1)
    >>> asap_no_name
    1
    >>> asap_with_name = knx_stack.ASAP(1, 'a meaningfull name to the connected piece of code')
    >>> asap_with_name
    1 (a meaningfull name to the connected piece of code)
    >>> asap_no_name == asap_with_name
    True
    >>> len(set([asap_no_name, asap_with_name]))
    1
    """

    def __init__(self, value: int, name: str = None):
        self._value = value
        self._name = name

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    def __repr__(self, *args, **kwargs):
        if self.name:
            s = "{} ({})".format(self.value, self.name)
        else:
            s = "{}".format(self.value)
        return s

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return self.value


class AssociationTable(object):
    """
    **4.10 Group Object Association Table (GrOAT)**

    *4.10.1 Abstract Resource definition*

    The Group Objects Association Table shall be a parameter of the Application Layer.

    It shall store the relationship between Transport Layer Service Access Points (TSAPs) and
    Application Layer Service Access Points (ASAP).
    The information on this relationship is needed when mapping the Multicast Communication Mode messages
    A_GroupValue_Read, A_GroupValue_Response and A_GroupValue_Write to T_Data_Group-messages and vice versa.

    The **TSAP** shall be an index in the Group Address Table.

    The **ASAP** shall be the Group Object number.

    The lowest ASAP shall be 0.
    The ASAP shall in this Resource be a unique identifier for a Group Object to the Application Layer.
    The ASAP for this Resource shall thus be a Group Object Number.

    [...]

    >>> import knx_stack
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(4097), [], 255)
    >>> asap_pippo = knx_stack.ASAP(1, "one")
    >>> asap_pluto = knx_stack.ASAP(2, "two")
    >>> table = knx_stack.AssociationTable(address_table, [knx_stack.Association(asap=asap_pippo,
    ...                                                                          address=knx_stack.GroupAddress(free_style=111))])
    >>> table.associate(asap_pippo, [knx_stack.GroupAddress(free_style=112)])
    >>> table.associate(asap_pippo, [knx_stack.GroupAddress(free_style=110)])
    >>> table.associate(asap_pluto, [knx_stack.GroupAddress(free_style=109)])
    >>> table.get_tsap(knx_stack.GroupAddress(free_style=111))
    3
    >>> table.get_addresses([3, 4, 2])
    [(0x006F 0/111 0/0/111), (0x0070 0/112 0/0/112), (0x006E 0/110 0/0/110)]
    >>> table.asaps
    dict_keys([0 (individual address), 1 (one), 2 (two)])
    >>> table.disassociate(asap_pippo, [knx_stack.GroupAddress(free_style=112)])
    >>> table.get_addresses([3, 2])
    [(0x006F 0/111 0/0/111), (0x006E 0/110 0/0/110)]
    >>> table.get_tsaps(asap_pippo)
    [3, 2]
    >>> table.get_tsap(knx_stack.GroupAddress(free_style=110))
    2
    >>> table
    AssociationTable: asap -> addresses
        0 (individual address) -> [0x1001]
        1 (one) -> [(0x006F 0/111 0/0/111), (0x006E 0/110 0/0/110)]
        2 (two) -> [(0x006D 0/109 0/0/109)]
    AddressTable: individual address: 0x1001, max_size=255
    <BLANKLINE>
        tsap -> individual address
        0 -> 0x1001
        tsap -> group address (hex_free_style two_level_style three_level_style)
        1 -> (0x006D 0/109 0/0/109)
        2 -> (0x006E 0/110 0/0/110)
        3 -> (0x006F 0/111 0/0/111)
    <BLANKLINE>
    """

    def __init__(self, address_table: 'knx_stack.AddressTable', associations: Iterable['Association'] = None):
        self._address_table = address_table
        self._asap_addresses = dict()
        self._tsap_asaps = dict()
        self.associate(ASAP(0, "individual address"), [self._address_table.individual_address])
        if associations:
            for association in associations:
                self.associate(association.asap, [association.address])

    @property
    def individual_address(self) -> 'knx_stack.Address':
        return self._address_table.individual_address

    def get_tsap(self, address: 'knx_stack.GroupAddress') -> int:
        return self._address_table.get_tsap(address)

    def get_tsaps(self, asap: 'knx_stack.ASAP') -> Iterable[int]:
        tsaps = [self.get_tsap(address) for address in self._asap_addresses[asap] if asap in self._asap_addresses]
        return tsaps

    def get_asaps(self, tsap: int) -> Iterable['knx_stack.ASAP']:
        return self._tsap_asaps[tsap]

    def get_asaps_from_address(self, address: 'knx_stack.GroupAddress') -> Iterable['knx_stack.ASAP']:
        tsap = self._address_table.get_tsap(address)
        return self._tsap_asaps[tsap]

    @property
    def asaps(self):
        return self._asap_addresses.keys()

    def get_free_asap_value(self):
        asaps = self._asap_addresses.keys()
        for e, asap in enumerate(asaps):
            if e != asap.value:
                return e
        return len(asaps)

    def get_addresses(self, tsaps: Iterable[int]):
        addresses = list()
        for tsap in tsaps:
            addresses.append(self._address_table.get_address(tsap))
        return addresses

    def _rebuild_tsap_asaps(self):
        self._tsap_asaps = dict()
        for asap_, addresses in self._asap_addresses.items():
            for address_ in addresses:
                tsap = self._address_table.get_tsap(address_)
                if tsap not in self._tsap_asaps:
                    self._tsap_asaps[tsap] = list()
                self._tsap_asaps[tsap].append(asap_)

    def associate(self, asap: 'knx_stack.ASAP', addresses: Iterable['knx_stack.GroupAddress']) -> None:
        for address in addresses:
            if (address not in self._address_table.addresses and
                    address is not self.individual_address):
                self._address_table.add(address)

        if asap not in self._asap_addresses:
            self._asap_addresses[asap] = list()
        for address in addresses:
            self._asap_addresses[asap].append(address)

        self._rebuild_tsap_asaps()

    def disassociate(self, asap: 'knx_stack.ASAP', addresses: Iterable['knx_stack.GroupAddress']) -> None:
        for address in addresses:
            if address != self.individual_address:
                self._address_table.remove(address)
            self._asap_addresses[asap].remove(address)

        self._rebuild_tsap_asaps()

    def __repr__(self, *args, **kwargs):
        s = "AssociationTable: asap -> addresses\n"
        for asap, addresses in self._asap_addresses.items():
            s += "    {} -> {}\n".format(asap, addresses)
        s += "{}".format(self._address_table)
        return s
