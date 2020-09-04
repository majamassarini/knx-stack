import knx_stack


if __name__ == "__main__":
    address_table = knx_stack.definition.AddressTable(0x102D, [], 255)
    association_table = knx_stack.definition.AssociationTable(address_table, {})
    new_association_table = association_table.associate(0x210F, 1)
    new_association_table = new_association_table.associate(0x211D, 2)
    new_association_table = new_association_table.associate(0x2120, 3)
    state = knx_stack.State(knx_stack.state.Medium.usb_hid, new_association_table,
                            {1: knx_stack.datapointtypes.DPT_Switch,
                             2: knx_stack.datapointtypes.DPT_Switch,
                             3: knx_stack.datapointtypes.DPT_Switch})

    msgs = list()
    for i in (0x66, 0x67, 0x68):
        msgs.append((knx_stack.encode.layer.application.a_property_value_read.req.Msg(asap=0, object_index=0, property_id=i,
                                                                                number_of_elements=1, start_index=0x24)))  # adjustable misuratore
    for i in (0x79, 0x7A, 0x7B):
        msgs.append((knx_stack.encode.layer.application.a_property_value_read.req.Msg(asap=0, object_index=0, property_id=i,
                                                                                number_of_elements=1, start_index=0x13)))  # adjustable linea
        msgs.append((knx_stack.encode.layer.application.a_property_value_read.req.Msg(asap=0, object_index=0, property_id=i,
                                                                                number_of_elements=1, start_index=0x11)))  # misura tipo linea
    msgs.append(
        knx_stack.layer.application.a_group_value_read.req.Msg(asap=1))
    msgs.append(
        knx_stack.layer.application.a_group_value_read.req.Msg(asap=2))
    msgs.append(
        knx_stack.layer.application.a_group_value_read.req.Msg(asap=3))
    msgs.append(
        knx_stack.encode.layer.application.a_property_value_write.req.Msg(asap=0, object_index=0, property_id=0x79,
                                                                    number_of_elements=1, start_index=0x1F, data='02'))  # potenza attiva
    msgs.append(
        knx_stack.encode.layer.application.a_property_value_read.req.Msg(asap=0, object_index=0, property_id=0x79,
                                                                   number_of_elements=1, start_index=0x1F))
    #msgs.append(PropertyValueWriteReq(asap=0, object_index=0, property_id=0x79, number_of_elements=1,
    #                                  start_index=0x20, data='02'))  # energia
    #msgs.append(PropertyValueReadReq(asap=0, object_index=0, property_id=0x79, number_of_elements=1,
    #                                  start_index=0x20))
    #msgs.append(PropertyValueWriteReq(asap=0, object_index=0, property_id=0x79, number_of_elements=1,
    #                                  start_index=0x21, data='02'))  # potenza reattiva
    #msgs.append(PropertyValueReadReq(asap=0, object_index=0, property_id=0x79, number_of_elements=1,
    #                                  start_index=0x21))
    msgs.append(
        knx_stack.encode.layer.application.a_property_value_write.req.Msg(asap=0, object_index=0, property_id=0x7A,
                                                                    number_of_elements=1, start_index=0x1F, data='02'))
    msgs.append(
        knx_stack.encode.layer.application.a_property_value_read.req.Msg(asap=0, object_index=0, property_id=0x7A,
                                                                   number_of_elements=1, start_index=0x1F))
    #msgs.append(PropertyValueWriteReq(asap=0, object_index=0, property_id=0x7A, number_of_elements=1,
    #                                  start_index=0x20, data='02'))
    #msgs.append(PropertyValueReadReq(asap=0, object_index=0, property_id=0x7A, number_of_elements=1,
    #                                  start_index=0x20))
    #msgs.append(PropertyValueWriteReq(asap=0, object_index=0, property_id=0x7A, number_of_elements=1,
    #                                  start_index=0x21, data='02'))
    #msgs.append(PropertyValueReadReq(asap=0, object_index=0, property_id=0x7A, number_of_elements=1,
    #                                  start_index=0x21))
    msgs.append(
        knx_stack.encode.layer.application.a_property_value_write.req.Msg(asap=0, object_index=0, property_id=0x7B,
                                                                    number_of_elements=1, start_index=0x1F, data='02'))
    msgs.append(
        knx_stack.encode.layer.application.a_property_value_read.req.Msg(asap=0, object_index=0, property_id=0x7B,
                                                                   number_of_elements=1, start_index=0x1F))
    #msgs.append(PropertyValueWriteReq(asap=0, object_index=0, property_id=0x7B, number_of_elements=1,
    #                                  start_index=0x20, data='02'))
    #msgs.append(PropertyValueReadReq(asap=0, object_index=0, property_id=0x7B, number_of_elements=1,
    #                                  start_index=0x20))
    #msgs.append(PropertyValueWriteReq(asap=0, object_index=0, property_id=0x7B, number_of_elements=1,
    #                                  start_index=0x21, data='02'))
    #msgs.append(PropertyValueReadReq(asap=0, object_index=0, property_id=0x7B, number_of_elements=1,
    #                                  start_index=0x21))
    msgs.append(
        knx_stack.layer.application.a_group_value_read.req.Msg(asap=1))
    msgs.append(
        knx_stack.layer.application.a_group_value_read.req.Msg(asap=2))
    msgs.append(
        knx_stack.layer.application.a_group_value_read.req.Msg(asap=3))

    for msg in msgs:
        if isinstance(msg, knx_stack.encode.layer.application.a_property_value_write.req.Msg):
            final_msg = knx_stack.encode_msg(state, msg)
        elif isinstance(msg, knx_stack.encode.layer.application.a_property_value_read.req.Msg):
            final_msg = knx_stack.encode_msg(state, msg)
        else:
            final_msg = knx_stack.encode_msg(state, msg)

        print(final_msg)
