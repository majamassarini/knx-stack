from ctypes import c_uint8, LittleEndianStructure, c_uint16, Union
from enum import IntEnum
from knx_stack import Msg


class Priority(IntEnum):
    low = 0b11
    normal = 0b01
    urgent = 0b10
    system = 0b00


class AcknowledgeRequest(IntEnum):
    no = 0
    yes = 1


class RepeatFlag(IntEnum):
    repeat_on_error = 0
    do_not_repeat = 1


class SystemBroadcastFlag(IntEnum):
    system_broadcast = 0
    broadcast = 1


class FrameTypeFlag(IntEnum):
    extended = 0
    standard = 1


class AddressType(IntEnum):
    individual = 0
    group = 1


class ConfirmFlag(IntEnum):
    ok = 0
    ko = 1


class NSDU(IntEnum):
    T_Data_Broadcast_PDU = 0
    T_Data_Group_PDU = 1
    T_Data_Tag_Group_PDU = 2
    T_Data_Individual_PDU = 3
    T_Data_Connected_PDU = 4
    T_Connect_PDU = 5
    T_Disconnect_PDU = 6
    T_ACK_PDU = 7
    T_NACK_PDU = 8


class _Cntrl1(LittleEndianStructure):

    _fields_ = [('confirm_flag', c_uint8, 1),
                ('acknowledge_request_flag', c_uint8, 1),
                ('priority', c_uint8, 2),
                ('system_broadcast', c_uint8, 1),
                ('repeat_flag', c_uint8, 1),
                ('padding', c_uint8, 1),
                ('frame_type_flag', c_uint8, 1)
                ]


class Cntrl1(Union):

    _fields_ = [('bits', _Cntrl1),
                ('value', c_uint8)]


class _Cntrl2(LittleEndianStructure):

    _fields_ = [('extended_frame_format', c_uint8, 4),
                ('hop_count', c_uint8, 3),
                ('address_type', c_uint8, 1),
                ]


class Cntrl2(Union):

    _fields_ = [('bits', _Cntrl2),
                ('value', c_uint8)]


class _TPCI(LittleEndianStructure):

    _fields_ = [('ack_nack', c_uint8, 2),
                ('sequence_number', c_uint8, 4),
                ('numbered', c_uint8, 1),
                ('control_flag', c_uint8, 1),
                ]


class TPCI(Union):

    _fields_ = [('bits', _TPCI),
                ('value', c_uint8)]


class _APCI(LittleEndianStructure):

    _fields_ = [('data', c_uint8, 6),
                ('apci', c_uint8, 2)]


class APCI(Union):

    _fields_ = [('bits', _APCI),
                ('value', c_uint8)]


