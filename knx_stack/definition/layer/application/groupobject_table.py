from typing import Dict


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

    def __init__(self, associations: Dict = None):
        if associations:
            self._associations = associations
        else:
            self._associations = {}

    @property
    def associations(self):
        return self._associations.items()

    def associate(self, asap: 'knx_stack.ASAP', datapointtype: 'knx_stack.datapointtypes.DPT'):
        self._associations[asap] = datapointtype

    def disassociate(self, asap: 'knx_stack.ASAP'):
        del self._associations[asap]

    def __repr__(self, *args, **kwargs):
        s = "GroupObjectTable: ASAP -> datapointtype\n"
        for asap, datapointtype in self._associations.items():
            s += "    {} -> {}\n".format(asap, datapointtype.__name__)
        return s
