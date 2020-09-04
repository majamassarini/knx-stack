import unittest

import knx_stack


class Test(unittest.TestCase):
    
    L_DATA_IND = "011319000800110103000029009660102C00000603D7007B101F0002"
    L_DATA_REQ = "0113180008001001030000110096600000102C0603D7007B101F02"

    def setUp(self):
        unittest.TestCase.setUp(self)
        
        octects = knx_stack.Msg.stringtooctects(self.L_DATA_IND)
        self.msg = knx_stack.Msg(octects)

        address_table = knx_stack.layer.AddressTable(0x102C, [], 255)
        association_table = knx_stack.layer.AssociationTable(address_table, {})
        self.state = knx_stack.State(knx_stack.Medium.usb_hid, association_table, {})

    def testSendLDataReq(self):
        req_msg = knx_stack.send.layer.application.a_property_value_write.req.Msg(asap=0, object_index=0, property_id=0x7B,
                                                                                  number_of_elements=1, start_index=0x1F, data='02')
        (_, final_msg) = knx_stack.send.layer.application.a_property_value_write.req.send(self.state, req_msg)
        self.assertEqual(str(final_msg), self.L_DATA_REQ)

    def testReceiveLDataInd(self):
        data, _ = knx_stack.receive.usb_hid.receive(self.state, self.msg)
        self.assertEqual(data[0].asap, 0)
        self.assertEqual(str(data[0].data), '02')


if __name__ == "__main__":
    unittest.main()