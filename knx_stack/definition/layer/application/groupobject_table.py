from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import knx_stack


class GroupObjectTable:
    """
    A simplified version of a **Group Object Table** (4.11) with just an association between *ASAPs and Datapoint Types*.

    >>> import knx_stack
    >>> table = knx_stack.GroupObjectTable({knx_stack.ASAP(1): knx_stack.datapointtypes.DPT_UpDown})
    >>> table.associate(knx_stack.ASAP(2), knx_stack.datapointtypes.DPT_Switch)
    >>> table
    GroupObjectTable: ASAP -> datapointtype
        1 -> DPT_UpDown
        2 -> DPT_Switch
    <BLANKLINE>
    >>> len(table.associations)
    2
    >>> table.disassociate(knx_stack.ASAP(1))
    >>> len(table.associations)
    1
    """

    def __init__(self, associations: dict = None):
        """Initialise with an optional pre-populated associations dictionary."""
        if associations:
            self._associations = associations
        else:
            self._associations = {}

    @property
    def associations(self):
        """Return the ASAP-to-datapoint-type association pairs."""
        return self._associations.items()

    def associate(
        self,
        asap: knx_stack.ASAP,
        datapointtype: knx_stack.datapointtypes.DPT,
    ):
        """Associate an ASAP with a datapoint type."""
        self._associations[asap] = datapointtype

    def disassociate(self, asap: knx_stack.ASAP):
        """Remove the association for the given ASAP."""
        del self._associations[asap]

    def __repr__(self, *args, **kwargs):
        """Return a multi-line string listing all ASAP-to-datapoint-type associations."""
        s = "GroupObjectTable: ASAP -> datapointtype\n"
        for asap, datapointtype in self._associations.items():
            s += "    {} -> {}\n".format(asap, datapointtype.__name__)
        return s
