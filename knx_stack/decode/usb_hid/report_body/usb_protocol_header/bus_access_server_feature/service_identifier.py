from typing import Iterable, NamedTuple
from knx_stack.definition.usb_hid import ServiceId
from knx_stack.decode.usb_hid.report_body.usb_protocol_header.bus_access_server_feature.device_feature_info import \
    feature_identifier


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    (head, msg) = msg.octect()
    result = []
    if head.value == ServiceId.DeviceFeatureInfo:
        (head, body) = msg.short()
        if head.value == 0x0000:
            result = feature_identifier.decode(state, body)
    if head.value == ServiceId.DeviceFeatureResponse:
        (head, body) = msg.short()
        if head.value == 0x0000:
            result = feature_identifier.decode(state, body)
    return result
