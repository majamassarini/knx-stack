import unittest
import knx_stack


class Test(unittest.TestCase):
    
    L_DATA_IND = "0113130008000B010300002900BCE000010002010080"
    L_DATA_IND_2 = "0113140008000C010300002900B4E00001000202008005"

    def setUp(self):
        unittest.TestCase.setUp(self)
        
        address_table = knx_stack.layer.AddressTable(0x0001, [], 255)
        self.association_table = knx_stack.layer.AssociationTable(address_table, {})
        octects = knx_stack.Msg.stringtooctects(self.L_DATA_IND)
        self.msg = knx_stack.Msg(octects)
        octects = knx_stack.Msg.stringtooctects(self.L_DATA_IND_2)
        self.msg2 = knx_stack.Msg(octects)

    def testLDataIndWithAssociatedASAP(self):
        new_association_table = self.association_table.associate(0x0002, 1)
        state = knx_stack.State(knx_stack.state.Medium.usb_hid, new_association_table)
        data, new_state = knx_stack.receive.usb_hid.receive(state, self.msg)
        self.assertEqual([], data)
        self.assertIsInstance(new_state, knx_stack.State)

    def testLDataIndWithoutAssociatedASAP(self):        
        state = knx_stack.State(knx_stack.state.Medium.usb_hid, self.association_table)
        data, new_state = knx_stack.receive.usb_hid.receive(state, self.msg)
        self.assertIsNone(data)
        self.assertIsInstance(new_state, knx_stack.State)

    def testLDataIndWithAssociatedASAPAndDpt(self):
        new_association_table = self.association_table.associate(0x0002, 1)
        state = knx_stack.State(knx_stack.state.Medium.usb_hid, new_association_table,
                                {1: knx_stack.datapointtypes.DPT_Switch})
        data, new_state = knx_stack.receive.usb_hid.receive(state, self.msg)
        self.assertEqual(data[0].asap, 1)
        self.assertEqual(data[0].dpt.action, knx_stack.datapointtypes.DPT_Switch.Action.off)
        self.assertIsInstance(new_state, knx_stack.State)

    def testLDataIndWithAssociatedASAPAndDpt2(self):
        new_association_table = self.association_table.associate(0x0002, 1)
        state = knx_stack.State(knx_stack.state.Medium.usb_hid, new_association_table,
                                {1: knx_stack.datapointtypes.DPTVimarScene})
        data, new_state = knx_stack.receive.usb_hid.receive(state, self.msg2)
        self.assertEqual(data[0].asap, 1)
        self.assertEqual(data[0].dpt.index, 5)
        self.assertIsInstance(new_state, knx_stack.State)

class TestDPTValue(unittest.TestCase):

    L_DATA_NEG_TEMP_DPT  = "0113150008000d010300002900bcd011fd0a0203008087ce0000000000000000000000000000000000000000000000000"
    L_DATA_NEG_TEMP_DPT2 = "0113150008000d010300002900bcd011fd0a0203008087d80000000000000000000000000000000000000000000000000000000000000000"

    def setUp(self):
        unittest.TestCase.setUp(self)

        address_table = knx_stack.layer.AddressTable(0x0001, [], 255)
        self.association_table = knx_stack.layer.AssociationTable(address_table, {})
        octects = knx_stack.Msg.stringtooctects(self.L_DATA_NEG_TEMP_DPT)
        self.msg = knx_stack.Msg(octects)
        octects = knx_stack.Msg.stringtooctects(self.L_DATA_NEG_TEMP_DPT2)
        self.msg2 = knx_stack.Msg(octects)

    def testLDataIndWithAssociatedASAPAndDptFloat16(self):
        new_association_table = self.association_table.associate(0x0a02, 1)
        state = knx_stack.State(knx_stack.state.Medium.usb_hid, new_association_table,
                                {1: knx_stack.datapointtypes.DPT_Value_Temp})
        data, new_state = knx_stack.receive.usb_hid.receive(state, self.msg)
        self.assertEqual(data[0].asap, 1)
        self.assertEqual(data[0].dpt.decode(), -0.5) #is -19.48
        self.assertIsInstance(new_state, knx_stack.State)

    def testLDataIndWithAssociatedASAPAndDptFloat16_2(self):
        new_association_table = self.association_table.associate(0x0a02, 1)
        state = knx_stack.State(knx_stack.state.Medium.usb_hid, new_association_table,
                                {1: knx_stack.datapointtypes.DPT_Value_Temp})
        data, new_state = knx_stack.receive.usb_hid.receive(state, self.msg2)
        self.assertEqual(data[0].asap, 1)
        self.assertEqual(data[0].dpt.decode(), -0.4) #is -20.08
        self.assertIsInstance(new_state, knx_stack.State)


if __name__ == "__main__":
    unittest.main()

    def testLDataIndWithAssociatedASAPAndDpt3(self):
        new_association_table = self.association_table.associate(0x0002, 1)
        state = knx_stack.State(knx_stack.state.Medium.usb_hid, new_association_table,
                                {1: knx_stack.datapointtypes.DPTVimarScene})
        data, new_state = knx_stack.receive.usb_hid.receive(state, self.msg3)
        self.assertEqual(data[0].asap, 1)
        self.assertEqual(data[0].dpt.index, 5)
        self.assertIsInstance(new_state, knx_stack.State)


if __name__ == "__main__":
    unittest.main()