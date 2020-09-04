import unittest

import knx_stack


class Test(unittest.TestCase):
    
    L_DATA_IND = "011319000800110103000029009660102C00000603D7007B101F02"
    L_DATA_REQ = "0113180008001001030000110096600000102C0603D7007B101F02"

    def setUp(self):
        unittest.TestCase.setUp(self)
        
        self.msg = knx_stack.Msg.make_from_str(self.L_DATA_IND)
        address_table = knx_stack.AddressTable(knx_stack.Address(0x102C), [], 255)
        association_table = knx_stack.AssociationTable(address_table, {})
        self.state = knx_stack.State(knx_stack.Medium.usb_hid, association_table, {})

    def testencodeLDataReq(self):
        req_msg = knx_stack.layer.application.a_property_value_write.req.Msg(asap=0,
                                                                             object_index=0,
                                                                             property_id=0x7B,
                                                                             number_of_elements=1,
                                                                             start_index=0x1F,
                                                                             data='02')
        final_msg = knx_stack.encode_msg(self.state, req_msg)
        self.assertEqual(str(final_msg), self.L_DATA_REQ)

    def testdecodeLDataInd(self):
        data = knx_stack.decode_msg(self.state, self.msg)
        self.assertEqual(data[0].asap, knx_stack.ASAP(0))
        self.assertEqual(str(data[0].data), '02')

