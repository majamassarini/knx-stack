from typing import Iterable, NamedTuple
from knx_stack.definition.usb_hid import KNX_DATA_EXCHANGE
from knx_stack.decode.usb_hid.report_header import packet_info


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    """
    >>> import knx_stack
    >>> individual_address = knx_stack.Address(0x0001)
    >>> address_table = knx_stack.AddressTable(individual_address, [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, [])
    >>> group_object_table = knx_stack.GroupObjectTable()
    >>> state = knx_stack.State(knx_stack.state.Medium.usb_hid, association_table, group_object_table)
    >>> msg = knx_stack.Msg.make_from_str("0113130008000B010300002900BCE00001ABCC010081")
    >>> data = knx_stack.decode_msg(state, msg)
    >>> data
    []
    """
    (head, body) = msg.octect()
    result = []
    if head.value == KNX_DATA_EXCHANGE:
        result = packet_info.decode(state, body)
    return result
