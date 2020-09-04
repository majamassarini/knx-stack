import asyncio
import logging
import knx_stack
from typing import Iterable, NamedTuple


class Client(object):
    """
    *A minimal asynchronous USB HID KNX Client*.

    It connects to a USB HID daemon listening on port 5555.

    First run the server: a simple daemon running only on a Linux system.
    Execute the following command where the USB HID device is attached specifying the right hidraw device:

    ``# knxstack-usbhid-daemon --dev-hidraw /dev/hidrawX``

    :param ip: str, host where knxstack-usbhid-daemon is running
    :param port: int, port where knxstack-usbhid-daemon is binded (5555 by default)
    :param state: knx_stack.State, setup of all needed KNX tables
    :param send_msgs: a list of messages to be sent on KNX bus

    Example:
        Turn on and off a light and read a property from its KNX device::

            if __name__ == '__main__':

                address_table = knx_stack.layer.AddressTable(knx_stack.Address(0x100A), [], 255)
                association_table = knx_stack.layer.AssociationTable(address_table, {})
                asap_device = knx_stack.ASAP(1, "a light switch device")
                asap_command = knx_stack.ASAP(2, "turn on/off light")
                association_table.associate(asap_device, [knx_stack.Address(0x1029)])
                association_table.associate(asap_command, [knx_stack.GroupAddress(free_style=0x0F81)])
                state = knx_stack.State(knx_stack.Medium.usb_hid,
                                        association_table,
                                        knx_stack.GroupObjectTable({asap_command: knx_stack.datapointtypes.DPT_Switch}))

                msgs = list()

                switch_on = knx_stack.datapointtypes.DPT_Switch()
                switch_on.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.on
                msgs.append(knx_stack.layer.application.a_group_value_write.req.Msg(asap=asap_command, dpt=switch_on))

                switch_off = knx_stack.datapointtypes.DPT_Switch()
                switch_off.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.off
                msgs.append(knx_stack.layer.application.a_group_value_write.req.Msg(asap=asap_command, dpt=switch_off))

                msgs.append(knx_stack.layer.application.a_property_value_read.req.Msg(asap=0,
                                                                                      object_index=0x01,
                                                                                      property_id=0xC9,
                                                                                      number_of_elements=1,
                                                                                      start_index=0x01))

                client = knx_stack.client.usbhid.Client('172.31.11.251', 5555, state, msgs)
                client.run()
    """

    def __init__(self, ip: str, port: int, state: 'knx_stack.State', send_msgs: Iterable[NamedTuple]):
        self._ip = ip
        self._port = port
        self._state = state
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._open_connection())
        self.loop.create_task(self._knx_write(send_msgs))
        self.loop.create_task(self._knx_read())

        self.logger = logging.getLogger(__name__)

    async def _open_connection(self):
        self.rsock, self.wsock = await asyncio.open_connection(self._ip, self._port)

    async def _knx_write(self, msgs):
        for msg in msgs:
            octect_msg = knx_stack.encode_msg(self._state, msg)
            self._write(str(octect_msg) + '\n')
            self.logger.error("written {}".format(msg))
            await asyncio.sleep(3)
        self.loop.stop()

    async def _knx_read(self):
        while True:
            msg = await self._read()
            octects_msg = knx_stack.Msg.make_from_str(msg)
            data = knx_stack.decode_msg(self._state, octects_msg)
            self.logger.error("read {}".format(data))

    def _write(self, msg):
        self.wsock.write(msg.encode())

    async def _read(self):
        msg = await self.rsock.readline()
        return msg.decode()[0:-1]

    def run(self):
        self.loop.run_forever()


if __name__ == "__main__":
    import sys

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    root.addHandler(handler)

    address_table = knx_stack.layer.AddressTable(knx_stack.Address(0x100A), [], 255)
    association_table = knx_stack.layer.AssociationTable(address_table, {})
    asap_device = knx_stack.ASAP(1, "a floor light switch device")
    asap_command = knx_stack.ASAP(2, "turn on/off floor light")
    association_table.associate(asap_device, [knx_stack.Address(0x1029)])
    association_table.associate(asap_command, [knx_stack.GroupAddress(free_style=0x0F81)])
    state = knx_stack.State(knx_stack.Medium.usb_hid, association_table,
                            knx_stack.GroupObjectTable({asap_command: knx_stack.datapointtypes.DPT_Switch}))

    msgs = list()

    switch_on = knx_stack.datapointtypes.DPT_Switch()
    switch_on.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.on
    msgs.append(knx_stack.layer.application.a_group_value_write.req.Msg(asap=asap_command, dpt=switch_on))

    switch_off = knx_stack.datapointtypes.DPT_Switch()
    switch_off.bits.action = knx_stack.datapointtypes.DPT_Switch.Action.off
    msgs.append(knx_stack.layer.application.a_group_value_write.req.Msg(asap=asap_command, dpt=switch_off))

    msgs.append(knx_stack.layer.application.a_property_value_read.req.Msg(asap=0,
                                                                          object_index=0x01,
                                                                          property_id=0xC9,
                                                                          number_of_elements=1,
                                                                          start_index=0x01))

    client = Client('172.31.11.251', 5555, state, msgs)
    client.run()

