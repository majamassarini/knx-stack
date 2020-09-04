from knx_stack.usb_hid import ProtocolId
from knx_stack.receive.cemi import emi_id
from knx_stack.receive.usb_hid.report_body.usb_protocol_header.bus_access_server_feature import service_identifier


def receive(state, msg):
    (head, body) = msg.octect()
    (data, new_state) = (None, state)
    if head.value == ProtocolId.KNXTunnel:
        (data, new_state) = emi_id.receive(state, body)
    elif head.value == ProtocolId.BusAccessServerFeatureService:
        (data, new_state) = service_identifier.receive(state, body)
    return data, new_state
