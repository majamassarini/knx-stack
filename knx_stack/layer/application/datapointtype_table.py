class DatapointtypeTable(object):
    """
    >>> from knx_stack.datapointtypes import DPT_Switch
    >>> table = DatapointtypeTable({})
    >>> new_table = table.associate(1, DPT_Switch)
    >>> len(new_table.associations)
    1
    >>> new_table = new_table.disassociate(1)
    >>> new_table.associations
    dict_items([])
    """

    def __init__(self, associations):
        self._associations = associations

    @property
    def associations(self):
        return self._associations.items()

    def associate(self, asap, datapointtype):
        new_associations = {k:v for (k, v) in self.associations}
        new_associations[asap] = datapointtype
        return DatapointtypeTable(new_associations)

    def disassociate(self, asap):
        new_associations = {k:v for (k, v) in self.associations}
        del new_associations[asap]
        return DatapointtypeTable(new_associations)

    def __repr__(self, *args, **kwargs):
        s = (""" DatapointtypeTable: %s \n\n\t""" % (self._associations))
        return s

if __name__ == "__main__":
    import doctest
    doctest.testmod()
