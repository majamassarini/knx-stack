import unittest
import knx_stack


class Test(unittest.TestCase):
    
    BUS_DISCONNECTED_MSG = "01130A000800020F0400000300"
    BUS_CONNECTED_MSG = "01130A000800020F0400000301"

    def testBusDisconnected(self):
        state = []
        octects = knx_stack.Msg.stringtooctects(self.BUS_DISCONNECTED_MSG)
        msg = knx_stack.Msg(octects)
        data, new_state = knx_stack.receive.usb_hid.receive(state, msg)
        self.assertEqual(data, "Disconnected")
    
    def testBusConnected(self):
        state = []
        octects = knx_stack.Msg.stringtooctects(self.BUS_CONNECTED_MSG)
        msg = knx_stack.Msg(octects)
        data, new_state = knx_stack.receive.usb_hid.receive(state, msg)
        self.assertEqual(data, "Connected")


if __name__ == "__main__":
    unittest.main()