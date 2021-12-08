import unittest
import doctest
import knx_stack


tests = list()
tests.append(doctest.DocTestSuite(knx_stack.datapointtypes))
tests.append(doctest.DocTestSuite(knx_stack.layer.link.ldata))
tests.append(doctest.DocTestSuite(knx_stack.layer.network.address_table))
tests.append(doctest.DocTestSuite(knx_stack.layer.transport.association_table))
tests.append(doctest.DocTestSuite(knx_stack.layer.application.groupobject_table))
tests.append(doctest.DocTestSuite(knx_stack.layer.application.a_property_value))
tests.append(doctest.DocTestSuite(knx_stack.msg))
tests.append(doctest.DocTestSuite(knx_stack.state))
tests.append(doctest.DocTestSuite(knx_stack.address))
tests.append(
    doctest.DocTestSuite(knx_stack.encode.layer.application.a_group_value_read.req)
)
tests.append(
    doctest.DocTestSuite(knx_stack.encode.layer.application.a_group_value_write.req)
)
tests.append(
    doctest.DocTestSuite(knx_stack.encode.layer.application.a_property_value_read.req)
)
tests.append(
    doctest.DocTestSuite(knx_stack.encode.layer.application.a_property_value_write.req)
)
tests.append(doctest.DocTestSuite(knx_stack.encode.layer.transport.t_connect.req))
tests.append(
    doctest.DocTestSuite(knx_stack.decode.usb_hid.report_header.report_identifier)
)
tests.append(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.core.connect.req))
tests.append(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.core.disconnect.req))
tests.append(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.core.connectionstate.req))
tests.append(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.core.search.req))
tests.append(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.tunneling.req))
tests.append(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.tunneling.ack))
tests.append(doctest.DocTestSuite(knx_stack.encode.knxnet_ip.header))
tests.append(
    doctest.DocTestSuite(knx_stack.decode.layer.application.a_group_value_read.ind)
)
tests.append(
    doctest.DocTestSuite(knx_stack.decode.layer.application.a_group_value_read.con)
)
tests.append(
    doctest.DocTestSuite(knx_stack.decode.layer.application.a_group_value_write.ind)
)
tests.append(
    doctest.DocTestSuite(knx_stack.decode.layer.application.a_group_value_write.con)
)
tests.append(
    doctest.DocTestSuite(knx_stack.decode.layer.application.a_property_value_read.ind)
)
tests.append(
    doctest.DocTestSuite(knx_stack.decode.layer.application.a_property_value_read.con)
)
tests.append(
    doctest.DocTestSuite(knx_stack.decode.layer.application.a_property_value_write.ind)
)
tests.append(
    doctest.DocTestSuite(knx_stack.decode.layer.application.a_property_value_write.con)
)
tests.append(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.core.search.res))
tests.append(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.core.connect.res))
tests.append(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.core.disconnect.res))
tests.append(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.core.connectionstate.res))
tests.append(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.tunneling.req))
tests.append(doctest.DocTestSuite(knx_stack.decode.knxnet_ip.tunneling.ack))

# tests.append(doctest.DocFileSuite('../docs/source/intro.rst', package=knx_stack))


def load_tests(loader, suite, ignore):
    for test in tests:
        suite.addTests(test)
    return suite


suite = unittest.TestSuite()
[suite.addTests(test) for test in tests]
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
