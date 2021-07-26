from typing import Iterable
from knx_stack.definition.layer.application.a_group_value_write.con import Msg
from knx_stack.decode.layer.application import a_group_value


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[Msg]:
    """
    >>> import knx_stack
    >>> asap = knx_stack.ASAP(1, "example asap")
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(0x0001), [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, {})
    >>> association_table.associate(asap, [knx_stack.GroupAddress(0x0002)])
    >>> state = knx_stack.State(knx_stack.Medium.usb_hid, association_table,
    ...                         knx_stack.GroupObjectTable({asap: knx_stack.datapointtypes.DPT_Switch}))
    >>> con = knx_stack.decode_msg(state, knx_stack.usb_hid.Msg.make_from_str("0113130008000B010300002E0096E000000002010081"))
    >>> con
    [GroupValueWriteCon status 0 (DPT_Switch {'action': 'on'} for asap 1 (example asap))]
    """
    group_values = a_group_value.decode(state, msg)
    group_values_write = [Msg(asap=group_value.asap,
                              dpt=group_value.dpt,
                              status=state.ldata.status)
                          for group_value in group_values]
    return group_values_write
