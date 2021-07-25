# knx-stack

[![Build Status](https://travis-ci.com/majamassarini/knx-stack.svg?branch=master)](https://travis-ci.com/majamassarini/knx-stack)
[![codecov](https://codecov.io/gh/majamassarini/knx-stack/branch/master/graph/badge.svg?token=HQ27JK26MT)](https://codecov.io/gh/majamassarini/knx-stack)
[![Documentation Status](https://readthedocs.com/projects/maja-massarini-knx-stack/badge/?version=latest&token=8336c023fa5922b6e166d8ef4cc2b5b52c8fa4d746995cddc6a29a99656e5cce)](https://maja-massarini-knx-stack.readthedocs-hosted.com/en/latest/?badge=latest)

A Python 3 KNX stack, not complete but easily extensible.

It is able to *encode/decode* knx messages for both **USB HID** and **KNXnet IP**.

It can be used with an **asynchronous** or **synchronous** client.

## Examples

### Setup 
```python

    >>> individual_address = knx_stack.Address(0x0001)
    >>> abcd = knx_stack.GroupAddress(free_style=0xABCD)
    >>> abce = knx_stack.GroupAddress(three_level_style=knx_stack.address.ThreeLevelStyle(main=21, middle=3, sub=206))
    >>> abcf = knx_stack.GroupAddress(two_level_style=knx_stack.address.TwoLevelStyle(main=21, sub=975))

    >>> asap_1 = knx_stack.ASAP(1, "an application service access point to 0xABCD")
    >>> asap_2 = knx_stack.ASAP(2, "another application service access point to 0xABCD")
    >>> asap_3 = knx_stack.ASAP(3)

    >>> address_table = knx_stack.AddressTable(individual_address, [], 255)
    >>> association_table = knx_stack.AssociationTable(address_table, [])
    >>> association_table.associate(asap_1, [abcd])
    >>> association_table.associate(asap_2, [abcd])
    >>> association_table.associate(asap_3, [abce, abcf])

    >>> group_object_table = knx_stack.GroupObjectTable({asap_1: knx_stack.datapointtypes.DPT_Switch,
    ...                                                  asap_2: knx_stack.datapointtypes.DPT_Switch,
    ...                                                  asap_3: knx_stack.datapointtypes.DPT_Value_Temp,
    ...                                                  })

    >>> association_table
    AssociationTable: asap -> addresses
        0 (individual address) -> [0x0001]
        1 (an application service access point to 0xABCD) -> [(0xABCD 21/973 21/3/205)]
        2 (another application service access point to 0xABCD) -> [(0xABCD 21/973 21/3/205)]
        3 -> [(0xABCE 21/974 21/3/206), (0xABCF 21/975 21/3/207)]
    AddressTable: individual address: 0x0001, max_size=255
    <BLANKLINE>
        tsap -> individual address
        0 -> 0x0001
        tsap -> group address (hex_free_style two_level_style three_level_style)
        1 -> (0xABCD 21/973 21/3/205)
        2 -> (0xABCE 21/974 21/3/206)
        3 -> (0xABCF 21/975 21/3/207)
    <BLANKLINE>

    >>> group_object_table
    GroupObjectTable: ASAP -> datapointtype
        1 (an application service access point to 0xABCD) -> DPT_Switch
        2 (another application service access point to 0xABCD) -> DPT_Switch
        3 -> DPT_Value_Temp
    <BLANKLINE>
    
```

### USB HID encode/decode

```python

    >>> state = knx_stack.State(knx_stack.state.Medium.usb_hid, association_table, group_object_table)

    >>> msg = knx_stack.Msg.make_from_str("0113130008000B010300002900BCE00001ABCD010080")
    >>> knx_stack.decode_msg(state, msg)
    [GroupValueWriteInd (DPT_Switch {'action': 'off'} for asap 1 (an application service access point to 0xABCD)), GroupValueWriteInd (DPT_Switch {'action': 'off'} for asap 2 (another application service access point to 0xABCD))]

    >>> msg = knx_stack.Msg.make_from_str("0113130008000B010300002900BCE00001ABCC010081")
    >>> knx_stack.decode_msg(state, msg)
    []

    >>> msg = knx_stack.Msg.make_from_str("0113140008000C010300002900B4E00001ABCE02008005")
    >>> knx_stack.decode_msg(state, msg)
    [GroupValueWriteInd (DPT_Value_Temp: {'decoded_value': 0.05} for asap 3 (an application service access point to 0xABCE & 0xABCF))]

    >>> req = knx_stack.layer.application.a_group_value_read.req.Msg(asap=asap_3)
    >>> knx_stack.encode_msg(state, req)
    0113130008000B01030000110096E00000ABCE010000

    >>> dpt = knx_stack.datapointtypes.DPT_Value_Temp()
    >>> dpt.encode(0.05)
    >>> req = knx_stack.layer.application.a_group_value_write.req.Msg(asap=asap_3, dpt=dpt)
    >>> knx_stack.encode_msg(state, req)
    0113150008000D01030000110096E00000ABCE0300800005
    
```

### KNXnet IP encode/decode

```python

    >>> state = knx_stack.knxnet_ip.State(knx_stack.state.Medium.knxnet_ip, association_table, group_object_table)

    >>> state.sequence_counter_remote = 1
    >>> msg = knx_stack.knxnet_ip.Msg.make_from_str("061004200015047401002900BCE00001ABCD010080")
    >>> knx_stack.decode_msg(state, msg)
    [TunnelingReq(sequence counter=1, status=<ErrorCodes.E_NO_ERROR: 0>), GroupValueWriteInd (DPT_Switch {'action': 'off'} for asap 1 (an application service access point to 0xABCD)), GroupValueWriteInd (DPT_Switch {'action': 'off'} for asap 2 (another application service access point to 0xABCD))]

    >>> msg = knx_stack.knxnet_ip.Msg.make_from_str("061004200016047401002900B4E00001ABCE02008005")
    >>> knx_stack.decode_msg(state, msg)
    [TunnelingReq(sequence counter=1, status=<ErrorCodes.E_NO_ERROR: 0>), GroupValueWriteInd (DPT_Value_Temp: {'decoded_value': 0.05} for asap 3 (an application service access point to 0xABCE & 0xABCF))]
    >>> req = knx_stack.layer.application.a_group_value_read.req.Msg(asap=asap_3)
    >>> knx_stack.encode_msg(state, req)
    06100420001504000000110096E00000ABCE010000

    >>> dpt = knx_stack.datapointtypes.DPT_Value_Temp()
    >>> dpt.encode(0.05)
    >>> req = knx_stack.layer.application.a_group_value_write.req.Msg(asap=asap_3, dpt=dpt)
    >>> knx_stack.encode_msg(state, req)
    06100420001704000000110096E00000ABCE0300800005

```


## Getting Started

```
pip install knx-stack
```

## Diving In

[Documentation](https://maja-massarini-knx-stack.readthedocs-hosted.com/en/latest/?)


