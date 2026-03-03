from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.definition.cemi import EMIId
from knx_stack.definition.usb_hid import FeatureId

if TYPE_CHECKING:
    import knx_stack


class ConnectionStatus(NamedTuple):
    status: str


class EMIType(NamedTuple):
    type: str


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    """Decode the USB HID bus access server feature identifier from raw message bytes.

    Reads the feature ID byte and returns a named tuple describing the connection
    status or the active EMI type, depending on the feature reported.
    """
    head, body = msg.octect()
    result: Iterable[NamedTuple] = []
    if head.value == FeatureId.busConnectionStatus:
        head, _ = body.octect()
        if head.value == 0x00:
            result = [ConnectionStatus(status="Disconnected")]
        elif head.value == 0x01:
            result = [ConnectionStatus(status="Connected")]
    elif head.value == FeatureId.activeEMIType:
        head, _ = body.octect()
        if head.value == EMIId.commonEmi:
            result = [EMIType(type="cEMI")]
        elif head.value == EMIId.emi1:
            result = [EMIType(type="emi1")]
        elif head.value == EMIId.emi2:
            result = [EMIType(type="emi2")]
    return result
