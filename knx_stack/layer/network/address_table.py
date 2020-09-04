class AddressTableException(Exception):
    """ Max entries already written inside address table """


class AddressTable(object):
    
    def __init__(self, ia, addresses, max_size):
        """
        >>> table = AddressTable(4097, [170, 187, 204], 255)
        >>> table.max_size
        255
        >>> table.addresses
        [170, 187, 204]
        >>> table.individual_address
        4097
        >>> table.tsaps
        [0, 1, 2, 3]
        >>> new_table = table.append(205)
        >>> new_table.addresses
        [170, 187, 204, 205]
        >>> table.addresses
        [170, 187, 204]
        >>> another_new_table = new_table.remove(205)
        >>> table.addresses == another_new_table.addresses
        True
        >>> s = str(another_new_table)        
        """
        self._max_size = max_size
        self._rebuild(ia, addresses)
        
    def _rebuild(self, ia, addresses):
        self._structure = {}
        self.individual_address = ia
        for tsap, address in enumerate(addresses):
            self._structure[tsap+1] = address     
            
    @property
    def max_size(self):
        return self._max_size   
    
    @property
    def tsaps(self):
        tsaps = list(self._structure.keys())
        tsaps.sort() 
        return tsaps
    
    @property
    def addresses(self):
        addresses = list(self._structure.values())
        addresses.remove(self.individual_address)
        addresses.sort()
        return addresses
    
    @property
    def individual_address(self):
        return self._structure[0]
    
    @individual_address.setter
    def individual_address(self, ia):
        self._structure[0] = ia
    
    def get_address(self, tsap):
        return self._structure[tsap]
    
    def get_addresses(self, tsaps):
        addresses = [self._structure[tsap] for tsap in tsaps]
        return addresses
    
    def get_tsap(self, address):
        tsaps = [tsap for tsap, stored_address in self._structure.items() if address == stored_address]
        if tsaps:
            tsap = tsaps.pop()
        else:
            tsap = None
        return tsap
    
    def append(self, address):
        if len(self._structure) >= self.max_size:
            raise AddressTableException("Max entries %d, already written inside address table" % self.max_size)
        addresses = set(self.addresses)
        addresses.add(address)
        addresses = list(addresses)
        addresses.sort()
        return AddressTable(self.individual_address, addresses, self.max_size)

    def append_multiple(self, new_addresses):
        if len(self._structure) >= self.max_size:
            raise AddressTableException("Max entries %d, already written inside address table" % self.max_size)
        addresses = set(self.addresses)
        addresses += new_addresses
        addresses = list(addresses)
        addresses.sort()
        return AddressTable(self.individual_address, addresses, self.max_size)

    def remove(self, address):
        addresses = self.addresses
        addresses.remove(address)
        return AddressTable(self.individual_address, addresses, self.max_size)
        
    def __repr__(self, *args, **kwargs):
        s = ("""AddressTable: max_size=%d, structure: %s\n\n\t""" % (self.max_size, self._structure))
        
        s += """address int -> hex conversion \n\t"""
        for address in self.addresses:
            s += """%d -> 0x%04X, \n\t""" % (address, address)
            
        return s


if __name__ == "__main__":
    import doctest
    doctest.testmod()

