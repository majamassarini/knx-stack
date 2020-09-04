import logging
from typing import Iterable
from knx_stack.decode import cemi
from knx_stack.definition.knxnet_ip import ErrorCodes
from knx_stack.definition.knxnet_ip.tunneling.req import Msg


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[Msg]:
    """
    >>> import knx_stack
    >>> asap = knx_stack.ASAP(1)
    >>> address_table = knx_stack.AddressTable(knx_stack.Address(0x0001), [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, [])
    >>> association_table.associate(asap, [knx_stack.GroupAddress(free_style=0x0C82)])
    >>> state = knx_stack.knxnet_ip.State(knx_stack.Medium.knxnet_ip, association_table,
    ...                                   knx_stack.GroupObjectTable({asap: knx_stack.datapointtypes.DPT_Switch}))
    >>> state.sequence_counter_remote = 1
    >>> example = knx_stack.knxnet_ip.Msg.make_from_str("0019047401002900b4e011010c82050080589f8037")
    >>> req = knx_stack.decode.knxnet_ip.tunneling.req.decode(state, example)
    >>> req
    [TunnelingReq(sequence counter=1, status=<ErrorCodes.E_NO_ERROR: 0>), GroupValueWriteInd (DPT_Switch {'action': 'on'} for asap 1)]
    """
    result = []
    (size, body) = msg.short()
    (communication_channel_id, sequence_counter, _, body) = body.header()
    logging.getLogger(__name__).debug("knxnet_ip.tunneling.decode.req sequence counter={}".format(sequence_counter))
    if state.sequence_counter_remote == sequence_counter:
        result.append(Msg(sequence_counter=sequence_counter, status=ErrorCodes.E_NO_ERROR))
        result_tmp = cemi.msg_code.decode(state, body)
        if result_tmp:
            result.extend(result_tmp)
    else:
        if state.sequence_counter_remote == (sequence_counter + 1):
            result.append(Msg(sequence_counter=sequence_counter, status=ErrorCodes.E_NO_ERROR))
        else:
            result.append(Msg(sequence_counter=sequence_counter, status=ErrorCodes.E_SEQUENCE_NUMBER))

    return result
