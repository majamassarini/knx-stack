from typing import Iterable
from knx_stack.definition.layer.application.a_group_value_response.ind import Msg
from knx_stack.decode.layer.application import a_group_value


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[Msg]:
    group_values = a_group_value.decode(state, msg)
    group_values_response = [Msg(asap=group_value.asap,
                                 dpt=group_value.dpt)
                             for group_value in group_values]
    return group_values_response
