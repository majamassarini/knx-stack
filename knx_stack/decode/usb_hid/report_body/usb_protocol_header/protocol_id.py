from typing import Iterable, NamedTuple
from knx_stack.definition.usb_hid import ProtocolId
from knx_stack.decode.cemi import emi_id
from knx_stack.decode.usb_hid.report_body.usb_protocol_header.bus_access_server_feature import service_identifier


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    (head, body) = msg.octect()
    result = []
    if head.value == ProtocolId.KNXTunnel:
        result = emi_id.decode(state, body)
    elif head.value == ProtocolId.BusAccessServerFeatureService:
        result = service_identifier.decode(state, body)
    return result
