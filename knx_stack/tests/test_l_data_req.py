import unittest

import knx_stack


class Test(unittest.TestCase):
    
    L_DATA_IND = "0113130008000B01030000290096E000000002010081"
    L_DATA_REQ = "0113130008000B01030000110096E000000002010081"

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.asap = knx_stack.ASAP(1)
        self.msg = knx_stack.Msg.make_from_str(self.L_DATA_IND)
        address_table = knx_stack.AddressTable(knx_stack.Address(0x0001), [], 255)
        self.association_table = knx_stack.AssociationTable(address_table)
        self.association_table.associate(self.asap, [knx_stack.GroupAddress(free_style=0x0002)])
        self.state = knx_stack.State(knx_stack.Medium.usb_hid, self.association_table,
                                     knx_stack.GroupObjectTable({self.asap: knx_stack.datapointtypes.DPT_Switch}))

    def testencodeLDataReq(self):
        switch = knx_stack.datapointtypes.DPT_Switch()
        switch.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.on
        req_msg = knx_stack.layer.application.a_group_value_write.req.Msg(asap=knx_stack.ASAP(1), dpt=switch)
        final_msg = knx_stack.encode_msg(self.state, req_msg)
        self.assertEqual(str(final_msg), self.L_DATA_REQ)

    def testdecodeLDataInd(self):
        data = knx_stack.decode_msg(self.state, self.msg)
        self.assertEqual(data[0].asap, knx_stack.ASAP(1))
        self.assertEqual(data[0].dpt.action, knx_stack.datapointtypes.DPT_Switch.Action.on)

