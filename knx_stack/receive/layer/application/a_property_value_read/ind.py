from collections import namedtuple

from knx_stack.receive.layer.application import a_property_value

Msg = namedtuple('PropertyValueReadInd', ['asap',
                                          'object_index',
                                          'property_id',
                                          'number_of_elements',
                                          'start_index'])


def receive(state, msg):
    (property_values, new_state) = a_property_value.receive(state, msg)
    property_values_read = [Msg(asap=property_value.asap,
                                object_index=property_value.object_index,
                                property_id=property_value.property_id,
                                number_of_elements=property_value.number_of_elements,
                                start_index=property_value.start_index)
                            for property_value in property_values]
    return property_values_read, new_state
