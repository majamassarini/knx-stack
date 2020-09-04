import asyncio
import knx_stack


class KnxClient(object):

    def __init__(self, ip, port, send_msgs):
        self._ip = ip
        self._port = port
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._open_connection())
        self.loop.create_task(self.knx_write(send_msgs))
        self.loop.create_task(self.knx_read())

    @asyncio.coroutine    
    def _open_connection(self):
        self.rsock, self.wsock = yield from asyncio.open_connection(self._ip, self._port)
        
    @asyncio.coroutine
    def knx_write(self, msgs):
        for msg in msgs:
            self.write(str(msg)+'\n')
            print("written {}".format(msg))
            yield from asyncio.sleep(3)
    
    @asyncio.coroutine            
    def knx_read(self):
        while True:
            msg = yield from self.read()
            octects = knx_stack.Msg.stringtooctects(msg)
            octects_msg = knx_stack.Msg(octects)
            data, new_state = knx_stack.cemi.receive(state, octects_msg)
            print("read    {}{}".format(data, new_state))
    
    def write(self, msg):
        self.wsock.write(msg.encode())
    
    @asyncio.coroutine    
    def read(self):
        msg = yield from self.rsock.readline()
        return msg.decode()[0:-1]
        
    def run(self):
        self.loop.run_forever()        


class KnxClientStub(KnxClient):
    
    def __init__(self):
        from socket import socketpair
        self.rsock, self.wsock = socketpair()
        self.rsock.setblocking(0)
        self.wsock.setblocking(0)
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.knx_write())
        self.loop.create_task(self.knx_read())        
        
    @asyncio.coroutine
    def mock(self):
        msgs = ['0113130008000B01030000290086E00000000201008100000000000000000000000000000000000000000000000000000000000000000000\n']
        while True:
            for msg in msgs:
                bytes = self.write(msg)
                yield from asyncio.sleep(3)
        
    def write(self, msg):
        return self.wsock.send(msg.encode())
    
    @asyncio.coroutine
    def read(self):
        msg = yield from self.loop.sock_recv(self.rsock, 128)
        return msg.decode()        
                
    def run(self):
        self.loop.call_soon(self.wsock.send, '0113130008000B01030000290086E000000002010081\n'.encode())
        self.loop.create_task(self.mock())
        super(KnxClientStub, self).run()


