from knx_stack.encode.layer.transport.t_data_group import req
from knx_stack.encode.layer.application.a_group_value_write.encode import al_encode


def encode(state: 'knx_stack.State', msg: 'knx_stack.layer.application.a_group_value_write.req.Msg') -> 'knx_stack.Msg':
    """
    >>> import knx_stack
    >>> asap = knx_stack.ASAP(1)
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(0x0001), [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, {})
    >>> association_table.associate(asap, [knx_stack.GroupAddress(0x0002)])
    >>> state = knx_stack.State(knx_stack.Medium.usb_hid, association_table,
    ...                         knx_stack.GroupObjectTable({asap: knx_stack.datapointtypes.DPT_Switch}))
    >>> switch = knx_stack.datapointtypes.DPT_Switch()
    >>> switch.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.on
    >>> req_msg = knx_stack.layer.application.a_group_value_write.req.Msg(asap=asap, dpt=switch)
    >>> req = knx_stack.encode_msg(state, req_msg)
    >>> req
    0113130008000B01030000110096E000000002010081
    """
    new_msg = al_encode(state, msg)
    final_msg = req.encode(state, new_msg)
    return final_msg
