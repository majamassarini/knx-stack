from collections import namedtuple

from knx_stack.receive.layer.application import a_group_value

Msg = namedtuple('GroupValueResponseInd', ['asap', 'dpt'])


def receive(state, msg):
    (group_values, new_state) = a_group_value.receive(state, msg)
    group_values_response = [Msg(asap=group_value.asap,
                                 dpt=group_value.dpt)
                             for group_value in group_values]
    return group_values_response, new_state
