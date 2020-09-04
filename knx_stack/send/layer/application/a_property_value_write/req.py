from collections import namedtuple

import knx_stack.state
from knx_stack import Msg as KnxMsg, Octect, Long, layer
from knx_stack.send.layer.transport.t_data_individual import req

Msg = namedtuple('PropertyValueWriteReq', ['asap',
                                           'object_index',
                                           'property_id',
                                           'number_of_elements',
                                           'start_index',
                                           'data'])


def send(state, msg):
    """
    >>> import knx_stack
    >>> address_table = knx_stack.layer.AddressTable(0x102C, [], 255)
    >>> association_table = knx_stack.layer.AssociationTable(address_table, {})
    >>> state = knx_stack.State(knx_stack.Medium.usb_hid, association_table, {})
    >>> req_msg = Msg(asap=0, object_index=0, property_id=0x7B, number_of_elements=1, start_index=0x21, data='FF')
    >>> (final_state, final_msg) = send(state, req_msg)
    >>> final_msg
    0113180008001001030000110096600000102C0603D7007B1021FF
    """
    apci = 0x3D7
    state.asap = msg.asap
    state.apci = apci
    state.address_type = layer.AddressType.individual
    ldata = layer.L_Data()
    ldata.apci = apci
    header = layer.PropertyServiceHeader()
    header.bits.object_index = msg.object_index
    header.bits.property_id = msg.property_id
    header.bits.number_of_elements = msg.number_of_elements
    header.bits.start_index = msg.start_index
    along = Long()
    along.value = header.value
    new_msg = KnxMsg([Octect(value=ldata.apci)] + along.octects + KnxMsg.stringtooctects(msg.data))
    (state, final_msg) = req.send(state, new_msg)
    return state, final_msg
