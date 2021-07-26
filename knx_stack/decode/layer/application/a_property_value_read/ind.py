from typing import Iterable
from knx_stack.definition.layer.application.a_property_value_read.ind import Msg
from knx_stack.decode.layer.application import a_property_value


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[Msg]:
    """
    >>> import knx_stack
    >>> asap = knx_stack.ASAP(0)
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(0x102C), [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, {})
    >>> state = knx_stack.State(knx_stack.Medium.usb_hid, association_table, knx_stack.GroupObjectTable())
    >>> ind = knx_stack.decode_msg(state, knx_stack.usb_hid.Msg.make_from_str("0113170008000F0103000029009660102C00000503D5007B1021"))
    >>> ind
    [PropertyValueReadInd (object index 0, property id 123, number of elements 1, start index 33 for asap 0)]
    """
    property_values = a_property_value.decode(state, msg)
    property_values_read = [Msg(asap=property_value.asap,
                                object_index=property_value.object_index,
                                property_id=property_value.property_id,
                                number_of_elements=property_value.number_of_elements,
                                start_index=property_value.start_index)
                            for property_value in property_values]
    return property_values_read
