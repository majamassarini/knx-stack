import knx_stack.state
from knx_stack import Msg, Octect
from knx_stack.definition import layer
from knx_stack.encode.layer.network.n_data_individual import req


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    """
    >>> import knx_stack
    >>> address_table = knx_stack.AddressTable(0x1001, [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, [])
    >>> state = knx_stack.State(knx_stack.state.Medium.usb_hid,association_table,None)
    >>> (final_state, final_msg) = encode(state, Msg([]))
    >>> final_msg
    0113120008000A0103000011008660000010010081
    """
    state.address_type = layer.AddressType.individual
    ldata = layer.L_Data()
    ldata.nsdu = layer.NSDU.T_Data_Individual_PDU
    ldata.connected = True
    ldata.apci = 0x100
    new_msg = Msg([Octect(value=ldata.tpci)])
    final_msg = req.encode(state, new_msg)
    return final_msg
