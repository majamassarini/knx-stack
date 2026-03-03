from __future__ import annotations
from knx_stack.address import Address
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


class USB(Enum):
    """USB connection status."""

    disconnected = 0
    connected = 1


class BUS(Enum):
    """KNX bus connection status."""

    disconnected = 0
    connected = 1


class MODE(Enum):
    """KNX device operating mode."""

    ldata = 0
    lraw = 1
    lbusmonitor = 2


class Medium(Enum):
    """KNX transport medium."""

    tp = 0
    usb_hid = 1
    knxnet_ip = 2


class State:
    """
    >>> import knx_stack
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(4097),
    ...                                              [knx_stack.GroupAddress(free_style=2)], 255)
    >>> association_table = knx_stack.AssociationTable(address_table,
    ...                         [knx_stack.layer.Association(address=knx_stack.GroupAddress(free_style=0x002),
    ...                                                      asap=knx_stack.ASAP(1))])
    >>> state = knx_stack.State(knx_stack.Medium.tp, association_table,
    ...                         knx_stack.GroupObjectTable({knx_stack.ASAP(1): knx_stack.datapointtypes.DPT_Switch}))
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

    def __init__(
        self,
        medium: knx_stack.Medium,
        association_table: knx_stack.AssociationTable,
        groupobject_table: knx_stack.GroupObjectTable,
    ):
        """Initialise the state with a transport medium, association table, and group object table."""
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
        """Return a multi-line string summarising the current state."""
        s = """ State for %s\n
        %s\n
        %s\n
        LData structure (for decode functions): %s\n
        ASAP: %s, APCI: %s, Address Type: %s\n
        Sequence Counter (remote): %s\n
        Sequence Counter (local): %s\n""" % (
            self.medium,
            self.association_table,
            self.datapointtypes,
            self.ldata,
            self.asap,
            self.apci,
            self.address_type,
            self.sequence_counter_remote,
            self.sequence_counter_local,
        )
        return s

    @property
    def association_table(self):
        """The association table mapping group addresses to ASAPs."""
        return self._association_table

    @property
    def datapointtypes(self):
        """The group object table mapping ASAPs to datapoint types."""
        return self._groupobject_table

    @property
    def medium(self):
        """The transport medium used by this state."""
        return self._medium

    @property
    def ldata(self):
        """The last decoded L_Data frame, used by decode functions."""
        return self._ldata

    @ldata.setter
    def ldata(self, value):
        """Set the current L_Data frame."""
        self._ldata = value

    @property
    def asap(self):
        """The Application Service Access Point used for encoding."""
        return self._asap

    @asap.setter
    def asap(self, value):
        """Set the ASAP used for encoding."""
        self._asap = value

    @property
    def apci(self):
        """The Application Protocol Control Information value."""
        return self._apci

    @apci.setter
    def apci(self, value):
        """Set the APCI value."""
        self._apci = value

    @property
    def address_type(self):
        """The address type (group or individual) for the current operation."""
        return self._address_type

    @address_type.setter
    def address_type(self, value):
        """Set the address type."""
        self._address_type = value

    @property
    def sequence_counter_remote(self):
        """The remote sequence counter, wrapping at 256."""
        return self._sequence_counter_remote

    @sequence_counter_remote.setter
    def sequence_counter_remote(self, value):
        """Set the remote sequence counter (wraps at 256)."""
        self._sequence_counter_remote = value % 256

    @property
    def sequence_counter_local(self):
        """The local sequence counter, wrapping at 256."""
        return self._sequence_counter_local

    @sequence_counter_local.setter
    def sequence_counter_local(self, value):
        """Set the local sequence counter (wraps at 256)."""
        self._sequence_counter_local = value % 256

    @property
    def individual_address(self):
        """The individual address of the local KNX device."""
        return self._association_table.individual_address

    def get_tsap(self):
        """Return the TSAP corresponding to the destination address in the current L_Data frame."""
        return self._association_table.get_tsap(
            Address(self._ldata.destination)
        )

    def get_asaps(self):
        """Return the list of ASAPs associated with the destination address in the current L_Data frame."""
        tsap = self.get_tsap()
        return self._association_table.get_asaps(tsap)

    def get_asaps_and_dpts(self):
        """Return a list of (ASAP, datapoint type) pairs for the current destination address."""
        asaps = set(self.get_asaps())
        associations = [
            (asap, dpt)
            for asap, dpt in self._groupobject_table.associations
            if asap in asaps
        ]
        return associations

    def get_tsaps(self):
        """Return the list of TSAPs associated with the current ASAP."""
        return self._association_table.get_tsaps(self._asap)

    def get_addresses(self):
        """Return the list of group addresses associated with the current ASAP."""
        tsaps = self.get_tsaps()
        return self._association_table.get_addresses(tsaps)

    def get_dpt(self):
        """Return the datapoint type associated with the current ASAP."""
        return self._groupobject_table._associations[self._asap]
