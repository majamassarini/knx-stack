import logging
from knx_stack import LOGGER_NAME
from collections import namedtuple


Msg = namedtuple('ConnectionstateRes', ['status'])


def receive(state, msg):
    """
    >>> import knx_stack
    >>> address_table = knx_stack.layer.AddressTable(0x0001, [], 255)
    >>> association_table = knx_stack.layer.AssociationTable(address_table, {})
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.usb_hid, association_table, {})
    >>> example = knx_stack.knxnet_ip.Msg.stringtooctects("000a044c0000")
    >>> res, state = receive(state, knx_stack.knxnet_ip.Msg(example))
    >>> res
    [ConnectionstateRes(status=0)]
    """
    (size, body) = msg.short()
    (communication_channel_id, sequence_counter, status, body) = body.header()
    if state.sequence_counter_local == sequence_counter:
        state.sequence_counter_local += 1
    logging.getLogger(LOGGER_NAME).info("knxnet_ip.tunneling.receive.req sequence counter={}".format(sequence_counter))
    return [Msg(status=status)], state
