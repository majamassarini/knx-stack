from knx_stack.cemi import EMIId
from knx_stack.receive.cemi import msg_code


def receive(state, msg):
    (data, new_state) = (None, state)
    (head, msg) = msg.octect()
    if head.value == EMIId.commonEmi:
        (head, body) = msg.short()
        if head.value == 0x0000:
            (data, new_state) = msg_code.receive(state, body)
    return data, new_state
