from knx_stack.cemi import EMIId
from knx_stack.usb_hid import FeatureId


def receive(state, msg):
    (head, body) = msg.octect()
    (data, new_state) = (None, state)
    if head.value == FeatureId.busConnectionStatus:
        (head, _) = body.octect()
        if head.value == 0x00:
            data = "Disconnected"
        elif head.value == 0x01:
            data = "Connected"
    elif head.value == FeatureId.activeEMIType:
        (head, _) = body.octect()
        if head.value == EMIId.commonEmi:
            data = "cEMI"
        elif head.value == EMIId.emi1:
            data = "emi1"
        elif head.value == EMIId.emi2:
            data = "emi2"
    return data, new_state
