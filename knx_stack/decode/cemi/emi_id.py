from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.definition.cemi import EMIId
from knx_stack.decode.cemi import msg_code

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    result: Iterable[NamedTuple] = []
    (head, msg) = msg.octect()
    if head.value == EMIId.commonEmi:
        (head, body) = msg.short()  # type: ignore[assignment]
        if head.value == 0x0000:
            result = msg_code.decode(state, body)
    return result
