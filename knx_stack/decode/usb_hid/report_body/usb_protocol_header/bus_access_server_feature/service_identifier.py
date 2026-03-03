from __future__ import annotations
from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple
from knx_stack.definition.usb_hid import ServiceId
from knx_stack.decode.usb_hid.report_body.usb_protocol_header.bus_access_server_feature.device_feature_info import (
    feature_identifier,
)

if TYPE_CHECKING:
    import knx_stack


def decode(state: knx_stack.State, msg: knx_stack.Msg) -> Iterable[NamedTuple]:
    """Decode the USB HID bus access server feature service identifier from raw message bytes.

    Reads the service ID byte and, for DeviceFeatureInfo or DeviceFeatureResponse
    services, delegates to the feature_identifier decoder.
    """
    (head, msg) = msg.octect()
    result: Iterable[NamedTuple] = []
    if head.value == ServiceId.DeviceFeatureInfo:
        (head, body) = msg.short()  # type: ignore[assignment]
        if head.value == 0x0000:
            result = feature_identifier.decode(state, body)
    if head.value == ServiceId.DeviceFeatureResponse:
        (head, body) = msg.short()  # type: ignore[assignment]
        if head.value == 0x0000:
            result = feature_identifier.decode(state, body)
    return result
