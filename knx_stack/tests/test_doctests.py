import unittest
import doctest
import knx_stack


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(knx_stack.datapointtypes))
    tests.addTests(doctest.DocTestSuite(knx_stack.msg))
    tests.addTests(doctest.DocTestSuite(knx_stack.state))

    tests.addTests(doctest.DocTestSuite(knx_stack.send.layer.application.a_group_value_read.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.send.layer.application.a_group_value_write.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.send.layer.application.a_property_value_read.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.send.layer.application.a_property_value_write.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.send.layer.transport.t_connect.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.send.knxnet_ip.core.connect.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.send.knxnet_ip.core.disconnect.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.send.knxnet_ip.core.connectionstate.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.send.knxnet_ip.core.search.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.send.knxnet_ip.tunneling.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.send.knxnet_ip.tunneling.ack))

    tests.addTests(doctest.DocTestSuite(knx_stack.receive.knxnet_ip.core.search.res))
    tests.addTests(doctest.DocTestSuite(knx_stack.receive.knxnet_ip.core.connect.res))
    tests.addTests(doctest.DocTestSuite(knx_stack.receive.knxnet_ip.core.disconnect.res))
    tests.addTests(doctest.DocTestSuite(knx_stack.receive.knxnet_ip.core.connectionstate.res))
    tests.addTests(doctest.DocTestSuite(knx_stack.receive.knxnet_ip.tunneling.req))
    tests.addTests(doctest.DocTestSuite(knx_stack.receive.knxnet_ip.tunneling.ack))

    return tests