class L_Data(LittleEndianStructure):
    """
    >>> from knx_stack.msg import Msg
    >>> s = "BCE000010002010080"
    >>> msg = Msg.make_from_str(s)
    >>> (ldata, _) = L_Data.make_from(msg)
    >>> ldata.source
    1
    >>> ldata.destination
    2
    >>> AddressType.group == ldata.address_type
    True
    >>> NSDU.T_Data_Group_PDU == ldata.nsdu
    True
    >>> ldata.apci
    128
    """

    def __init__(self, *args, **kwargs):
        super(L_Data, self).__init__(*args, **kwargs)
        self._make_default()

    def _make_default(self):
        self._cntrl1.bits.acknowledge_request_flag = AcknowledgeRequest.yes
        self._cntrl1.bits.priority = Priority.normal
        self._cntrl1.bits.repeat_flag = RepeatFlag.repeat_on_error
        self._cntrl1.bits.frame_type_flag = FrameTypeFlag.standard
        self._cntrl1.bits.system_broadcast = SystemBroadcastFlag.broadcast

        self._cntrl2.bits.hop_count = 6

    _fields_ = [('_apci', APCI),
                ('_tpci', TPCI),
                ('_npdu_length', c_uint8),
                ('_destination', c_uint16),
                ('_source', c_uint16),
                ('_cntrl2', Cntrl2),
                ('_cntrl1', Cntrl1),
                ]

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, value):
        self._destination = value

    @property
    def address_type(self):
        return AddressType(self._cntrl2.bits.address_type)

    @address_type.setter
    def address_type(self, value):
        self._cntrl2.bits.address_type = value

    @property
    def connected(self):
        if self._tpci.bits.control_flag:
            return True
        else:
            return False

    @connected.setter
    def connected(self, is_connected):
        if is_connected:
            self._tpci.bits.control_flag = 1
        else:
            self._tpci.bits.control_flag = 0

    @property
    def status(self):
        return ConfirmFlag(self._cntrl1.bits.confirm_flag)

    @property
    def apci(self):
        return (self._tpci.bits.ack_nack << 8) + self._apci.value

    @property
    def apci_value(self):
        return self._apci.value

    @property
    def tpci(self):
        return self._tpci.value

    @apci.setter
    def apci(self, value):
        self._tpci.bits.ack_nack = value >> 8
        self._apci.value = value

    @property
    def data(self):
        return self._apci.bits.data

    @data.setter
    def data(self, value):
        self._apci.bits.data = value

    @property
    def nsdu(self):
        pdu = None
        if (self._cntrl2.bits.address_type == AddressType.group and
            self._tpci.bits.control_flag == 0 and
            self._tpci.bits.numbered == 0 and
            self._tpci.bits.sequence_number == 0 and
            self._destination == 0):
            pdu = NSDU.T_Data_Broadcast_PDU
        elif (self._cntrl2.bits.address_type == AddressType.group and
              self._tpci.bits.control_flag == 0 and
              self._tpci.bits.numbered == 0 and
              self._tpci.bits.sequence_number == 0 and
              self._destination != 0):
            pdu = NSDU.T_Data_Group_PDU
        elif (self._cntrl2.bits.address_type == AddressType.group and
              self._tpci.bits.control_flag == 0 and
              self._tpci.bits.numbered == 0 and
              self._tpci.bits.sequence_number == 1):
            pdu = NSDU.T_Data_Tag_Group_PDU
        elif (self._cntrl2.bits.address_type == AddressType.individual and
              self._tpci.bits.control_flag == 0 and
              self._tpci.bits.numbered == 0 and
              self._tpci.bits.sequence_number == 0):
            pdu = NSDU.T_Data_Individual_PDU
        elif (self._cntrl2.bits.address_type == AddressType.individual and
              self._tpci.bits.control_flag == 0 and
              self._tpci.bits.numbered == 1):
            pdu = NSDU.T_Data_Connected_PDU
        elif (self._cntrl2.bits.address_type == AddressType.individual and
              self._tpci.bits.control_flag == 1 and
              self._tpci.bits.numbered == 0):
            pdu = NSDU.T_Data_Connected_PDU
        elif (self._cntrl2.bits.address_type == AddressType.individual and
              self._tpci.bits.control_flag == 1 and
              self._tpci.bits.numbered == 0 and
              self._tpci.bits.ack_nack == 0):
            pdu = NSDU.T_Connect_PDU
        elif (self._cntrl2.bits.address_type == AddressType.individual and
              self._tpci.bits.control_flag == 1 and
              self._tpci.bits.numbered == 0 and
              self._tpci.bits.ack_nack == 1):
            pdu = NSDU.T_Disconnect_PDU
        elif (self._cntrl2.bits.address_type == AddressType.individual and
              self._tpci.bits.control_flag == 1 and
              self._tpci.bits.numbered == 1 and
              self._tpci.bits.ack_nack == 2):
            pdu = NSDU.T_ACK_PDU
        elif (self._cntrl2.bits.address_type == AddressType.individual and
              self._tpci.bits.control_flag == 1 and
              self._tpci.bits.numbered == 1 and
              self._tpci.bits.ack_nack == 3):
            pdu = NSDU.T_NACK_PDU  
        return pdu


    @nsdu.setter
    def nsdu(self, pdu):
        if pdu == NSDU.T_Data_Broadcast_PDU:
            self._tpci.bits.control_flag = 0
            self._tpci.bits.numbered = 0
            self._tpci.bits.sequence_number = 0

        elif pdu == NSDU.T_Data_Group_PDU:
            self._tpci.bits.control_flag = 0
            self._tpci.bits.numbered = 0
            self._tpci.bits.sequence_number = 0

        elif pdu == NSDU.T_Data_Tag_Group_PDU:
            self._tpci.bits.control_flag = 0
            self._tpci.bits.numbered = 0
            self._tpci.bits.sequence_number = 1

        elif pdu == NSDU.T_Data_Individual_PDU:
            self._tpci.bits.control_flag = 0
            self._tpci.bits.numbered = 0
            self._tpci.bits.sequence_number = 0

        elif pdu == NSDU.T_Data_Connected_PDU:
            self._tpci.bits.control_flag = 0
            self._tpci.bits.numbered = 1

        elif pdu == NSDU.T_Data_Connected_PDU:
            self._tpci.bits.control_flag = 1
            self._tpci.bits.numbered = 0

        elif pdu == NSDU.T_Connect_PDU:
            self._tpci.bits.control_flag = 1
            self._tpci.bits.numbered = 0
            self._tpci.bits.ack_nack = 0

        elif pdu == NSDU.T_Disconnect_PDU:
            self._tpci.bits.control_flag = 1
            self._tpci.bits.numbered = 0
            self._tpci.bits.ack_nack = 1

        elif pdu == NSDU.T_ACK_PDU:
            self._tpci.bits.control_flag = 1
            self._tpci.bits.numbered = 1
            self._tpci.bits.ack_nack = 2

        elif pdu == NSDU.T_NACK_PDU:
            self._tpci.bits.control_flag = 1
            self._tpci.bits.numbered = 1
            self._tpci.bits.ack_nack = 3


    @staticmethod
    def make_from(msg):
        l_data = L_Data()
        (cntrl1, body) = msg.octect()
        l_data._cntrl1 = Cntrl1(value=cntrl1.value)
        (cntrl2, body) = body.octect()
        l_data._cntrl2 = Cntrl2(value=cntrl2.value)
        (source, body) = body.short()
        l_data._source = source.value
        (destination, body) = body.short()
        l_data._destination = destination.value
        (npdu_length, body) = body.octect()
        l_data._npdu_length = npdu_length.value
        (tpci, body) = body.octect()
        l_data._tpci = TPCI(value=tpci.value)
        (apci, body) = body.octect()
        l_data._apci = APCI(value=apci.value)

        if body:
            new_msg = Msg(body)
        else:
            new_msg = Msg([apci])

        return l_data, new_msg

    def __repr__(self, *args, **kwargs):
        s = ("""source: %d (0x%04X), destination: %d (0x%04X), address_type: %s""" %
             (self.source,
              self.source,
              self.destination,
              self.destination,
              self.address_type, 
              ))
        return s    
