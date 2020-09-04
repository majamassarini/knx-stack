from knx_stack.msg import Msg, Octect, Long, Short, Nibbles
from knx_stack.address import Address, GroupAddress, ThreeLevelStyle, TwoLevelStyle
from knx_stack.state import State, Medium
from knx_stack import datapointtypes
from knx_stack import address
from knx_stack.definition import knxnet_ip, usb_hid, layer, cemi
from knx_stack.definition.layer.network import AddressTable
from knx_stack.definition.layer.transport import ASAP, Association, AssociationTable
from knx_stack.definition.layer.application import GroupObjectTable
from knx_stack import encode
from knx_stack import decode
from knx_stack.decode.usb_hid.report_header.report_identifier import decode as usb_hid_decode
from knx_stack.decode.knxnet_ip.header import decode as knxnet_ip_decode
from knx_stack import client


encode_mapping = {
    knxnet_ip.core.connect.req.Msg: encode.knxnet_ip.core.connect.req.encode,
    knxnet_ip.core.disconnect.req.Msg: encode.knxnet_ip.core.disconnect.req.encode,
    knxnet_ip.core.connectionstate.req.Msg: encode.knxnet_ip.core.connectionstate.req.encode,
    knxnet_ip.core.search.req.Msg: encode.knxnet_ip.core.search.req.encode,
    knxnet_ip.tunneling.ack.Msg: encode.knxnet_ip.tunneling.ack.encode,
    layer.application.a_group_value_read.req.Msg: encode.layer.application.a_group_value_read.req.encode,
    layer.application.a_group_value_write.req.Msg: encode.layer.application.a_group_value_write.req.encode,
    layer.application.a_group_value_write.ind.Msg: encode.layer.application.a_group_value_write.ind.encode,
    layer.application.a_property_value_read.req.Msg: encode.layer.application.a_property_value_read.req.encode,
    layer.application.a_property_value_write.req.Msg: encode.layer.application.a_property_value_write.req.encode,
}


def encode_msg(state_, msg_):
    return encode_mapping[msg_.__class__](state_, msg_)


def decode_msg(state_, msg_):
    if state_.medium == Medium.usb_hid:
        return decode.usb_hid.report_header.report_identifier.decode(state_, msg_)
    elif state_.medium == Medium.knxnet_ip:
        return decode.knxnet_ip.header.decode(state_, msg_)
    else:
        raise Exception("Not supported medium")


