from typing import Iterable, NamedTuple
from knx_stack.definition.cemi import EMIId
from knx_stack.decode.cemi import msg_code


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    result = []
    (head, msg) = msg.octect()
    if head.value == EMIId.commonEmi:
        (head, body) = msg.short()
        if head.value == 0x0000:
            result = msg_code.decode(state, body)
    return result
