import logging
from typing import Iterable, NamedTuple
from knx_stack.definition.knxnet_ip import HEADER_SIZE_10, KNXNETIP_VERSION_10, Services
from knx_stack.decode.knxnet_ip import core, tunneling


def decode(state: 'knx_stack.State', msg: 'knx_stack.Msg') -> Iterable[NamedTuple]:
    """
    >>> import knx_stack
    >>> individual_address = knx_stack.Address(0x0001)
    >>> group_address = knx_stack.GroupAddress(free_style=0xABCD)
    >>> asap = knx_stack.ASAP(1, "an application service access point to 0xABCD")
    >>> address_table = knx_stack.AddressTable(individual_address, [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, [])
    >>> association_table.associate(asap, [group_address])
    >>> group_object_table = knx_stack.GroupObjectTable({asap: knx_stack.datapointtypes.DPT_Switch})
    >>> state = knx_stack.State(knx_stack.state.Medium.knxnet_ip, association_table, group_object_table)
    >>> state.sequence_counter_remote = 1
    >>> msg = knx_stack.knxnet_ip.Msg.make_from_str("061004200015047401002900BCE00001ABCD010080")
    >>> data = knx_stack.decode_msg(state, msg)
    >>> data
    [TunnelingReq(sequence_counter=1, status=<ErrorCodes.E_NO_ERROR: 0>), GroupValueWriteInd (DPT_Switch {'action': 'off'} for asap 1 (an application service access point to 0xABCD))]
    """
    (header, body) = msg.octect()
    (version, body) = body.octect()
    (service, body) = body.short()
    result = []
    if header.value == HEADER_SIZE_10 and version.value == KNXNETIP_VERSION_10:
        if service.value == Services.SEARCH_RESPONSE:
            result = core.search.res.decode(state, body)
        elif service.value == Services.DISCONNECT_RESPONSE:
            result = core.disconnect.res.decode(state, body)
        elif service.value == Services.CONNECT_RESPONSE:
            result = core.connect.res.decode(state, body)
        elif service.value == Services.CONNECTIONSTATE_RESPONSE:
            result = core.connectionstate.res.decode(state, body)
        elif service.value == Services.TUNNELING_REQUEST:
            result = tunneling.req.decode(state, body)
        elif service.value == Services.TUNNELING_ACK:
            result = tunneling.ack.decode(state, body)
        else:
            logging.getLogger(__name__).error("Unknown knxnet_ip service value %d" % service.value)
    return result
