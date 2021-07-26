from typing import Iterable
from knx_stack.definition.layer.application.a_group_value_read.ind import Msg
from knx_stack.decode.layer.application import a_group_value


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[Msg]:
    """
    >>> import knx_stack
    >>> asap = knx_stack.ASAP(1)
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(0x0001), [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, {})
    >>> association_table.associate(asap, [knx_stack.GroupAddress(free_style=0x0002)])
    >>> state = knx_stack.State(knx_stack.Medium.usb_hid, association_table,
    ...                         knx_stack.GroupObjectTable({asap: knx_stack.datapointtypes.DPT_Switch}))
    >>> ind = knx_stack.decode_msg(state, knx_stack.usb_hid.Msg.make_from_str("0113130008000B01030000290096E000000002010000"))
    >>> ind
    [GroupValueReadInd (DPT_Switch {'action': 'off'} for asap 1)]
    """
    group_values = a_group_value.decode(state, msg)
    group_values_read = [Msg(asap=group_value.asap,
                             dpt=group_value.dpt)
                         for group_value in group_values]
    return group_values_read
