from knx_stack import Msg as KnxMsg, Octect, Long
from knx_stack.definition import layer
from knx_stack.encode.layer.transport.t_data_individual import req


def encode(state: 'knx_stack.State',
           msg: 'knx_stack.layer.application.a_property_value_write.req.Msg') -> 'knx_stack.Msg':
    """
    >>> import knx_stack
    >>> asap = knx_stack.ASAP(0)
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(0x102C), [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, {})
    >>> state = knx_stack.State(knx_stack.Medium.usb_hid, association_table, knx_stack.GroupObjectTable())
    >>> req_msg = knx_stack.layer.application.a_property_value_write.req.Msg(asap=asap, object_index=0, property_id=0x7B,
    ...                                                                      number_of_elements=1, start_index=0x21,
    ...                                                                      data='FF')
    >>> req = knx_stack.encode_msg(state, req_msg)
    >>> req
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
    final_msg = req.encode(state, new_msg)
    return final_msg
