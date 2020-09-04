from collections import namedtuple

import knx_stack.state
from knx_stack import Msg as KnxMsg, Octect, layer
from knx_stack.send.layer.transport.t_data_group import req


Msg = namedtuple('GroupValueReadReq', ['asap'])


def send(state, msg):
    """
    >>> import knx_stack
    >>> address_table = knx_stack.layer.AddressTable(0x0001, [], 255)
    >>> association_table = knx_stack.layer.AssociationTable(address_table, {})
    >>> new_association_table = association_table.associate(0x0002, 1)
    >>> state = knx_stack.State(knx_stack.Medium.usb_hid, new_association_table, {1: knx_stack.datapointtypes.DPT_Switch})
    >>> req_msg = Msg(asap=1)
    >>> (final_state, final_msg) = send(state, req_msg)
    >>> final_msg
    0113130008000B01030000110096E000000002010000
    """
    apci = 0
    state.apci = apci
    state.asap = msg.asap
    state.address_type = layer.AddressType.group
    ldata = layer.link.L_Data()
    ldata.apci = apci
    new_msg = KnxMsg([Octect(value=ldata.apci_value)])
    (final_state, final_msg) = req.send(state, new_msg)
    return final_state, final_msg
