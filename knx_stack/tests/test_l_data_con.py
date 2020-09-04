import unittest

import knx_stack


class Test(unittest.TestCase):
    
    L_DATA_CON = "0113130008000B010300002E00BDE0AAAA0002010000"
    
    def setUp(self):
        unittest.TestCase.setUp(self)

        address_table = knx_stack.layer.AddressTable(0x0001, [], 255)
        self.association_table = knx_stack.layer.AssociationTable(address_table, {})
        octects = knx_stack.Msg.stringtooctects(self.L_DATA_CON)
        self.msg = knx_stack.Msg(octects)

    def testLDataConWithAssociatedASAP(self):
        new_association_table = self.association_table.associate(0x0002, 1)
        state = knx_stack.State(knx_stack.Medium.usb_hid, new_association_table)
        data, new_state = knx_stack.receive.usb_hid.receive(state, self.msg)
        self.assertEqual([], data)
        self.assertIsInstance(new_state, knx_stack.State)
        
    def testLDataConWithoutAssociatedASAP(self):
        state = knx_stack.State(knx_stack.Medium.usb_hid, self.association_table)
        data, new_state = knx_stack.receive.usb_hid.receive(state, self.msg)
        self.assertIsNone(data)
        self.assertIsInstance(new_state, knx_stack.State)

    def testLDataConWithAssociatedASAPAndDpt(self):
        new_association_table = self.association_table.associate(0x0002, 1)
        state = knx_stack.State(knx_stack.Medium.usb_hid, new_association_table,
                                {1: knx_stack.datapointtypes.DPT_Switch})
        data, new_state = knx_stack.receive.usb_hid.receive(state, self.msg)
        self.assertEqual(data[0].asap, 1)
        self.assertEqual(data[0].dpt.action, knx_stack.datapointtypes.DPT_Switch.Action.off)
        self.assertEqual(data[0].status, knx_stack.layer.ConfirmFlag.ko)
        self.assertIsInstance(new_state, knx_stack.State)


if __name__ == "__main__":
    unittest.main()