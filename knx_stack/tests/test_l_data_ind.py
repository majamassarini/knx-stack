import unittest
import knx_stack


class Test(unittest.TestCase):
    
    L_DATA_IND = "0113130008000B010300002900BCE000010002010080"
    L_DATA_IND_2 = "0113140008000C010300002900B4E00001000202008005"

    def setUp(self):
        unittest.TestCase.setUp(self)

        address_table = knx_stack.definition.AddressTable(knx_stack.Address(1), [], 255)
        self.association_table = knx_stack.AssociationTable(address_table)
        self.groupobject_table = knx_stack.GroupObjectTable()
        self.asap = knx_stack.ASAP(1, "prova")
        self.association_table.associate(self.asap, [knx_stack.GroupAddress(free_style=0x0002)])
        self.state = knx_stack.State(knx_stack.state.Medium.usb_hid, self.association_table, self.groupobject_table)
        self.msg = knx_stack.Msg.make_from_str(self.L_DATA_IND)
        self.msg2 = knx_stack.Msg.make_from_str(self.L_DATA_IND_2)

    def testLDataIndWithAssociatedASAP(self):
        data = knx_stack.decode_msg(self.state, self.msg)
        self.assertEqual([], data)

    def testLDataIndWithoutAssociatedASAP(self):        
        state = knx_stack.State(knx_stack.state.Medium.usb_hid, self.association_table, self.groupobject_table)
        self.association_table.disassociate(self.asap, [knx_stack.GroupAddress(free_style=0x0002)])
        data = knx_stack.decode_msg(state, self.msg)
        self.assertEqual([], data)

    def testLDataIndWithAssociatedASAPAndDpt(self):
        state = knx_stack.State(knx_stack.state.Medium.usb_hid,
                                self.association_table,
                                knx_stack.GroupObjectTable({self.asap: knx_stack.datapointtypes.DPT_Switch}))
        data = knx_stack.decode_msg(state, self.msg)
        self.assertEqual(data[0].asap, knx_stack.ASAP(1))
        self.assertEqual(data[0].dpt.action, knx_stack.datapointtypes.DPT_Switch.Action.off)

    def testLDataIndWithAssociatedASAPAndDpt2(self):
        state = knx_stack.State(knx_stack.state.Medium.usb_hid,
                                self.association_table,
                                knx_stack.GroupObjectTable({self.asap: knx_stack.datapointtypes.DPTVimarScene}))
        data = knx_stack.decode_msg(state, self.msg2)
        self.assertEqual(data[0].asap, knx_stack.ASAP(1))
        self.assertEqual(data[0].dpt.index, 5)


class TestDPTValue(unittest.TestCase):

    L_DATA_NEG_TEMP_DPT = "0113150008000d010300002900bcd011fd0a0203008087ce0000000000000000000000000000000000000000000000000"
    L_DATA_NEG_TEMP_DPT2 = "0113150008000d010300002900bcd011fd0a0203008087d80000000000000000000000000000000000000000000000000000000000000000"

    def setUp(self):
        address_table = knx_stack.AddressTable(knx_stack.Address(0x0001), [], 255)
        association_table = knx_stack.AssociationTable(address_table)
        asap = knx_stack.ASAP(1, "prova")
        association_table.associate(asap, [knx_stack.GroupAddress(free_style=0x0A02)])
        self.state = knx_stack.State(knx_stack.Medium.usb_hid,
                                     association_table,
                                     knx_stack.GroupObjectTable({asap: knx_stack.datapointtypes.DPT_Value_Temp}))
        self.msg = knx_stack.Msg.make_from_str(self.L_DATA_NEG_TEMP_DPT)
        self.msg2 = knx_stack.Msg.make_from_str(self.L_DATA_NEG_TEMP_DPT2)

    def testLDataIndWithAssociatedASAPAndDptFloat16(self):
        data = knx_stack.decode_msg(self.state, self.msg)
        self.assertEqual(data[0].asap, knx_stack.ASAP(1))
        self.assertEqual(data[0].dpt.decode(), -0.5)  # is -19.48

    def testLDataIndWithAssociatedASAPAndDptFloat16_2(self):
        data = knx_stack.decode_msg(self.state, self.msg2)
        self.assertEqual(data[0].asap, knx_stack.ASAP(1))
        self.assertEqual(data[0].dpt.decode(), -0.4)  # is -20.08

