from typing import NamedTuple, Iterable
from knx_stack.definition.layer.transport.association_table import ASAP
from knx_stack.definition.layer import PropertyServiceHeader


class PropertyData(NamedTuple):
    asap: 'knx_stack.ASAP'
    object_index: int
    property_id: int
    number_of_elements: int
    start_index: int
    data: int


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[PropertyData]:
    results = []
    propety_header, data = msg.long()
    header = PropertyServiceHeader()
    header.value = propety_header.value

    results.append(PropertyData(asap=ASAP(0),
                                object_index=header.bits.object_index,
                                property_id=header.bits.property_id,
                                number_of_elements=header.bits.number_of_elements,
                                start_index=header.bits.start_index,
                                data=data))
    return results
