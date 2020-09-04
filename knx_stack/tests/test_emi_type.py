import unittest
import knx_stack


class Test(unittest.TestCase):
    
    COMMON_EMI_ACTIVE_MSG = "01130A000800020F0200000503"
    EMI_2_ACTIVE_MSG = "01130A000800020F0200000502"

    def testCommonEMIActive(self):
        state = []
        octects = knx_stack.Msg.stringtooctects(self.COMMON_EMI_ACTIVE_MSG)
        msg = knx_stack.Msg(octects)
        data, new_state = knx_stack.receive.usb_hid.receive(state, msg)
        self.assertEqual(data, "cEMI")
    
    def testEMI2Active(self):
        state = []
        octects = knx_stack.Msg.stringtooctects(self.EMI_2_ACTIVE_MSG)
        msg = knx_stack.Msg(octects)
        data, new_state = knx_stack.receive.usb_hid.receive(state, msg)
        self.assertEqual(data, "emi2")


if __name__ == "__main__":
    unittest.main()