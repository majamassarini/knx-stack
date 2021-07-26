import unittest
import doctest
import knx_stack


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(knx_stack.datapointtypes))
    tests.addTests(doctest.DocTestSuite(knx_stack.layer.link.ldata))
    tests.addTests(doctest.DocTestSuite(knx_stack.layer.network.address_table))
    tests.addTests(doctest.DocTestSuite(knx_stack.layer.transport.association_table))
    tests.addTests(doctest.DocTestSuite(knx_stack.layer.application.groupobject_table))
    tests.addTests(doctest.DocTestSuite(knx_stack.layer.application.a_property_value))
    tests.addTests(doctest.DocTestSuite(knx_stack.msg))
    tests.addTests(doctest.DocTestSuite(knx_stack.state))
    tests.addTests(doctest.DocTestSuite(knx_stack.address))

    tests.addTests(doctest.DocTestSuite(knx_stack.encode.layer.application.a_group_value_read.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.encode.layer.application.a_group_value_write.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.encode.layer.application.a_property_value_read.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.encode.layer.application.a_property_value_write.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.encode.layer.transport.t_connect.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.usb_hid.report_header.report_identifier))
    tests.addTests(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.core.connect.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.core.disconnect.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.core.connectionstate.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.core.search.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.tunneling.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.tunneling.ack))
    tests.addTests(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.header))

    tests.addTests(doctest.DocTestSuite(knx_stack.decode.layer.application.a_group_value_read.ind))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.layer.application.a_group_value_read.con))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.layer.application.a_group_value_write.ind))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.layer.application.a_group_value_write.con))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.layer.application.a_property_value_read.ind))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.layer.application.a_property_value_read.con))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.layer.application.a_property_value_write.ind))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.layer.application.a_property_value_write.con))

    tests.addTests(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.core.search.res))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.core.connect.res))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.core.disconnect.res))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.core.connectionstate.res))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.tunneling.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.tunneling.ack))

    return tests