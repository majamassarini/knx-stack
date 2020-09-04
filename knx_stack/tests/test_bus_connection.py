import unittest
import knx_stack


class Test(unittest.TestCase):
    
    BUS_DISCONNECTED_MSG = "01130A000800020F0400000300"
    BUS_CONNECTED_MSG = "01130A000800020F0400000301"

    def testBusDisconnected(self):
        state = knx_stack.State(knx_stack.Medium.usb_hid, None, None)
        msg = knx_stack.Msg.make_from_str(self.BUS_DISCONNECTED_MSG)
        data = knx_stack.decode_msg(state, msg)
        self.assertTrue(len(data), 1)
        self.assertEqual(data[0].status, 'Disconnected')

    def testBusConnected(self):
        state = knx_stack.State(knx_stack.Medium.usb_hid, None, None)
        msg = knx_stack.Msg.make_from_str(self.BUS_CONNECTED_MSG)
        data = knx_stack.decode_msg(state, msg)
        self.assertTrue(len(data), 1)
        self.assertEqual(data[0].status, 'Connected')
