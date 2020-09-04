import unittest
import knx_stack


class Test(unittest.TestCase):
    
    COMMON_EMI_ACTIVE_MSG = "01130A000800020F0200000503"
    EMI_2_ACTIVE_MSG = "01130A000800020F0200000502"

    def testCommonEMIActive(self):
        state = knx_stack.State(knx_stack.Medium.usb_hid, None, None)
        msg = knx_stack.Msg.make_from_str(self.COMMON_EMI_ACTIVE_MSG)
        data = knx_stack.decode_msg(state, msg)
        self.assertTrue(len(data), 1)
        self.assertEqual(data[0].type, "cEMI")
    
    def testEMI2Active(self):
        state = knx_stack.State(knx_stack.Medium.usb_hid, None, None)
        msg = knx_stack.Msg.make_from_str(self.EMI_2_ACTIVE_MSG)
        data = knx_stack.decode_msg(state, msg)
        self.assertTrue(len(data), 1)
        self.assertEqual(data[0].type, "emi2")
