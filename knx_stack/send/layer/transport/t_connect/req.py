import knx_stack.state
from knx_stack import Msg, Octect, layer
from knx_stack.send.layer.network.n_data_individual import req


def send(state, msg):
    """
import knx_stack.state    >>> import knx_stack
    >>> address_table = knx_stack.layer.AddressTable(0x1001, [], 255)
    >>> association_table = knx_stack.layer.AssociationTable(address_table, [])
    >>> state = knx_stack.state.State(knx_stack.state.Medium.usb_hid, association_table, None)
    >>> (final_state, final_msg) = send(state, knx_stack.Msg([]))
    >>> final_msg
    0113120008000A0103000011009660000010010080
    """
    state.address_type = layer.AddressType.individual
    ldata = layer.L_Data()
    ldata.nsdu = layer.NSDU.T_Data_Individual_PDU
    ldata.connected = True
    new_msg = Msg([Octect(value=ldata.tpci)])
    (state, final_msg) = req.send(state, new_msg)
    return state, final_msg
