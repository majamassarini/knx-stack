from collections import namedtuple

GroupData = namedtuple('GroupData', ['asap', 'dpt'])


def receive(state, msg):
    dpts = []
    for asap, dpt in state.get_asaps_and_dpts():
        data = dpt()
        value = 0
        (head, body) = msg.octect()
        while body:
            value <<= 8
            value += head.value
            (head, body) = body.octect()
        value <<= 8
        value += head.value
        data.value = value
        dpts.append(GroupData(asap=asap, dpt=data))
    return dpts, state
