import logging
from typing import Iterable
from knx_stack.definition.knxnet_ip.tunneling.ack import Msg
from knx_stack.definition.knxnet_ip import ErrorCodes


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[Msg]:
    """
    >>> import knx_stack
    >>> address_table = knx_stack.AddressTable(0x0001, [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, {})
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.usb_hid, association_table, {})
    >>> example = knx_stack.knxnet_ip.Msg.make_from_str("000a044c0000")
    >>> res, state = knx_stack.decode.knxnet_ip.tunneling.ack.decode(state, example)
    >>> res
    [TunnelingAck(sequence counter=1, status=0)]
    """
    (size, body) = msg.short()
    (communication_channel_id, sequence_counter, status, body) = body.header()
    if state.sequence_counter_local == sequence_counter:
        state.sequence_counter_local += 1
    logging.getLogger(__name__).info("knxnet_ip.tunneling.decode.req sequence counter={}".format(sequence_counter))
    return [Msg(sequence_counter=state.sequence_counter_local, status=ErrorCodes(status))], state
