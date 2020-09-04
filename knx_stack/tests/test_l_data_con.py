import unittest

import knx_stack


class Test(unittest.TestCase):
    
    L_DATA_CON = "0113130008000B010300002E00BDE0AAAA0002010000"
    
    def setUp(self):
        unittest.TestCase.setUp(self)

        address_table = knx_stack.AddressTable(knx_stack.Address(0x0001), [], 255)
        self.association_table = knx_stack.AssociationTable(address_table)
        self.groupobject_table = knx_stack.GroupObjectTable()
        self.msg = knx_stack.Msg.make_from_str(self.L_DATA_CON)

    def testLDataConWithAssociatedASAP(self):
        self.association_table.associate(knx_stack.ASAP(1), [knx_stack.GroupAddress(free_style=0x0002)])
        state = knx_stack.State(knx_stack.Medium.usb_hid, self.association_table, self.groupobject_table)
        data = knx_stack.decode_msg(state, self.msg)
        self.assertEqual([], data)

    def testLDataConWithoutAssociatedASAP(self):
        state = knx_stack.State(knx_stack.Medium.usb_hid, self.association_table, self.groupobject_table)
        data = knx_stack.decode_msg(state, self.msg)
        self.assertEqual(data, [])

    def testLDataConWithAssociatedASAPAndDpt(self):
        self.association_table.associate(knx_stack.ASAP(1), [knx_stack.GroupAddress(free_style=0x0002)])
        state = knx_stack.State(knx_stack.Medium.usb_hid, self.association_table,
                                knx_stack.GroupObjectTable({knx_stack.ASAP(1): knx_stack.datapointtypes.DPT_Switch}))
        data = knx_stack.decode_msg(state, self.msg)
        self.assertEqual(data[0].asap, knx_stack.ASAP(1))
        self.assertEqual(data[0].dpt.action, knx_stack.datapointtypes.DPT_Switch.Action.off)
        self.assertEqual(data[0].status, knx_stack.definition.layer.ConfirmFlag.ko)
