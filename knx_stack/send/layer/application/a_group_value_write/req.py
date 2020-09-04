from knx_stack.send.layer.transport.t_data_group import req
from knx_stack.send.layer.application.a_group_value_write.send import al_send


class Msg(object):
    
    def __init__(self, asap, dpt):
        self._asap = asap
        self._dpt = dpt
    
    @property
    def asap(self):
        return self._asap
    
    @property
    def dpt(self):
        return self._dpt
    
    def __repr__(self, *args, **kwargs):
        s = "asap: %s, dpt_name: %s, dpt_value: %s" % (self._asap, str(self._dpt.__class__), str(self._dpt.value))
        return s


def send(state, msg):
    """
    >>> import knx_stack
    >>> address_table = knx_stack.layer.AddressTable(0x0001, [], 255)
    >>> association_table = knx_stack.layer.AssociationTable(address_table, {})
    >>> new_association_table = association_table.associate(0x0002, 1)
    >>> state = knx_stack.State(knx_stack.Medium.usb_hid, new_association_table, {1: knx_stack.datapointtypes.DPT_Switch})
    >>> switch = knx_stack.datapointtypes.DPT_Switch()
    >>> switch.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.on
    >>> req_msg = Msg(asap=1, dpt=switch)
    >>> (final_state, final_msg) = send(state, req_msg)
    >>> final_msg
    0113130008000B01030000110096E000000002010081
    """
    (new_state, new_msg) = al_send(state, msg)
    (final_state, final_msg) = req.send(new_state, new_msg)
    return final_state, final_msg
