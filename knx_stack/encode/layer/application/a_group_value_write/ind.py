from knx_stack.encode.layer.transport.t_data_group import ind
from knx_stack.encode.layer.application.a_group_value_write.encode import al_encode


def encode(state: 'knx_stack.State', msg: 'knx_stack.layer.application.a_group_value_write.ind.Msg') -> 'knx_stack.Msg':
    """
    >>> import knx_stack
    >>> address_table = knx_stack.AddressTable(0x0001, [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, {})
    >>> new_association_table = association_table.associate(0x0002, 1)
    >>> state = knx_stack.State(knx_stack.Medium.usb_hid, new_association_table, {1: knx_stack.datapointtypes.DPT_Switch})
    >>> switch = knx_stack.datapointtypes.DPT_Switch()
    >>> switch.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.on
    >>> ind_msg = knx_stack.layer.application.a_group_value_write.ind.Msg(asap=1, dpt=switch)
    >>> ind = encode(state, ind_msg)
    >>> ind
    0113130008000B01030000290096E000000002010081
    """
    new_msg = al_encode(state, msg)
    final_msg = ind.encode(state, new_msg)
    return final_msg
