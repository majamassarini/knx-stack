from collections import namedtuple

Association = namedtuple('Association',['asap', 'tsap'])
AddressAssociation = namedtuple('AddressAssociation',['asap', 'address'])


class AssociationTable(object):
    
    def __init__(self, address_table, associations):
        """
        >>> from knx_stack.hid.report_body import AddressTable
        >>> address_table = AddressTable(4097, [], 255)
        >>> association_table = AssociationTable(address_table, [])
        >>> new_association_table = association_table.associate(111, 1)
        >>> new_association_table.associations
        [AddressAssociation(asap=1, address=111)]
        >>> new_association_table.addresses
        [111]
        >>> new_association_table.get_tsap(111)
        1
        >>> new_association_table.get_addresses_from(1)
        [111]
        >>> new_association_table.asaps
        [1]
        >>> another_association_table = new_association_table.disassociate(111, 1)
        >>> another_association_table.associations
        []
        >>> another_association_table.addresses
        []
        """        
        
        self._address_table = address_table
        self._rebuild(associations)
        
    def __getattribute__(self, *args, **kwargs):
        try:
            return object.__getattribute__(self, *args, **kwargs)
        except AttributeError:
            if args[0] in ('tsaps', 'addresses', 'individual_address',
                           'get_address', 'get_addresses', 'get_tsap',
                           'append', 'remove'):
                return self._address_table.__getattribute__(*args, **kwargs)
            
    def _rebuild(self, associations):
        self._structure = {}
        for key, association in enumerate(associations):
            tsap = self._address_table.get_tsap(association.address)
            self._structure[key] = Association(tsap=tsap, asap=association.asap)        
    
    def get_tsaps(self, asap):
        tsaps = [association.tsap for association in self._structure.values() if association.asap == asap]
        return tsaps
    
    def get_asaps(self, tsap):
        asaps = [association.asap for association in self._structure.values() if association.tsap == tsap]
        return asaps
            
    @property
    def associations(self):
        asap_address_associations = []
        for association in self._structure.values():
            address_association = AddressAssociation(association.asap,
                                                     self._address_table.get_address(association.tsap))
            asap_address_associations.append(address_association)
        return asap_address_associations

    @property
    def asaps(self):
        return [association.asap for association in self.associations]
            
    def _append(self, address, asap):
        old_associations = self.associations
        new_address_table = self._address_table.append(address)
        old_associations.append(AddressAssociation(asap=asap, address=address))
        old_associations.sort(key=lambda ass: ass.asap)
        return AssociationTable(new_address_table, old_associations)

    def _remove(self, address, asap):
        old_associations = [association for association in self.associations if association.address != address
                            or association.asap != asap]
        new_address_table = self._address_table.remove(address)
        return AssociationTable(new_address_table, old_associations)
            
    def get_addresses_from(self, asap):
        tsaps = self.get_tsaps(asap)
        addresses = self._address_table.get_addresses(tsaps)
        return addresses

    def associate(self, address, asap):
        return self._append(address, asap)

    def associate_addresses(self, addresses, asap):
        new_association_table = self
        for address in addresses:
            new_association_table = new_association_table._append(address, asap)
        return new_association_table

    def disassociate(self, address, asap):
        return self._remove(address, asap)

    def __repr__(self, *args, **kwargs):
        s = (""" AssociationTable: %s \n\n\t %s""" % (self._structure, self._address_table))
        return s
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()    