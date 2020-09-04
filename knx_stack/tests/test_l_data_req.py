import unittest

import knx_stack


class Test(unittest.TestCase):
    
    L_DATA_IND = "0113130008000B01030000290096E000000002010081"
    L_DATA_REQ = "0113130008000B01030000110096E000000002010081"

    def setUp(self):
        unittest.TestCase.setUp(self)
        
        octects = knx_stack.Msg.stringtooctects(self.L_DATA_IND)
        self.msg = knx_stack.Msg(octects)

        address_table = knx_stack.layer.AddressTable(0x0001, [], 255)
        association_table = knx_stack.layer.AssociationTable(address_table, {})
        new_association_table = association_table.associate(0x0002, 1)
        self.state = knx_stack.State(knx_stack.state.Medium.usb_hid, new_association_table,
                                     {1: knx_stack.datapointtypes.DPT_Switch})

    def testSendLDataReq(self):
        switch = knx_stack.datapointtypes.DPT_Switch()
        switch.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.on
        req_msg = knx_stack.send.layer.application.a_group_value_write.req.Msg(asap=1, dpt=switch)
        (_, final_msg) = knx_stack.send.layer.application.a_group_value_write.req.send(self.state, req_msg)
        self.assertEqual(str(final_msg), self.L_DATA_REQ)

    def testReceiveLDataInd(self):
        data, _ = knx_stack.receive.usb_hid.receive(self.state, self.msg)
        self.assertEqual(data[0].asap, 1)
        self.assertEqual(data[0].dpt.action, knx_stack.datapointtypes.DPT_Switch.Action.on)


if __name__ == "__main__":
    unittest.main()