from knx_stack.address import Address
from enum import Enum


class USB(Enum):
    disconnected = 0
    connected = 1


class BUS(Enum):
    disconnected = 0
    connected = 1


class MODE(Enum):
    ldata = 0
    lraw = 1
    lbusmonitor = 2


class Medium(Enum):
    tp = 0
    usb_hid = 1
    knxnet_ip = 2


class State:
    """
    >>> import knx_stack
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(4097),
    ...                                              [knx_stack.GroupAddress(free_style=2)], 255)
    >>> association_table = knx_stack.AssociationTable(address_table,
    ...                                                      [knx_stack.layer.Association(address=knx_stack.GroupAddress(free_style=0x002),
    ...                                                                                   asap=knx_stack.ASAP(1))])
    >>> state = State(knx_stack.Medium.tp, association_table,
    ...               knx_stack.GroupObjectTable({knx_stack.ASAP(1): knx_stack.datapointtypes.DPT_Switch}))
    >>> s = "BCE000010002010080"
    >>> msg = knx_stack.Msg.make_from_str(s)
    >>> (ldata, _) = knx_stack.layer.L_Data.make_from(msg)
    >>> state.ldata = ldata
    >>> state.get_tsap()
    1
    >>> state.get_asaps()
    [1]
    >>> state.get_asaps_and_dpts()
    [(1, <class 'knx_stack.datapointtypes.DPT_Switch'>)]
    >>> state.asap = knx_stack.ASAP(1)
    >>> state.apci = 2
    >>> state.get_tsaps()
    [1]
    >>> state.get_addresses()
    [(0x0002 0/2 0/0/2)]
    >>> state.get_dpt()
    <class 'knx_stack.datapointtypes.DPT_Switch'>
    """

    def __init__(self,
                 medium: 'knx_stack.Medium',
                 association_table: 'knx_stack.AssociationTable',
                 groupobject_table: 'knx_stack.GroupObjectTable'):
        self._association_table = association_table
        self._groupobject_table = groupobject_table
        self._medium = medium

        self._ldata = None
        self._asap = None
        self._apci = None
        self._address_type = None

        self._sequence_counter_remote = 0
        self._sequence_counter_local = 0

    def __repr__(self, *args, **kwargs):
        s = (""" State for %s\n
        %s\n
        %s\n
        LData structure (for decode functions): %s\n
        ASAP: %s, APCI: %s, Address Type: %s\n
        Sequence Counter (remote): %s\n
        Sequence Counter (local): %s\n""" % (self.medium,
                                             self.association_table,
                                             self.datapointtypes, self.ldata,
                                             self.asap, self.apci, self.address_type,
                                             self.sequence_counter_remote,
                                             self.sequence_counter_local))
        return s

    @property
    def association_table(self):
        return self._association_table

    @property
    def datapointtypes(self):
        return self._groupobject_table

    @property
    def medium(self):
        return self._medium

    @property
    def ldata(self):
        return self._ldata

    @ldata.setter
    def ldata(self, value):
        self._ldata = value

    @property
    def asap(self):
        return self._asap

    @asap.setter
    def asap(self, value):
        self._asap = value

    @property
    def apci(self):
        return self._apci

    @apci.setter
    def apci(self, value):
        self._apci = value

    @property
    def address_type(self):
        return self._address_type

    @address_type.setter
    def address_type(self, value):
        self._address_type = value

    @property
    def sequence_counter_remote(self):
        return self._sequence_counter_remote

    @sequence_counter_remote.setter
    def sequence_counter_remote(self, value):
        self._sequence_counter_remote = value % 256

    @property
    def sequence_counter_local(self):
        return self._sequence_counter_local

    @sequence_counter_local.setter
    def sequence_counter_local(self, value):
        self._sequence_counter_local = value % 256

    @property
    def individual_address(self):
        return self._association_table.individual_address

    def get_tsap(self):
        return self._association_table.get_tsap(Address(self._ldata.destination))

    def get_asaps(self):
        tsap = self.get_tsap()
        return self._association_table.get_asaps(tsap)

    def get_asaps_and_dpts(self):
        asaps = set(self.get_asaps())
        associations = [(asap, dpt) for asap, dpt in self._groupobject_table.associations
                        if asap in asaps]
        return associations

    def get_tsaps(self):
        return self._association_table.get_tsaps(self._asap)

    def get_addresses(self):
        tsaps = self.get_tsaps()
        return self._association_table.get_addresses(tsaps)

    def get_dpt(self):
        return self._groupobject_table._associations[self._asap]
