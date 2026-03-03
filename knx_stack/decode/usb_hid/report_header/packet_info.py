from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack import Msg
from knx_stack.definition.usb_hid import PacketType
from knx_stack.decode.usb_hid.report_body.usb_protocol_header import (
    protocol_version,
)

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    (packet_info_byte, body) = msg.octect()
    packet_type = packet_info_byte.nibble.low
    result: Iterable[NamedTuple] = []

    if packet_type == PacketType.allInOnePacket:
        (data_length, body) = body.octect()
        result = protocol_version.decode(
            state, Msg(body[0 : data_length.value])
        )
    else:
        _sequence_number = packet_info_byte.nibble.high  # noqa

    return result
