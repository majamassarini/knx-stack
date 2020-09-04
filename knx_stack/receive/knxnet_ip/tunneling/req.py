import logging
from collections import namedtuple
from knx_stack import LOGGER_NAME
from knx_stack.receive import cemi
from knx_stack.knxnet_ip import ErrorCodes

Msg = namedtuple('TunnelingReq', [ 'sequence_counter', 'status'])


def receive(state, msg):
    """
    >>> import knx_stack
    >>> address_table = knx_stack.layer.AddressTable(0x0001, [], 255)
    >>> association_table = knx_stack.layer.AssociationTable(address_table, {})
    >>> new_association_table = association_table.associate(0x0C82, 1)
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.usb_hid, new_association_table, {1: knx_stack.datapointtypes.DPT_Switch})
    >>> state.sequence_counter_remote = 1
    >>> example = knx_stack.knxnet_ip.Msg.stringtooctects("0019047401002900b4e011010c82050080589f8037")
    >>> res, state = receive(state, knx_stack.knxnet_ip.Msg(example))
    >>> res
    [TunnelingReq(sequence_counter=1, status=<ErrorCodes.E_NO_ERROR: 0>), GroupValueWriteInd(asap=1, dpt=DPT_Switch: {'action': 'on'})]
    """
    data = []
    (size, body) = msg.short()
    (communication_channel_id, sequence_counter, _, body) = body.header()
    logging.getLogger(LOGGER_NAME).info("knxnet_ip.tunneling.receive.req sequence counter={}".format(sequence_counter))
    if state.sequence_counter_remote == sequence_counter:
        data.append(Msg(sequence_counter=sequence_counter, status=ErrorCodes.E_NO_ERROR))
        data_tmp, state = cemi.msg_code.receive(state, body)
        if data_tmp:
            data.extend(data_tmp)
    else:
        if state.sequence_counter_remote == (sequence_counter + 1):
            data.append(Msg(sequence_counter=sequence_counter, status=ErrorCodes.E_NO_ERROR))
        else:
            data.append(Msg(sequence_counter=sequence_counter, status=ErrorCodes.E_SEQUENCE_NUMBER))

    return data, state
