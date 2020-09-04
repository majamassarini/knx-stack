from knx_stack import Msg as KnxMsg, Octect
from knx_stack.definition import layer
from knx_stack.encode.layer.transport.t_data_group import req


def encode(state: 'knx_stack.State', msg: 'knx_stack.layer.application.a_group_value_read.req.Msg') -> 'knx_stack.Msg':
    """
    >>> import knx_stack
    >>> asap = knx_stack.ASAP(1)
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(0x0001), [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, {})
    >>> association_table.associate(asap, [knx_stack.GroupAddress(free_style=0x0002)])
    >>> state = knx_stack.State(knx_stack.Medium.usb_hid, association_table,
    ...                         knx_stack.GroupObjectTable({asap: knx_stack.datapointtypes.DPT_Switch}))
    >>> req_msg = knx_stack.layer.application.a_group_value_read.req.Msg(asap=asap)
    >>> req = knx_stack.encode_msg(state, req_msg)
    >>> req
    0113130008000B01030000110096E000000002010000
    """
    apci = 0
    state.apci = apci
    state.asap = msg.asap
    state.address_type = layer.AddressType.group
    ldata = layer.link.L_Data()
    ldata.apci = apci
    new_msg = KnxMsg([Octect(value=ldata.apci_value)])
    final_msg = req.encode(state, new_msg)
    return final_msg