if __name__ == "__main__":
    address_table = knx_stack.cemi.AddressTable(0x1004, [], 255)
    association_table = knx_stack.cemi.AssociationTable(address_table, {})
    state = knx_stack.State(knx_stack.state.Medium.usb_hid, association_table, {})
    msgs = list()
    msgs.append((knx_stack.cemi.a_property_value_write.req.Msg(asap=0,
                                                                  object_index=0,
                                                                  property_id=0x6B,
                                                                  number_of_elements=1,
                                                                  start_index=0x0F,
                                                                  data='01'),
                 knx_stack.cemi.a_property_value_write.req.send))
    msgs.append((knx_stack.cemi.a_property_value_read.req.Msg(asap=0,
                                                                object_index=0,
                                                                property_id=0x6B,
                                                                number_of_elements=1,
                                                                start_index=0x0F),
                 knx_stack.cemi.a_property_value_read.req.send))

    for i in (0x66, 0x67, 0x68):
        msgs.append((knx_stack.cemi.a_property_value_read.req.Msg(asap=0,
                                                                    object_index=0,
                                                                    property_id=i,
                                                                    number_of_elements=1,
                                                                    start_index=0x13),
                     knx_stack.cemi.a_property_value_read.req.send))
        msgs.append((knx_stack.cemi.a_property_value_read.req.Msg(asap=0,
                                                                    object_index=0,
                                                                    property_id=i,
                                                                    number_of_elements=1,
                                                                    start_index=0x11),
                     knx_stack.cemi.a_property_value_read.req.send))

    tx_msgs = list()
    for req_msg, send_callable in msgs:
        (_, final_msg) = send_callable(state, req_msg)
        tx_msgs.append(final_msg)

    controllo_carichi_configurazione_msgs = [
'0113180008001001030000110086600000102C0603D70079101F02',
'0113170008000F01030000110086600000102C0503D50079101F',
'0113180008001001030000110086600000102C0603D70079102002',
'0113170008000F01030000110086600000102C0503D500791020',
'0113180008001001030000110086600000102C0603D70079102102',
'0113170008000F01030000110086600000102C0503D500791021',
'0113180008001001030000110086600000102C0603D7007A101F02',
'0113170008000F01030000110086600000102C0503D5007A101F',
'0113180008001001030000110086600000102C0603D7007A102002',
'0113170008000F01030000110086600000102C0503D5007A1020',
'0113180008001001030000110086600000102C0603D7007A102102',
'0113170008000F01030000110086600000102C0503D5007A1021',
'0113180008001001030000110086600000102C0603D7007B101F02',
'0113170008000F01030000110086600000102C0503D5007B101F',
'0113180008001001030000110086600000102C0603D7007B102002',
'0113170008000F01030000110086600000102C0503D5007B1020',
'0113180008001001030000110086600000102C0603D7007B102102',
'0113170008000F01030000110086600000102C0503D5007B1021',
]
    controllo_carichi_power_read_msgs = [
        '0113130008000B01030000110086E00000210F010000',
        '0113130008000B01030000110086E00000211D010000',
        '0113130008000B01030000110086E000002120010000',
    ]

    controllo_carichi_check_msgs = [
        '0113170008000F01030000110086600000102C0503D500661013',
        '0113170008000F01030000110086600000102C0503D500661011',
        '0113170008000F01030000110086600000102C0503D500671013',
        '0113170008000F01030000110086600000102C0503D500671011',
        '0113170008000F01030000110086600000102C0503D500681013',
        '0113170008000F01030000110086600000102C0503D500681011'
    ]

    controllo_carichi_all_togheter_msgs = [
        '0113170008000F01030000110086600000102D0503D500661024',
        '0113170008000F01030000110086600000102D0503D500671024',
        '0113170008000F01030000110086600000102D0503D500681024',
        '0113170008000F01030000110086600000102D0503D500661013',
        '0113170008000F01030000110086600000102D0503D500661011',
        '0113170008000F01030000110086600000102D0503D500671013',
        '0113170008000F01030000110086600000102D0503D500671011',
        '0113170008000F01030000110086600000102D0503D500681013',
        '0113170008000F01030000110086600000102D0503D500681011',
        '0113130008000B01030000110086E00000210F010000',
        '0113130008000B01030000110086E00000211D010000',
        '0113130008000B01030000110086E000002120010000',
        '0113180008001001030000110086600000102D0603D70079101F02',
        '0113170008000F01030000110086600000102D0503D50079101F',
        '0113180008001001030000110086600000102D0603D7007A101F02',
        '0113170008000F01030000110086600000102D0503D5007A101F',
        '0113180008001001030000110086600000102D0603D7007B101F02',
        '0113170008000F01030000110086600000102D0503D5007B101F',
        '0113130008000B01030000110086E00000210F010000',
        '0113130008000B01030000110086E00000211D010000',
        '0113130008000B01030000110086E000002120010000',
            ]

    #client = KnxClient('172.31.11.251', 5555, tx_msgs)
    #client = KnxClient('127.0.0.1', 5555, tx_msgs)
    #client = KnxClient('172.31.11.251', 5555, controllo_carichi_configurazione_msgs)
    client = KnxClient('172.31.11.251', 5555, controllo_carichi_power_read_msgs)
    #client = KnxClient('172.31.11.251', 5555, controllo_carichi_check_msgs)
    #client = KnxClient('172.31.11.251', 5555, controllo_carichi_all_togheter_msgs)
    client.run()
