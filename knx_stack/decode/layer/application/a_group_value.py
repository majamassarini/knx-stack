from typing import NamedTuple, Iterable


class GroupData(NamedTuple):
    asap: 'knx_stack.ASAP'
    dpt: 'knx_stack.datapointtypes.DPT'


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[GroupData]:
    associations = []
    for asap, dpt in state.get_asaps_and_dpts():
        data = dpt()
        value = 0
        (head, body) = msg.octect()
        while body:
            value <<= 8
            value += head.value
            (head, body) = body.octect()
        value <<= 8
        value += head.value
        data.value = value
        associations.append(GroupData(asap=asap, dpt=data))
    return associations
