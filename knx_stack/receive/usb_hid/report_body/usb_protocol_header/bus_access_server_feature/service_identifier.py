from knx_stack.usb_hid import ServiceId
from knx_stack.receive.usb_hid.report_body.usb_protocol_header.bus_access_server_feature.device_feature_info import \
    feature_identifier


def receive(state, msg):
    (head, msg) = msg.octect()
    (data, new_state) = (None, state)
    if head.value == ServiceId.DeviceFeatureInfo:
        (head, body) = msg.short()
        if head.value == 0x0000:
            (data, new_state) = feature_identifier.receive(state, body)
    if head.value == ServiceId.DeviceFeatureResponse:
        (head, body) = msg.short()
        if head.value == 0x0000:
            (data, new_state) = feature_identifier.receive(state, body)
    
    return (data, new_state)