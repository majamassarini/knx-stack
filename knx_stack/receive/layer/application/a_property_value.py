from collections import namedtuple
from knx_stack.layer import PropertyServiceHeader

PropertyData = namedtuple('PropertyData', ['asap',
                                           'object_index',
                                           'property_id',
                                           'number_of_elements',
                                           'start_index',
                                           'data'])


def receive(state, msg):
    (head, body) = msg.octect()
    msgs = []
    propety_header, data = body.long()
    header = PropertyServiceHeader()
    header.value = propety_header.value

    msgs.append(PropertyData(asap=0,
                             object_index=header.bits.object_index,
                             property_id=header.bits.property_id,
                             number_of_elements=header.bits.number_of_elements,
                             start_index=header.bits.start_index,
                             data=data))
    return msgs, state
