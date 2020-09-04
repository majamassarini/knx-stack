import knx_stack.state
from knx_stack import Msg, Octect
from knx_stack.definition import layer
from knx_stack.encode.layer.network.n_data_individual import req


def encode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> 'knx_stack.Msg':
    """
    >>> import knx_stack
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(0x1001), [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, [])
    >>> state = knx_stack.state.State(knx_stack.state.Medium.usb_hid, association_table, None)
    >>> final_msg = encode(state, knx_stack.Msg([]))
    >>> final_msg
    0113120008000A0103000011009660000010010080
    """
    state.address_type = layer.AddressType.individual
    ldata = layer.L_Data()
    ldata.nsdu = layer.NSDU.T_Data_Individual_PDU
    ldata.connected = True
    new_msg = Msg([Octect(value=ldata.tpci)])
    final_msg = req.encode(state, new_msg)
    return final_msg
